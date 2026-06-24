# Movie Explorer Platform

A full-stack platform for exploring movies, actors, directors, and genres — with backend-driven filtering, aggregated ratings/reviews, and a localStorage favourites list.

## Stack

| Layer     | Technology                                             |
|-----------|--------------------------------------------------------|
| Backend   | Python 3.12 · Django 4.2 · Django REST Framework 3.15 |
| Database  | SQLite (Docker volume-persisted)                       |
| API Docs  | drf-spectacular (OpenAPI 3 · Swagger UI · ReDoc)       |
| Frontend  | Vue 3 · Vite · TypeScript · Tailwind CSS               |
| State     | Pinia (favourites → localStorage)                      |
| Container | Docker + Docker Compose                                |

---

## Quick Start

> **Prerequisites:** Docker Desktop running.

```bash
git clone <repo-url>
cd move-villa
docker compose up --build
```

| Service      | URL                              |
|--------------|----------------------------------|
| Frontend     | http://localhost:8080            |
| API root     | http://localhost:8000/api/       |
| Swagger UI   | http://localhost:8000/api/docs/  |
| ReDoc        | http://localhost:8000/api/redoc/ |
| Django admin | http://localhost:8000/admin/     |

> **Build = lint + tests.** Both the backend and frontend Dockerfiles run linting and unit tests during `docker compose up --build`. If either fails, the build stops.

> **Auto-seeded.** The backend seeds 10 genres, 10 directors, 10 actors, 10 movies, and 10 reviews on first start — no manual step needed.

---

## Running Locally (without Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
# API available at http://localhost:8000/api/
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Dev server at http://localhost:5173 — proxies /api → http://localhost:8000
```

---

## Lint & Tests

### Backend

```bash
cd backend
source .venv/bin/activate
ruff check .    # lint (E, F, W, I rules)
pytest -q       # 27 tests: models, filters, API endpoints, edge cases
```

### Frontend

```bash
cd frontend
npm run lint        # ESLint (vue/recommended + typescript-eslint, 0 warnings allowed)
npm run test:run    # Vitest — 19 tests: MovieCard, FilterBar, favorites store
```

---

## API Reference

All endpoints are documented interactively at **`/api/docs/`** (Swagger UI) and **`/api/redoc/`**.

### Movies — `GET /api/movies/`

| Parameter      | Type    | Description                               |
|----------------|---------|-------------------------------------------|
| `search`       | string  | Title substring (case-insensitive)        |
| `genre`        | integer | Filter by genre id                        |
| `genre_name`   | string  | Genre name substring (case-insensitive)   |
| `director`     | integer | Filter by director id                     |
| `actor`        | integer | Filter by actor id                        |
| `release_year` | integer | Exact release year                        |
| `year_min`     | integer | Release year ≥ value                      |
| `year_max`     | integer | Release year ≤ value                      |
| `ordering`     | string  | `release_year`, `title`, `-release_year`  |
| `page`         | integer | Page number (page_size = 12)              |

**Slug-based detail:** `GET /api/movies/<slug>/` — e.g. `/api/movies/inception-2010/`

### Actors — `GET /api/actors/`

| Parameter | Type    | Description                         |
|-----------|---------|-------------------------------------|
| `movie`   | integer | Actors who appeared in this movie   |
| `genre`   | integer | Actors whose movies span this genre |
| `search`  | string  | Name substring                      |

**Detail:** `GET /api/actors/<slug>/` — e.g. `/api/actors/cillian-murphy/`

### Directors — `GET /api/directors/`

| Parameter | Type   | Description        |
|-----------|--------|--------------------|
| `search`  | string | Name substring     |

**Detail:** `GET /api/directors/<slug>/` — e.g. `/api/directors/christopher-nolan/`

### Genres — `GET /api/genres/`

Returns all genres with their movie count.

### Reviews (nested under movie)

```
GET  /api/movies/<movie-slug>/reviews/
POST /api/movies/<movie-slug>/reviews/
```

Body for POST: `{ "author_name": "...", "rating": 1–10, "comment": "..." }`

---

## Data Model

```
Genre  ←──────── Movie ──────────→ Director
                   │
                   ├──── M2M ────→ Actor
                   └──── FK  ────→ Review
```

- **Movie → Director**: many-to-one FK (nullable — a movie may have no known director)
- **Movie ↔ Genre**: many-to-many
- **Movie ↔ Actor**: many-to-many
- **Review → Movie**: many-to-one FK (cascade delete)
- **`average_rating`**: computed server-side via Django ORM `Avg` aggregation — no denormalized field

Every entity has a human-readable **slug** field (e.g. `inception-2010`, `christopher-nolan`) used in all detail URLs.

---

## Architecture

```
Browser
  │
  └─→ nginx :8080
          ├── /api/*                  → Django (gunicorn) :8000
          ├── /api/docs, /api/redoc   → Django (gunicorn) :8000
          └── /*                      → Vue SPA (index.html)
```

- **No client-side filtering.** All filter params are forwarded as query strings to Django.
- **Backend healthcheck** gates frontend container startup (no race-condition 502s).
- **Pinia store** manages favourites in memory; `localStorage` persists slugs across page reloads.

---

## Edge Cases

| Scenario                          | Behaviour                                         |
|-----------------------------------|---------------------------------------------------|
| No movies match filters           | `200 { count: 0, results: [] }` + empty-state UI  |
| Invalid filter value (non-integer)| django-filter ignores it → empty queryset, not 500|
| Movie / actor / director not found| `404` from DRF; frontend shows error message      |
| Actor with no movies              | Detail page shows "No movies found" empty state   |
| Favourites list empty             | FavoritesView shows a prompt to browse movies     |
| Backend not yet ready             | Docker healthcheck gates frontend startup         |
| Re-running seed                   | `update_or_create` — safe to run multiple times   |

---

## Bonus: Favourites / Watch Later

Click the ❤️ heart on any movie card (list or detail page). Favourites persist in `localStorage` under the key `movie-explorer-favorites` as a JSON array of movie slugs. No account required. Visit `/favorites` to see your saved list.

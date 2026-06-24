# Movie Explorer

Browse movies, actors, directors and genres. Filter by genre, director, year or search by title. Each movie has reviews and an average rating.

**Stack:** Django + DRF · Vue 3 + TypeScript · Tailwind · SQLite · Docker

---

## Running with Docker

```bash
git clone <repo-url>
cd move-villa
docker compose up --build
```

| | URL |
|---|---|
| App | http://localhost:8080 |
| API | http://localhost:8000/api/ |
| Swagger | http://localhost:8000/api/docs/ |

Build step runs lint + tests for both services. DB is seeded automatically on first start.

---

## Running locally

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py seed
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

---

## API filters

`GET /api/movies/` accepts:

| param | example |
|---|---|
| `search` | `?search=inception` |
| `genre_slug` | `?genre_slug=action` |
| `director_slug` | `?director_slug=christopher-nolan` |
| `release_year` | `?release_year=2010` |
| `year_min` / `year_max` | `?year_min=2000&year_max=2010` |

`GET /api/actors/` accepts `?movie=<id>` and `?genre=<id>`

Full docs at `/api/docs/`

---

## Tests & lint

```bash
# backend
ruff check . && pytest

# frontend
npm run lint && npm run test:run
```

---

## Bonus

Favourites are saved to `localStorage` — no login needed. Click ❤️ on any movie card.

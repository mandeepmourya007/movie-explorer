import pytest
from rest_framework.test import APIClient

from catalog.models import Actor, Director, Genre, Movie, Review


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_data(db):
    """Shared fixture: creates a small but complete dataset."""
    genre_action = Genre.objects.create(name="Action", slug="action")
    genre_drama = Genre.objects.create(name="Drama", slug="drama")
    director_a = Director.objects.create(name="Director A", slug="director-a")
    director_b = Director.objects.create(name="Director B", slug="director-b")
    actor_x = Actor.objects.create(name="Actor X", slug="actor-x")
    actor_y = Actor.objects.create(name="Actor Y", slug="actor-y")

    movie1 = Movie.objects.create(
        title="Alpha Film", slug="alpha-film-2010", release_year=2010, director=director_a
    )
    movie1.genres.add(genre_action)
    movie1.actors.add(actor_x)

    movie2 = Movie.objects.create(
        title="Beta Film", slug="beta-film-2020", release_year=2020, director=director_b
    )
    movie2.genres.add(genre_drama)
    movie2.actors.add(actor_y)

    Review.objects.create(movie=movie1, author_name="Tester", rating=8)

    return {
        "genre_action": genre_action,
        "genre_drama": genre_drama,
        "director_a": director_a,
        "director_b": director_b,
        "actor_x": actor_x,
        "actor_y": actor_y,
        "movie1": movie1,
        "movie2": movie2,
    }


# ---------------------------------------------------------------------------
# Movies list + detail
# ---------------------------------------------------------------------------


class TestMovieList:
    def test_list_returns_200(self, client, sample_data):
        response = client.get("/api/movies/")
        assert response.status_code == 200

    def test_list_contains_expected_fields(self, client, sample_data):
        response = client.get("/api/movies/")
        result = response.json()["results"][0]
        for field in ("id", "slug", "title", "release_year", "genres", "director", "average_rating"):
            assert field in result

    def test_empty_list_returns_200_with_empty_results(self, client, db):
        response = client.get("/api/movies/")
        assert response.status_code == 200
        assert response.json()["results"] == []

    def test_detail_returns_200(self, client, sample_data):
        movie = sample_data["movie1"]
        response = client.get(f"/api/movies/{movie.slug}/")
        assert response.status_code == 200

    def test_detail_contains_reviews(self, client, sample_data):
        movie = sample_data["movie1"]
        response = client.get(f"/api/movies/{movie.slug}/")
        data = response.json()
        assert "reviews" in data
        assert len(data["reviews"]) == 1

    def test_detail_404_for_unknown_slug(self, client, db):
        response = client.get("/api/movies/nonexistent-movie-9999/")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Movie filters — backend only
# ---------------------------------------------------------------------------


class TestMovieFilters:
    def test_filter_by_genre_id(self, client, sample_data):
        genre_id = sample_data["genre_action"].id
        response = client.get(f"/api/movies/?genre={genre_id}")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Alpha Film"

    def test_filter_by_genre_name(self, client, sample_data):
        response = client.get("/api/movies/?genre_name=drama")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Beta Film"

    def test_filter_by_director_id(self, client, sample_data):
        dir_id = sample_data["director_b"].id
        response = client.get(f"/api/movies/?director={dir_id}")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Beta Film"

    def test_filter_by_actor_id(self, client, sample_data):
        actor_id = sample_data["actor_x"].id
        response = client.get(f"/api/movies/?actor={actor_id}")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Alpha Film"

    def test_filter_by_release_year(self, client, sample_data):
        response = client.get("/api/movies/?release_year=2010")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["release_year"] == 2010

    def test_filter_by_year_range(self, client, sample_data):
        response = client.get("/api/movies/?year_min=2015&year_max=2025")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Beta Film"

    def test_filter_no_match_returns_empty(self, client, sample_data):
        response = client.get("/api/movies/?release_year=1800")
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []

    def test_search_by_title(self, client, sample_data):
        response = client.get("/api/movies/?search=Alpha")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["title"] == "Alpha Film"


# ---------------------------------------------------------------------------
# Actor filters
# ---------------------------------------------------------------------------


class TestActorFilters:
    def test_filter_actors_by_movie_id(self, client, sample_data):
        movie_id = sample_data["movie1"].id
        response = client.get(f"/api/actors/?movie={movie_id}")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["name"] == "Actor X"

    def test_filter_actors_by_genre_id(self, client, sample_data):
        genre_id = sample_data["genre_drama"].id
        response = client.get(f"/api/actors/?genre={genre_id}")
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["name"] == "Actor Y"


# ---------------------------------------------------------------------------
# Genres & Directors
# ---------------------------------------------------------------------------


class TestGenreEndpoints:
    def test_genre_list(self, client, sample_data):
        response = client.get("/api/genres/")
        assert response.status_code == 200
        assert response.json()["count"] >= 2

    def test_genre_detail_404(self, client, db):
        response = client.get("/api/genres/nonexistent-genre/")
        assert response.status_code == 404


class TestDirectorEndpoints:
    def test_director_detail_includes_movies(self, client, sample_data):
        director = sample_data["director_a"]
        response = client.get(f"/api/directors/{director.slug}/")
        data = response.json()
        assert "movies" in data
        assert len(data["movies"]) == 1

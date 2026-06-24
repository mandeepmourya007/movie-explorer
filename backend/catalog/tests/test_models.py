"""Unit tests for catalog models."""
import pytest

from catalog.models import Actor, Director, Genre, Movie, Review


@pytest.mark.django_db
class TestMovieAverageRating:
    """Tests for Movie.average_rating computed property."""

    def setup_method(self):
        self.genre = Genre.objects.create(name="Drama", slug="drama")
        self.director = Director.objects.create(name="Test Director", slug="test-director")
        self.movie = Movie.objects.create(
            title="Test Movie", slug="test-movie-2020", release_year=2020, director=self.director
        )

    def test_no_reviews_returns_none(self):
        assert self.movie.average_rating is None

    def test_single_review(self):
        Review.objects.create(movie=self.movie, author_name="Alice", rating=8)
        assert self.movie.average_rating == 8.0

    def test_multiple_reviews_rounds_to_one_decimal(self):
        Review.objects.create(movie=self.movie, author_name="Alice", rating=7)
        Review.objects.create(movie=self.movie, author_name="Bob", rating=9)
        assert self.movie.average_rating == 8.0

    def test_average_rating_rounds_correctly(self):
        for rating in [7, 8, 9]:
            Review.objects.create(movie=self.movie, author_name="Reviewer", rating=rating)
        assert self.movie.average_rating == 8.0


@pytest.mark.django_db
class TestMovieRelationships:
    def test_movie_can_have_multiple_genres(self):
        g1 = Genre.objects.create(name="Action", slug="action")
        g2 = Genre.objects.create(name="Thriller", slug="thriller")
        movie = Movie.objects.create(title="Film", slug="film-2022", release_year=2022)
        movie.genres.set([g1, g2])
        assert movie.genres.count() == 2

    def test_movie_can_have_multiple_actors(self):
        a1 = Actor.objects.create(name="Actor One", slug="actor-one")
        a2 = Actor.objects.create(name="Actor Two", slug="actor-two")
        movie = Movie.objects.create(title="Film", slug="film-2022b", release_year=2022)
        movie.actors.set([a1, a2])
        assert movie.actors.count() == 2

    def test_movie_has_single_director(self):
        director = Director.objects.create(name="Dir", slug="dir")
        movie = Movie.objects.create(title="Film", slug="film-2022c", release_year=2022, director=director)
        assert movie.director == director

    def test_movie_director_nullable(self):
        movie = Movie.objects.create(title="Film", slug="film-2022d", release_year=2022)
        assert movie.director is None

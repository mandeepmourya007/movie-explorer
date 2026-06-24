"""
Catalog models for Movie Explorer.

Entity relationships:
  Movie --< Genre  (M2M)
  Movie --< Actor  (M2M)
  Movie --> Director (FK, nullable)
  Movie --< Review (FK)
"""
from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PersonMixin(models.Model):
    """Abstract base for person entities (Actor, Director) sharing common fields."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo_url = models.URLField(max_length=500, blank=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """A film genre, e.g. Action, Drama, Comedy."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Director(PersonMixin):
    """A film director."""


class Actor(PersonMixin):
    """An actor who appears in movies."""


class Movie(models.Model):
    """
    A film title with its core metadata.

    Relationships:
      - director: single FK (optional) — a movie may have no known director.
      - genres: M2M — a movie can span multiple genres.
      - actors: M2M — cast of the movie.
    """

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    release_year = models.PositiveSmallIntegerField(db_index=True)
    synopsis = models.TextField(blank=True)
    poster_url = models.URLField(max_length=500, blank=True)
    director = models.ForeignKey(
        Director,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movies",
    )
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    class Meta:
        ordering = ["-release_year", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"

    @property
    def average_rating(self) -> float | None:
        from django.db.models import Avg

        result = self.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(result, 1) if result is not None else None


class Review(models.Model):
    """A user review (mock/seed data) for a movie."""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.author_name} → {self.movie.title} ({self.rating}/10)"

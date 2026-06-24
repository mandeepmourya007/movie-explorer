"""
Serializers for the Movie Explorer catalog.

Pattern:
  - Lightweight nested serializers for reading (id + name + photo).
  - List serializers expose minimal fields for browse views (performance).
  - Detail serializers expose full relationships for single-object views.
  - Write operations use PrimaryKeyRelatedField so FK/M2M updates stay trivial.
"""
from rest_framework import serializers

from .models import Actor, Director, Genre, Movie, Review

# ---------------------------------------------------------------------------
# Nested read-only serializers (used inside other serializers)
# ---------------------------------------------------------------------------


class GenreMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "slug", "name"]


class DirectorMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "slug", "name", "photo_url"]


class ActorMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "slug", "name", "photo_url"]


# ---------------------------------------------------------------------------
# Review
# ---------------------------------------------------------------------------


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author_name", "rating", "comment", "created_at"]
        read_only_fields = ["created_at"]


# ---------------------------------------------------------------------------
# Movie — split list vs detail for performance
# ---------------------------------------------------------------------------


class MovieListSerializer(serializers.ModelSerializer):
    """Compact representation for movie browse/list views."""

    genres = GenreMinimalSerializer(many=True, read_only=True)
    director = DirectorMinimalSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "slug", "title", "release_year", "poster_url", "genres", "director", "average_rating"]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Full representation for single-movie views, including cast and reviews."""

    genres = GenreMinimalSerializer(many=True, read_only=True)
    director = DirectorMinimalSerializer(read_only=True)
    actors = ActorMinimalSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "slug",
            "title",
            "release_year",
            "synopsis",
            "poster_url",
            "director",
            "genres",
            "actors",
            "reviews",
            "average_rating",
        ]


class MovieWriteSerializer(serializers.ModelSerializer):
    """Used for POST/PUT/PATCH — accepts ids for FK/M2M fields."""

    director = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), allow_null=True, required=False
    )
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)
    actors = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True, required=False)

    class Meta:
        model = Movie
        fields = ["id", "slug", "title", "release_year", "synopsis", "poster_url", "director", "genres", "actors"]


# ---------------------------------------------------------------------------
# Actor — split list vs detail
# ---------------------------------------------------------------------------


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "slug", "name", "photo_url"]


class ActorDetailSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ["id", "slug", "name", "bio", "birth_date", "photo_url", "movies"]


# ---------------------------------------------------------------------------
# Director — split list vs detail
# ---------------------------------------------------------------------------


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "slug", "name", "photo_url"]


class DirectorDetailSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ["id", "slug", "name", "bio", "birth_date", "photo_url", "movies"]


# ---------------------------------------------------------------------------
# Genre
# ---------------------------------------------------------------------------


class GenreSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["id", "slug", "name", "movie_count"]

    def get_movie_count(self, obj: Genre) -> int:  # noqa: D401
        return obj.movies.count()

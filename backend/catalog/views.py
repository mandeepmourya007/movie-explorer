"""
ViewSets for the Movie Explorer catalog.

Each entity gets a ModelViewSet.  List/detail serializer switching is done
in get_serializer_class() — a DRY pattern that avoids duplicate viewsets.

Querysets use select_related / prefetch_related to prevent N+1 queries.
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .filters import ActorFilter, MovieFilter
from .models import Actor, Director, Genre, Movie, Review
from .serializers import (
    ActorDetailSerializer,
    ActorListSerializer,
    DirectorDetailSerializer,
    DirectorListSerializer,
    GenreSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    MovieWriteSerializer,
    ReviewSerializer,
)

# Actions that return a single object
_DETAIL_ACTIONS = {"retrieve", "create", "update", "partial_update"}


class MovieViewSet(ModelViewSet):
    """
    CRUD + filtering for movies.

    Filters: genre, genre_name, director, actor, release_year, year_min, year_max
    Search:  ?search=<title substring>
    Order:   ?ordering=release_year | title | -release_year | -title
    """

    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ["title"]
    ordering_fields = ["release_year", "title"]
    ordering = ["-release_year"]

    def get_queryset(self):
        qs = Movie.objects.select_related("director").prefetch_related(
            "genres", "actors", "reviews"
        )
        # .distinct() avoids duplicate rows from M2M joins when filtering
        return qs.distinct()

    def get_serializer_class(self):
        if self.action in _DETAIL_ACTIONS:
            if self.request.method in ("POST", "PUT", "PATCH"):
                return MovieWriteSerializer
            return MovieDetailSerializer
        return MovieListSerializer


class ActorViewSet(ModelViewSet):
    """
    CRUD + filtering for actors.

    Filters: movie (id), genre (id)
    Search:  ?search=<name substring>
    """

    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ActorFilter
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return Actor.objects.prefetch_related("movies__genres").distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorListSerializer


class DirectorViewSet(ModelViewSet):
    """
    CRUD + filtering for directors.

    Search: ?search=<name substring>
    """

    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return Director.objects.prefetch_related("movies__genres").distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DirectorDetailSerializer
        return DirectorListSerializer


class GenreViewSet(ModelViewSet):
    """CRUD for genres."""

    lookup_field = "slug"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class ReviewViewSet(ModelViewSet):
    """Reviews nested under /movies/<movie_slug>/reviews/."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(movie__slug=self.kwargs["movie_slug"])

    def perform_create(self, serializer):
        movie = Movie.objects.get(slug=self.kwargs["movie_slug"])
        serializer.save(movie=movie)

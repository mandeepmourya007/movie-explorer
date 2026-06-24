"""
URL routing for the catalog API.

DefaultRouter registers standard CRUD routes automatically.
Reviews are nested under /movies/<movie_pk>/reviews/ via manual path entries
(avoids adding drf-nested-routers as an extra dependency — KISS).
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActorViewSet, DirectorViewSet, GenreViewSet, MovieViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"actors", ActorViewSet, basename="actor")
router.register(r"directors", DirectorViewSet, basename="director")
router.register(r"genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("", include(router.urls)),
    # Nested reviews under a movie (keyed by movie slug)
    path(
        "movies/<slug:movie_slug>/reviews/",
        ReviewViewSet.as_view({"get": "list", "post": "create"}),
        name="movie-reviews-list",
    ),
    path(
        "movies/<slug:movie_slug>/reviews/<int:pk>/",
        ReviewViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
        name="movie-reviews-detail",
    ),
]

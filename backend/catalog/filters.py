"""
Django-filter FilterSets for the catalog API.

All filtering is performed here on the backend — the frontend sends query
params which are translated to queryset filters.
"""
import django_filters

from .models import Actor, Movie


class MovieFilter(django_filters.FilterSet):
    """
    Filter movies by:
      - genre       : exact genre id
      - genre_name  : case-insensitive genre name substring
      - director    : exact director id
      - actor       : exact actor id (movies containing this actor)
      - release_year: exact year
      - year_min / year_max: year range (inclusive)
    Search by title via DRF SearchFilter (search= param).
    """

    genre = django_filters.NumberFilter(field_name="genres__id", label="Genre ID")
    genre_name = django_filters.CharFilter(
        field_name="genres__name", lookup_expr="icontains", label="Genre name (partial)"
    )
    director = django_filters.NumberFilter(field_name="director__id", label="Director ID")
    actor = django_filters.NumberFilter(field_name="actors__id", label="Actor ID")
    release_year = django_filters.NumberFilter(label="Exact release year")
    year_min = django_filters.NumberFilter(field_name="release_year", lookup_expr="gte", label="Year >=")
    year_max = django_filters.NumberFilter(field_name="release_year", lookup_expr="lte", label="Year <=")

    class Meta:
        model = Movie
        fields = ["genre", "genre_name", "director", "actor", "release_year", "year_min", "year_max"]


class ActorFilter(django_filters.FilterSet):
    """
    Filter actors by:
      - movie : exact movie id (actors who appeared in this movie)
      - genre : exact genre id (actors whose movies belong to this genre)
    """

    movie = django_filters.NumberFilter(field_name="movies__id", label="Movie ID")
    genre = django_filters.NumberFilter(field_name="movies__genres__id", label="Genre ID")

    class Meta:
        model = Actor
        fields = ["movie", "genre"]

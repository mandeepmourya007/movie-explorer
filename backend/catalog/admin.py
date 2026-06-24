"""Django admin registration for the catalog app."""
from django.contrib import admin

from .models import Actor, Director, Genre, Movie, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]
    search_fields = ["name"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]
    search_fields = ["name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year", "director"]
    list_filter = ["release_year", "genres"]
    search_fields = ["title", "director__name"]
    filter_horizontal = ["genres", "actors"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["movie", "author_name", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["movie__title", "author_name"]

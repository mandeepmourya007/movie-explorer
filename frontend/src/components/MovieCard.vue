<!--
  MovieCard — compact card for a single movie shown in grid/list views.

  Props:
    movie — MovieList shape (id, title, release_year, poster_url, genres, director, average_rating)

  Clicking the card navigates to the movie detail page.
  The heart button toggles the movie in the Favorites store (localStorage).
-->
<template>
  <RouterLink
    :to="{ name: 'movie-detail', params: { slug: movie.slug } }"
    class="card flex flex-col hover:shadow-md transition-shadow no-underline text-gray-800"
  >
    <!-- Poster image -->
    <div class="bg-gray-100 aspect-[2/3] overflow-hidden relative">
      <img
        v-if="movie.poster_url"
        :src="movie.poster_url"
        :alt="movie.title"
        class="w-full h-full object-cover"
        loading="lazy"
      />
      <!-- Fallback when no poster URL -->
      <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-300">
        🎬
      </div>

      <!-- Favourite toggle -->
      <button
        class="absolute bottom-2 right-2 flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium shadow-md transition-all"
        :class="isFav
          ? 'bg-red-500 text-white hover:bg-red-600'
          : 'bg-white/90 text-gray-600 hover:bg-red-50 hover:text-red-500'"
        :title="isFav ? 'Remove from favourites' : 'Add to favourites'"
        @click.prevent="store.toggle(movie.slug)"
      >
        <span>{{ isFav ? '❤️' : '🤍' }}</span>
        <span>{{ isFav ? 'Saved' : 'Save' }}</span>
      </button>
    </div>

    <!-- Card body -->
    <div class="p-3 flex flex-col gap-1 flex-1">
      <h3 class="font-semibold text-sm leading-tight line-clamp-2">{{ movie.title }}</h3>

      <div class="flex items-center justify-between text-xs text-gray-500">
        <span>{{ movie.release_year }}</span>
        <RatingStars :rating="movie.average_rating" />
      </div>

      <p v-if="movie.director" class="text-xs text-gray-400 truncate">
        {{ movie.director.name }}
      </p>

      <!-- Genre badges -->
      <div class="flex flex-wrap gap-1 mt-auto pt-1">
        <span v-for="g in movie.genres.slice(0, 2)" :key="g.id" class="badge">
          {{ g.name }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MovieList } from '@/types'
import { useFavoritesStore } from '@/stores/favorites'
import RatingStars from './RatingStars.vue'

const props = defineProps<{ movie: MovieList }>()
const store = useFavoritesStore()
const isFav = computed(() => store.isFavorite(props.movie.slug))
</script>

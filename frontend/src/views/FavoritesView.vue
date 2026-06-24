<!--
  FavoritesView — shows all movies the user has bookmarked.
  Favourite IDs are stored in localStorage (no account needed).
  Re-fetches the latest movie data from the API on each visit.
-->
<template>
  <div class="page">
    <h1 class="text-2xl font-bold mb-1">Favourites</h1>
    <p class="text-sm text-gray-500 mb-6">Saved in your browser — no account needed.</p>

    <LoadingSpinner v-if="loading" />

    <!-- Empty state when no favourites saved -->
    <EmptyState
      v-else-if="store.count === 0"
      title="No favourites yet"
      description="Browse movies and click the ❤️ to save them here."
      icon="🤍"
    >
      <RouterLink to="/" class="btn-primary mt-4">Browse Movies</RouterLink>
    </EmptyState>

    <!-- Grid of favourited movies -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { fetchMoviesBySlugs } from '@/api/catalog'
import type { MovieList } from '@/types'
import { useFavoritesStore } from '@/stores/favorites'
import MovieCard from '@/components/MovieCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import EmptyState from '@/components/EmptyState.vue'

const store   = useFavoritesStore()
const movies  = ref<MovieList[]>([])
const loading = ref(false)

const load = async () => {
  if (!store.count) { movies.value = []; return }
  loading.value = true
  try {
    movies.value = await fetchMoviesBySlugs(store.allSlugs)
  } finally {
    loading.value = false
  }
}

// Reload if the user removes a favourite directly from this page
watch(() => store.allSlugs, load, { deep: true })

onMounted(load)
</script>

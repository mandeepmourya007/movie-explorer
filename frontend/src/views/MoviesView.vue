<!--
  MoviesView — the home page.
  Shows a search/filter bar at the top and a responsive grid of MovieCards below.
  All filtering is done on the backend (filters are sent as query params).
-->
<template>
  <div class="page">
    <h1 class="text-2xl font-bold mb-6">Movies</h1>

    <!-- Filter bar -->
    <FilterBar
      :model-value="filters"
      :genres="genres"
      :directors="directors"
      class="mb-6"
      @update:model-value="(val) => Object.assign(filters, val)"
    />

    <!-- Loading -->
    <LoadingSpinner v-if="loading" />

    <!-- Error -->
    <p v-else-if="error" class="text-center text-red-500 py-8">{{ error }}</p>

    <!-- Empty state -->
    <EmptyState
      v-else-if="movies.length === 0"
      title="No movies found"
      description="Try adjusting your search or filters."
      icon="🔍"
    />

    <!-- Results -->
    <template v-else>
      <p class="text-sm text-gray-500 mb-4">{{ total }} result{{ total !== 1 ? 's' : '' }}</p>

      <!-- Responsive grid — 2 cols on mobile, up to 5 on wide screens -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        <MovieCard v-for="movie in movies" :key="movie.id" :movie="movie" />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-8">
        <button
          class="btn-outline"
          :disabled="currentPage === 1"
          @click="goTo(currentPage - 1)"
        >
          ← Prev
        </button>
        <span class="text-sm text-gray-500">{{ currentPage }} / {{ totalPages }}</span>
        <button
          class="btn-outline"
          :disabled="currentPage === totalPages"
          @click="goTo(currentPage + 1)"
        >
          Next →
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { fetchDirectors, fetchGenres, fetchMovies } from '@/api/catalog'
import type { DirectorMinimal, Genre, MovieFilters, MovieList } from '@/types'
import FilterBar from '@/components/FilterBar.vue'
import MovieCard from '@/components/MovieCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import EmptyState from '@/components/EmptyState.vue'

const PAGE_SIZE = 12

const movies  = ref<MovieList[]>([])
const genres  = ref<Genre[]>([])
const directors = ref<DirectorMinimal[]>([])
const total   = ref(0)
const loading = ref(false)
const error   = ref<string | null>(null)
const filters = reactive<MovieFilters>({ page: 1 })

const currentPage = computed(() => filters.page ?? 1)
const totalPages  = computed(() => Math.ceil(total.value / PAGE_SIZE))

const load = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await fetchMovies(filters)
    movies.value = data.results
    total.value  = data.count
  } catch {
    error.value = 'Could not load movies. Is the backend running?'
  } finally {
    loading.value = false
  }
}

const goTo = (page: number) => { filters.page = page }

// Debounce so typing in the search box doesn't fire on every keystroke
let timer: ReturnType<typeof setTimeout>
watch(filters, () => { clearTimeout(timer); timer = setTimeout(load, 300) }, { deep: true })

onMounted(async () => {
  // Load dropdowns + first page of movies in parallel
  const [genreData, directorData] = await Promise.all([
    fetchGenres(),
    fetchDirectors({ page_size: 200 }),
  ])
  genres.value    = genreData.results
  directors.value = directorData.results
  await load()
})
</script>

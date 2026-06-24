<!--
  DirectorDetailView — profile page for a single director.
  Shows photo, name, bio, birth date, and their filmography as a MovieCard grid.
-->
<template>
  <div class="page">
    <LoadingSpinner v-if="loading" />

    <EmptyState v-else-if="error" :title="error" icon="🎬">
      <RouterLink to="/" class="btn-primary mt-4">← Home</RouterLink>
    </EmptyState>

    <template v-else-if="director">
      <RouterLink to="/" class="text-sm text-gray-500 hover:text-blue-600 no-underline mb-6 inline-block">
        ← Home
      </RouterLink>

      <!-- Profile header -->
      <div class="flex flex-col sm:flex-row gap-5 mt-4 items-start">
        <!-- Avatar -->
        <div class="w-28 h-28 rounded-full overflow-hidden bg-gray-200 flex-shrink-0">
          <img
            v-if="director.photo_url"
            :src="director.photo_url"
            :alt="director.name"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-4xl">🎬</div>
        </div>

        <!-- Info -->
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wide">Director</p>
          <h1 class="text-2xl font-bold mt-0.5">{{ director.name }}</h1>
          <p v-if="director.birth_date" class="text-sm text-gray-500 mt-1">Born: {{ director.birth_date }}</p>
          <p v-if="director.bio" class="text-sm text-gray-600 mt-3 max-w-xl leading-relaxed">{{ director.bio }}</p>
        </div>
      </div>

      <!-- Filmography -->
      <div class="mt-8">
        <h2 class="section-title">
          Filmography
          <span class="text-gray-400 font-normal text-base">({{ director.movies.length }})</span>
        </h2>

        <EmptyState v-if="!director.movies.length" title="No movies listed" icon="🎬" />

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <MovieCard v-for="movie in director.movies" :key="movie.id" :movie="movie" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchDirector } from '@/api/catalog'
import type { DirectorDetail } from '@/types'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import EmptyState from '@/components/EmptyState.vue'
import MovieCard from '@/components/MovieCard.vue'

const route     = useRoute()
const director  = ref<DirectorDetail | null>(null)
const loading   = ref(true)
const error     = ref<string | null>(null)

onMounted(async () => {
  try {
    director.value = await fetchDirector(route.params.slug as string)
  } catch {
    error.value = 'Director not found.'
  } finally {
    loading.value = false
  }
})
</script>

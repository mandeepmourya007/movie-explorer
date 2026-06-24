<!--
  ActorDetailView — profile page for a single actor.
  Shows photo, name, bio, birth date, and a grid of their movies.
-->
<template>
  <div class="page">
    <LoadingSpinner v-if="loading" />

    <EmptyState v-else-if="error" :title="error" icon="👤">
      <RouterLink to="/" class="btn-primary mt-4">← Home</RouterLink>
    </EmptyState>

    <template v-else-if="actor">
      <RouterLink to="/" class="text-sm text-gray-500 hover:text-blue-600 no-underline mb-6 inline-block">
        ← Home
      </RouterLink>

      <!-- Profile header -->
      <div class="flex flex-col sm:flex-row gap-5 mt-4 items-start">
        <!-- Avatar -->
        <div class="w-28 h-28 rounded-full overflow-hidden bg-gray-200 flex-shrink-0">
          <img
            v-if="actor.photo_url"
            :src="actor.photo_url"
            :alt="actor.name"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-4xl">👤</div>
        </div>

        <!-- Info -->
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wide">Actor</p>
          <h1 class="text-2xl font-bold mt-0.5">{{ actor.name }}</h1>
          <p v-if="actor.birth_date" class="text-sm text-gray-500 mt-1">Born: {{ actor.birth_date }}</p>
          <p v-if="actor.bio" class="text-sm text-gray-600 mt-3 max-w-xl leading-relaxed">{{ actor.bio }}</p>
        </div>
      </div>

      <!-- Filmography -->
      <div class="mt-8">
        <h2 class="section-title">
          Movies
          <span class="text-gray-400 font-normal text-base">({{ actor.movies.length }})</span>
        </h2>

        <EmptyState v-if="!actor.movies.length" title="No movies listed" icon="🎬" />

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <MovieCard v-for="movie in actor.movies" :key="movie.id" :movie="movie" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchActor } from '@/api/catalog'
import type { ActorDetail } from '@/types'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import EmptyState from '@/components/EmptyState.vue'
import MovieCard from '@/components/MovieCard.vue'

const route  = useRoute()
const actor  = ref<ActorDetail | null>(null)
const loading = ref(true)
const error   = ref<string | null>(null)

onMounted(async () => {
  try {
    actor.value = await fetchActor(route.params.slug as string)
  } catch {
    error.value = 'Actor not found.'
  } finally {
    loading.value = false
  }
})
</script>

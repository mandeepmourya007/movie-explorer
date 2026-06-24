<!--
  MovieDetailView — full detail page for a single movie.
  Shows poster, synopsis, director (linked), cast (linked), genres, reviews.
  Includes a favourites toggle button.
-->
<template>
  <div class="page">
    <LoadingSpinner v-if="loading" />

    <!-- Error / not found -->
    <EmptyState v-else-if="error" :title="error" icon="🎬">
      <RouterLink to="/" class="btn-primary mt-4">← Back to movies</RouterLink>
    </EmptyState>

    <template v-else-if="movie">
      <!-- Back link -->
      <RouterLink to="/" class="text-sm text-gray-500 hover:text-blue-600 no-underline mb-6 inline-block">
        ← All movies
      </RouterLink>

      <!-- Top section: poster + info side by side -->
      <div class="flex flex-col sm:flex-row gap-6 mt-4">

        <!-- Poster -->
        <div class="w-full sm:w-48 flex-shrink-0">
          <div class="card aspect-[2/3] overflow-hidden">
            <img
              v-if="movie.poster_url"
              :src="movie.poster_url"
              :alt="movie.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-5xl bg-gray-50">
              🎬
            </div>
          </div>

          <!-- Favourites button below poster -->
          <button
            class="w-full mt-2 py-2 text-sm rounded border transition-colors"
            :class="isFav
              ? 'border-red-300 text-red-500 bg-red-50 hover:bg-red-100'
              : 'border-gray-300 text-gray-600 hover:bg-gray-100'"
            @click="store.toggle(movie.slug)"
          >
            {{ isFav ? '❤️ In Favourites' : '🤍 Add to Favourites' }}
          </button>
        </div>

        <!-- Movie info -->
        <div class="flex-1">
          <h1 class="text-2xl font-bold">{{ movie.title }}</h1>

          <!-- Year + rating on the same line -->
          <div class="flex items-center gap-4 mt-1 text-sm text-gray-500">
            <span>{{ movie.release_year }}</span>
            <RatingStars :rating="movie.average_rating" />
          </div>

          <!-- Genres -->
          <div class="flex flex-wrap gap-2 mt-3">
            <span v-for="g in movie.genres" :key="g.id" class="badge">{{ g.name }}</span>
          </div>

          <!-- Synopsis -->
          <p v-if="movie.synopsis" class="mt-4 text-sm text-gray-600 leading-relaxed">
            {{ movie.synopsis }}
          </p>

          <!-- Director -->
          <div v-if="movie.director" class="mt-4">
            <p class="text-xs text-gray-400 uppercase tracking-wide mb-1">Director</p>
            <RouterLink
              :to="{ name: 'director-detail', params: { slug: movie.director.slug } }"
              class="flex items-center gap-2 w-fit no-underline hover:opacity-75"
            >
              <img
                v-if="movie.director.photo_url"
                :src="movie.director.photo_url"
                :alt="movie.director.name"
                class="w-9 h-9 rounded-full object-cover bg-gray-200"
              />
              <div v-else class="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center text-sm">
                👤
              </div>
              <span class="text-sm font-medium text-blue-600">{{ movie.director.name }}</span>
            </RouterLink>
          </div>

          <!-- Cast -->
          <div v-if="movie.actors.length" class="mt-4">
            <p class="text-xs text-gray-400 uppercase tracking-wide mb-2">Cast</p>
            <div class="flex flex-wrap gap-3">
              <RouterLink
                v-for="actor in movie.actors"
                :key="actor.id"
                :to="{ name: 'actor-detail', params: { slug: actor.slug } }"
                class="flex flex-col items-center gap-1 no-underline hover:opacity-75"
              >
                <img
                  v-if="actor.photo_url"
                  :src="actor.photo_url"
                  :alt="actor.name"
                  class="w-12 h-12 rounded-full object-cover bg-gray-200"
                />
                <div v-else class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center text-lg">
                  👤
                </div>
                <span class="text-xs text-center text-gray-600 max-w-[4rem] truncate">{{ actor.name }}</span>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews section -->
      <section class="mt-10">
        <h2 class="section-title">
          Reviews
          <span class="text-gray-400 font-normal text-base">({{ movie.reviews.length }})</span>
        </h2>

        <EmptyState v-if="!movie.reviews.length" title="No reviews yet" icon="💬" />

        <div v-else class="space-y-3">
          <div
            v-for="review in movie.reviews"
            :key="review.id"
            class="card p-4"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="font-medium text-sm">{{ review.author_name }}</span>
              <RatingStars :rating="review.rating" />
            </div>
            <p class="text-sm text-gray-600">{{ review.comment }}</p>
            <p class="text-xs text-gray-400 mt-2">
              {{ new Date(review.created_at).toLocaleDateString() }}
            </p>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchMovie } from '@/api/catalog'
import type { MovieDetail } from '@/types'
import { useFavoritesStore } from '@/stores/favorites'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import EmptyState from '@/components/EmptyState.vue'
import RatingStars from '@/components/RatingStars.vue'

const route = useRoute()
const store = useFavoritesStore()

const movie   = ref<MovieDetail | null>(null)
const loading = ref(true)
const error   = ref<string | null>(null)

const isFav = computed(() => movie.value ? store.isFavorite(movie.value.slug) : false)

onMounted(async () => {
  try {
    movie.value = await fetchMovie(route.params.slug as string)
  } catch {
    error.value = 'Movie not found.'
  } finally {
    loading.value = false
  }
})
</script>

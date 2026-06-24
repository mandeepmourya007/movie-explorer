<!--
  NavBar — top navigation bar.
  Shows app name, page links, and a favorites badge.
-->
<template>
  <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">

      <!-- Logo / Home link -->
      <RouterLink to="/" class="text-blue-600 font-bold text-lg no-underline">
        🎬 Movie Explorer
      </RouterLink>

      <!-- Nav links -->
      <nav class="flex items-center gap-4 text-sm">
        <RouterLink
          to="/"
          class="text-gray-600 hover:text-blue-600 no-underline"
          :class="{ 'text-blue-600 font-medium': $route.name === 'movies' }"
        >
          Movies
        </RouterLink>

        <RouterLink
          to="/favorites"
          class="flex items-center gap-1 text-gray-600 hover:text-blue-600 no-underline"
          :class="{ 'text-blue-600 font-medium': $route.name === 'favorites' }"
        >
          Favorites
          <!-- Badge shows count when favourites exist -->
          <span
            v-if="favCount > 0"
            class="bg-blue-600 text-white text-xs rounded-full px-1.5 py-0.5 leading-none"
          >
            {{ favCount }}
          </span>
        </RouterLink>
      </nav>

    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFavoritesStore } from '@/stores/favorites'

const store = useFavoritesStore()
const favCount = computed(() => store.count)
</script>

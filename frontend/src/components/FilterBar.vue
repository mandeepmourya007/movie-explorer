<template>
  <div class="card p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">

      <!-- Search by title -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Search</label>
        <input
          v-model="local.search"
          type="text"
          placeholder="Movie title..."
          class="form-control"
          @input="emit"
        />
      </div>

      <!-- Filter by genre (slug) -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Genre</label>
        <select v-model="local.genre_slug" class="form-control" @change="emit">
          <option :value="undefined">All genres</option>
          <option v-for="g in genres" :key="g.slug" :value="g.slug">{{ g.name }}</option>
        </select>
      </div>

      <!-- Filter by director (slug) -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Director</label>
        <select v-model="local.director_slug" class="form-control" @change="emit">
          <option :value="undefined">All directors</option>
          <option v-for="d in directors" :key="d.slug" :value="d.slug">{{ d.name }}</option>
        </select>
      </div>

      <!-- Filter by year -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Year</label>
        <select v-model.number="local.release_year" class="form-control" @change="emit">
          <option :value="undefined">All years</option>
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

    </div>

    <!-- Clear filters link -->
    <div class="mt-2 text-right">
      <button
        v-if="hasFilters"
        class="text-xs text-gray-400 hover:text-red-500 transition-colors"
        @click="clear"
      >
        ✕ Clear filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import type { DirectorMinimal, Genre, MovieFilters } from '@/types'

const props = defineProps<{
  modelValue: MovieFilters
  genres: Genre[]
  directors: DirectorMinimal[]
}>()

const emits = defineEmits<{ 'update:modelValue': [MovieFilters] }>()

const currentYear = new Date().getFullYear()
const years = Array.from({ length: currentYear - 1989 }, (_, i) => currentYear - i)

const local = reactive<MovieFilters>({ ...props.modelValue })

watch(() => props.modelValue, (v) => Object.assign(local, v), { deep: true })

const hasFilters = computed(
  () => !!local.search || !!local.genre_slug || !!local.director_slug || !!local.release_year
)

const emit = () => emits('update:modelValue', { ...local, page: 1 })

const clear = () => {
  Object.assign(local, { search: undefined, genre_slug: undefined, director_slug: undefined, release_year: undefined })
  emit()
}
</script>

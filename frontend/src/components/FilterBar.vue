<!--
  FilterBar — search and filter controls for the movies list.

  Props (v-model):
    modelValue — MovieFilters object (search, genre, director, release_year)
    genres     — list of Genre options for the dropdown
    directors  — list of DirectorMinimal options for the dropdown

  Emits update:modelValue whenever any control changes.
  All filtering happens on the backend — this component only sends query params.
-->
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

      <!-- Filter by genre -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Genre</label>
        <select v-model="local.genre" class="form-control" @change="emit">
          <option :value="undefined">All genres</option>
          <option v-for="g in genres" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>

      <!-- Filter by director -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Director</label>
        <select v-model="local.director" class="form-control" @change="emit">
          <option :value="undefined">All directors</option>
          <option v-for="d in directors" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>
      </div>

      <!-- Filter by year -->
      <div>
        <label class="block text-xs text-gray-500 mb-1">Year</label>
        <input
          v-model.number="local.release_year"
          type="number"
          placeholder="e.g. 2023"
          min="1900"
          :max="new Date().getFullYear()"
          class="form-control"
          @input="emit"
        />
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

// Local copy — avoids re-rendering parent on every keystroke
const local = reactive<MovieFilters>({ ...props.modelValue })

// Keep local in sync if parent resets filters externally
watch(() => props.modelValue, (v) => Object.assign(local, v), { deep: true })

const hasFilters = computed(
  () => !!local.search || !!local.genre || !!local.director || !!local.release_year
)

const emit = () => emits('update:modelValue', { ...local, page: 1 })

const clear = () => {
  Object.assign(local, { search: undefined, genre: undefined, director: undefined, release_year: undefined })
  emit()
}
</script>

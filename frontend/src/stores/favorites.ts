import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const STORAGE_KEY = 'movie-explorer-favorites'
const STORAGE_VERSION = 'v2' // bump when storage schema changes (clears stale data)
const VERSION_KEY = 'movie-explorer-favorites-version'

const loadFromStorage = (): Set<string> => {
  try {
    // Clear stale data from older versions (e.g. numeric IDs stored before slug migration)
    if (localStorage.getItem(VERSION_KEY) !== STORAGE_VERSION) {
      localStorage.removeItem(STORAGE_KEY)
      localStorage.setItem(VERSION_KEY, STORAGE_VERSION)
      return new Set()
    }
    const raw = localStorage.getItem(STORAGE_KEY)
    const parsed: string[] = raw ? JSON.parse(raw) : []
    // Guard: drop any non-string entries left from old format
    return new Set(parsed.filter((v) => typeof v === 'string' && v.includes('-')))
  } catch {
    return new Set()
  }
}

const saveToStorage = (slugs: Set<string>): void => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify([...slugs]))
}

export const useFavoritesStore = defineStore('favorites', () => {
  const slugs = ref<Set<string>>(loadFromStorage())

  const count = computed(() => slugs.value.size)

  const isFavorite = (slug: string): boolean => slugs.value.has(slug)

  const toggle = (slug: string): void => {
    const updated = new Set(slugs.value)
    if (updated.has(slug)) {
      updated.delete(slug)
    } else {
      updated.add(slug)
    }
    slugs.value = updated
    saveToStorage(updated)
  }

  const add = (slug: string): void => {
    if (!slugs.value.has(slug)) {
      const updated = new Set(slugs.value)
      updated.add(slug)
      slugs.value = updated
      saveToStorage(updated)
    }
  }

  const remove = (slug: string): void => {
    if (slugs.value.has(slug)) {
      const updated = new Set(slugs.value)
      updated.delete(slug)
      slugs.value = updated
      saveToStorage(updated)
    }
  }

  const allSlugs = computed((): string[] => [...slugs.value])

  return { slugs, count, isFavorite, toggle, add, remove, allSlugs }
})

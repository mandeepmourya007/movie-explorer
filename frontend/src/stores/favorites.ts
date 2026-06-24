import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const STORAGE_KEY = 'movie-explorer-favorites'

const loadFromStorage = (): Set<string> => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const parsed: string[] = raw ? JSON.parse(raw) : []
    return new Set(parsed)
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

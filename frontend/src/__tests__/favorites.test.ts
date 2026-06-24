import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useFavoritesStore } from '@/stores/favorites'

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] ?? null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

vi.stubGlobal('localStorage', localStorageMock)

describe('useFavoritesStore', () => {
  beforeEach(() => {
    localStorageMock.clear()
    setActivePinia(createPinia())
  })

  it('starts empty', () => {
    const store = useFavoritesStore()
    expect(store.count).toBe(0)
    expect(store.allSlugs).toEqual([])
  })

  it('adds a movie to favorites', () => {
    const store = useFavoritesStore()
    store.add('inception-2010')
    expect(store.isFavorite('inception-2010')).toBe(true)
    expect(store.count).toBe(1)
  })

  it('removes a movie from favorites', () => {
    const store = useFavoritesStore()
    store.add('inception-2010')
    store.remove('inception-2010')
    expect(store.isFavorite('inception-2010')).toBe(false)
    expect(store.count).toBe(0)
  })

  it('toggle adds when not present', () => {
    const store = useFavoritesStore()
    store.toggle('dune-2021')
    expect(store.isFavorite('dune-2021')).toBe(true)
  })

  it('toggle removes when present', () => {
    const store = useFavoritesStore()
    store.add('dune-2021')
    store.toggle('dune-2021')
    expect(store.isFavorite('dune-2021')).toBe(false)
  })

  it('does not add duplicates', () => {
    const store = useFavoritesStore()
    store.add('barbie-2023')
    store.add('barbie-2023')
    expect(store.count).toBe(1)
  })

  it('persists to localStorage on add', () => {
    const store = useFavoritesStore()
    store.add('titanic-1997')
    const stored = JSON.parse(localStorageMock.getItem('movie-explorer-favorites') ?? '[]')
    expect(stored).toContain('titanic-1997')
  })

  it('persists to localStorage on remove', () => {
    const store = useFavoritesStore()
    store.add('inception-2010')
    store.add('barbie-2023')
    store.remove('inception-2010')
    const stored = JSON.parse(localStorageMock.getItem('movie-explorer-favorites') ?? '[]')
    expect(stored).not.toContain('inception-2010')
    expect(stored).toContain('barbie-2023')
  })
})

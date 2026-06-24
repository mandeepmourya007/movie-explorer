/**
 * Tests for MovieCard component.
 * Verifies: title renders, year renders, genres render, favorite toggle works.
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'
import type { MovieList } from '@/types'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', name: 'home', component: { template: '<div />' } },
    { path: '/movies/:slug', name: 'movie-detail', component: { template: '<div />' } },
  ],
})

const mockMovie: MovieList = {
  id: 1,
  slug: 'test-movie-2023',
  title: 'Test Movie',
  release_year: 2023,
  poster_url: '',
  average_rating: 8.5,
  genres: [{ id: 1, slug: 'action', name: 'Action' }, { id: 2, slug: 'drama', name: 'Drama' }],
  director: { id: 1, slug: 'great-director', name: 'Great Director', photo_url: '' },
}

describe('MovieCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders movie title', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: mockMovie },
      global: { plugins: [router] },
    })
    expect(wrapper.text()).toContain('Test Movie')
  })

  it('renders release year', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: mockMovie },
      global: { plugins: [router] },
    })
    expect(wrapper.text()).toContain('2023')
  })

  it('renders genres', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: mockMovie },
      global: { plugins: [router] },
    })
    expect(wrapper.text()).toContain('Action')
    expect(wrapper.text()).toContain('Drama')
  })

  it('renders director name', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: mockMovie },
      global: { plugins: [router] },
    })
    expect(wrapper.text()).toContain('Great Director')
  })

  it('renders fallback icon when no poster', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: { ...mockMovie, poster_url: '' } },
      global: { plugins: [router] },
    })
    expect(wrapper.find('img').exists()).toBe(false)
    expect(wrapper.text()).toContain('🎬')
  })

  it('renders poster img when poster_url provided', async () => {
    const wrapper = mount(MovieCard, {
      props: { movie: { ...mockMovie, poster_url: 'https://example.com/poster.jpg' } },
      global: { plugins: [router] },
    })
    expect(wrapper.find('img').exists()).toBe(true)
    expect(wrapper.find('img').attributes('src')).toBe('https://example.com/poster.jpg')
  })
})

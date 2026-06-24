/**
 * Tests for FilterBar component.
 * Verifies: renders genre/director options, search input, emits on change, clear button.
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import FilterBar from '@/components/FilterBar.vue'
import type { Genre, DirectorMinimal, MovieFilters } from '@/types'

const genres: Genre[] = [
  { id: 1, name: 'Action' },
  { id: 2, name: 'Drama' },
]

const directors: DirectorMinimal[] = [
  { id: 1, name: 'Director One', photo_url: '' },
  { id: 2, name: 'Director Two', photo_url: '' },
]

const emptyFilters: MovieFilters = {}

describe('FilterBar', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders genre options', () => {
    const wrapper = mount(FilterBar, {
      props: { genres, directors, modelValue: emptyFilters },
    })
    const options = wrapper.find('select').findAll('option')
    expect(options.some((o) => o.text() === 'Action')).toBe(true)
    expect(options.some((o) => o.text() === 'Drama')).toBe(true)
  })

  it('renders director options', () => {
    const wrapper = mount(FilterBar, {
      props: { genres, directors, modelValue: emptyFilters },
    })
    const selects = wrapper.findAll('select')
    const directorSelect = selects[1]
    expect(directorSelect.text()).toContain('Director One')
    expect(directorSelect.text()).toContain('Director Two')
  })

  it('does not show clear button when no active filters', () => {
    const wrapper = mount(FilterBar, {
      props: { genres, directors, modelValue: emptyFilters },
    })
    expect(wrapper.text()).not.toContain('Clear filters')
  })

  it('shows clear button when filters are active', async () => {
    const wrapper = mount(FilterBar, {
      props: { genres, directors, modelValue: { search: 'test' } },
    })
    expect(wrapper.text()).toContain('Clear filters')
  })

  it('emits update:modelValue on search input', async () => {
    const wrapper = mount(FilterBar, {
      props: { genres, directors, modelValue: emptyFilters },
    })
    const input = wrapper.find('input[type="text"]')
    await input.setValue('Inception')
    const emitted = wrapper.emitted('update:modelValue')
    expect(emitted).toBeTruthy()
    expect((emitted?.[0]?.[0] as MovieFilters).search).toBe('Inception')
  })
})

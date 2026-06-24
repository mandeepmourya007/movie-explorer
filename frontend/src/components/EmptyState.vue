<!--
  EmptyState — shown when a list has no results.

  Props:
    title       — main message
    description — optional sub-text
    icon        — emoji or character shown above the title

  Slot: optional action (e.g. a back-link button)

  Usage:
    <EmptyState title="No movies found" description="Try different filters." icon="🔍" />
-->
<template>
  <div class="text-center py-16 text-gray-500">
    <p class="text-4xl mb-3">{{ icon }}</p>
    <p class="text-lg font-medium text-gray-600">{{ title }}</p>
    <p v-if="description" class="mt-1 text-sm">{{ description }}</p>
    <div class="mt-4">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    description?: string
    icon?: string
  }>(),
  { icon: '🎬', description: '' }
)
</script>

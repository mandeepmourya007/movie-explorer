<!--
  RatingStars — displays a numeric rating out of 10.

  Props:
    rating — number | null  (null shows a dash)

  Usage:
    <RatingStars :rating="movie.average_rating" />
-->
<template>
  <span class="inline-flex items-center gap-1 text-sm text-yellow-500 font-medium">
    ★ {{ rating !== null ? rating.toFixed(1) : '—' }}
    <span class="text-gray-400 font-normal">/10</span>
  </span>
</template>

<script setup lang="ts">
defineProps<{ rating: number | null }>()
</script>

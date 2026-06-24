<template>
  <div class="min-h-screen flex flex-col">
    <NavBar />

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="border-t border-gray-200 bg-white text-center text-sm text-gray-400 py-4">
      Movie Explorer — Made with Love
    </footer>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

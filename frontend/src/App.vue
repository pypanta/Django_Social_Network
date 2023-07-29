<template>
  <Nav />

  <main>
    <!-- https://stackoverflow.com/a/65064827 -->
    <RouterView :key="$route.fullPath" />
  </main>
</template>

<script setup>
import Nav from '@/components/Nav.vue'
</script>

<style scoped>
</style>

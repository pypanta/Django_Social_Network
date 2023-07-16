<template>
  <main>
    <p v-if="isAuthenticated">{{ message }}</p>
    <p v-else>
      {{ message }}. Please
      <router-link :to="{name: 'login'}">log in.</router-link>
    </p>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'

const store = useUserStore()
const { isAuthenticated, message, userData } = storeToRefs(store)
</script>

<template>
  <div v-if="store.isVisible" :class="store.classes" class="message">
    {{ store.message }}
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'

const store = useToastStore()
</script>

<style scoped>
.message {
  position: absolute;
  bottom: 20px;
  right: 20px;
  padding: 20px;
  color: #fff;
  border-radius: 5px;
}

.message-success {
  background-color: hsl(140, 100%, 35%);
}

.message-danger {
  background-color: hsl(12, 100%, 45%);
}
</style>

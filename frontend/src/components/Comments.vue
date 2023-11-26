<template>
  <div v-for="comment in comments" class="comments">
    <section class="status-post-info">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
      <p class="status-post-info-name">{{ filterUsername(comment.created_by) }}</p>
      <p class="status-post-info-time">{{ comment.time_ago }} ago.</p>
    </section>
    <section class="status-post-body">
      <p>{{ comment.body }}</p>
    </section>
    <!-- TODO
    <footer class="status-post-footer">
    </footer>
    -->
  </div>
</template>

<script setup>
import { filterUsername } from '@/utils/filters.js'
import userAvatar from "../assets/images/user-avatar.png"

const props = defineProps(['comments'])
</script>

<style scoped>
.comments {
  margin: var(--20px) 0 var(--20px) var(--20px);
  padding: var(--20px);
  background-color: hsl(0, 0%, 100%);
  border-radius: var(--10px);
}

.status-post-body {
  margin-top: var(--20px);
}
</style>

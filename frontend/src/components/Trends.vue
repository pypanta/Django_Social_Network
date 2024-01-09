<template>
  <div class="trends">
    <p>Trends</p>
    <div v-for="tag in tags" :key="tag.id" class="trends-group">
      <div>
        <p>#{{ tag.name }}</p>
        <p>{{ tag.posts.length }} posts</p>
      </div>
      <button @click="$emit('tagPosts', [tag.posts, tag.name])">Explore</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Posts from '@/components/Posts.vue'
import fetchData from '@/utils/handleFetch.js'

const tags = ref([])

onMounted(async () => {
  const response = await fetchData('posts/tags', 'GET')
  if (response.ok) {
    tags.value.push(...await response.json())
  } else {
    throw response
  }
})
</script>

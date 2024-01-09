<template>
  <section class="timeline">
    <div class="status">
      <p class="tag-name">
        Posts tagged with: <span>{{ tagName }}</span>
      </p>
      <Posts :posts="posts" />
    </div>

    <div class="suggestions">
      <SuggestedUsers />
      <!-- <Trends @tagPosts="(value) => posts = value[0]" /> -->
      <Trends @tagPosts="updateTag" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Posts from '@/components/Posts.vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Trends from '@/components/Trends.vue'
import fetchData from '@/utils/handleFetch.js'

const route = useRoute()
const posts = ref([])
const tagName = ref(route.params.name)

onMounted(async () => {
  const response = await fetchData(`posts/tag/${route.params.name}`, 'GET')
  if (response.ok) {
    const data = await response.json()
    posts.value.push(...data.posts)
  } else {
    throw response
  }
})

const updateTag = (value) => {
  posts.value = value[0]
  tagName.value = value[1]
}
</script>

<style scoped>
.tag-name {
  padding: var(--20px);
  font-weight: 700;
  color: hsl(0, 0%, 20%);
  background-color: #fff;
  border-radius: var(--10px);
}

.tag-name > span {
  padding: var(--10px);
  font-size: 1.4rem;
  color: #fff;
  background-color: hsl(330, 100%, 35%);
  border-radius: var(--10px);
}
</style>

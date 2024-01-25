<template>
  <Toast />
  <article v-for="post in posts" key="post.id" class="status-post">
    <section class="status-post-info">
      <img
        :src="post.created_by.avatar_path ? post.created_by.avatar_path : userAvatar"
        alt="Avatar" class="user-avatar-50"
      >
      <p class="status-post-info-name">{{ filterUsername(post.created_by) }}</p>
      <p class="status-post-info-time">{{ post.time_ago }} ago.</p>
    </section>
    <section class="status-post-body">
      <p id="postBody" v-html="post.body"></p>
      <div
        v-if="post.post_images.length"
        v-for="image in post.post_images" :key="image.id"
      >
        <img :src="image.image" alt="Post Image">
      </div>
    </section>
    <footer class="status-post-footer">
      <div>
        <a
          @click="like(post.id)"
          :class="post.created_by.id === store.userData.id ? 'disabled' : ''"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon" :class="{ liked: isLiked(post.id) }">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
          </svg>
        </a>
        <span>{{ post.likes_count }} likes</span>
      </div>
      <div>
        <a href="#">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
          </svg>
        </a>
        <router-link :to="{ name: 'postview', params: {id: post.id} }">
          {{ pluralize(post.comments.length, 'comment') }}
        </router-link>
      </div>
      <div>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
        </svg>
      </div>
    </footer>
  </article>
</template>

<script setup>
import { ref, onUpdated } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Toast from '@/components/Toast.vue'
import { filterUsername } from '@/utils/filters.js'
import fetchData from '@/utils/handleFetch.js'
import userAvatar from "../assets/images/user-avatar.png"

const props = defineProps(['posts'])

const store = useUserStore()
const toast = useToastStore()


onUpdated(() => {
  // Replace all words in post that starts with # symbol with a link
  if (props.posts.length) {
  for (let i = 0; i < props.posts.length; i++) {
    props.posts[i].body = props.posts[i].body.replace(/(?<=[#])(\w+)/g,
      '<a href="/tag/$1">$1</a>')
  }
  }
})

const isLiked = (post_id) => {
  const post = props.posts.filter(p => p.id === post_id)[0]
  if (post.liked_by.length) {
    const liked = post.liked_by.filter(like =>
      like.created_by_id === store.userData.id)[0]
    if (liked) return true
  }
  return false
}

const like = async (post_id) => {
  const response = await fetchData(`posts/${post_id}/like`, 'POST')
  if (response.ok) {
    const data = await response.json()
    const post = props.posts.filter(p => p.id === post_id)[0]
    if (data.message === 'Liked') {
      toast.showToast(5000, 'Liked', 'message-success')
      post.likes_count += 1
      // Add user in post liked users list
      props.posts.filter(p => {
        if (p.id === post_id) {
          p.liked_by.push({created_by_id: store.userData.id})
        }
      })
    } else {
      post.likes_count -= 1
      toast.showToast(5000, 'Unliked', 'message-danger')
      // Remove user from post liked users list
      props.posts.filter(p => {
        if (p.id === post_id) {
          const index = p.liked_by.indexOf(
            p.liked_by.filter(l => l.created_by_id === store.userData.id)
          )
          p.liked_by.pop(index)
        }
      })
    }
  } else {
    throw response
  }
}

const pluralize = (num, word, suffix='s') => {
  if (num !== 1) {
    return `${num} ${word}${suffix}`
  }
  return `${num} ${word}`
}

const filterPostsByTag = (tag) => {
  console.log('clciked')
}
</script>

<style scoped>
.liked {
  fill: hsl(0, 100%, 50%);
  color: hsl(0, 100%, 40%);
}
.disabled {
  pointer-events: none;
}
</style>

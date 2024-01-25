<template>
  <section class="timeline">
    <UserInfo
      :userProfile="store.userData"
      :friendsCount="store.getFriendsCount"
      :friends="store.getFriends"
    />

    <div class="status">
      <Posts :posts="post" />
      <Comments :comments="comments" />
      <div class="status-form">
        <form @submit.prevent="handleSubmit">
          <textarea
            v-model="body"
            rows="5"
            placeholder="What are you thinking about?"
          ></textarea>
          <div class="form-group">
            <input type="submit" value="Comment" class="btn">
          </div>
        </form>
      </div>
    </div>

    <div class="suggestions">
      <SuggestedUsers />
      <Trends />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import UserInfo from '@/components/UserInfo.vue'
import Posts from '@/components/Posts.vue'
import Comments from '@/components/Comments.vue'
import Trends from '@/components/Trends.vue'
import fetchData from '@/utils/handleFetch.js'
import postImage from "../assets/images/post-1.jpg"

const route = useRoute()
const store = useUserStore()

const post = ref([])
const comments = ref([])
const body = ref('')

onMounted(async () => {
  const response = await fetchData(`posts/post/${route.params.id}`, 'GET')
  if (response.ok) {
    post.value.push(await response.json())
    comments.value = post.value[0].comments
  } else {
    throw response
  }
})

const handleSubmit = async () => {
  const data = {'body': body.value}
  const response = await fetchData(
    `posts/${post.value[0].id}/comment`,
    'POST',
    data
  )
  if (response.ok) {
    const data = await response.json()
    comments.value.push(data)
    body.value = ''
  } else {
    throw response
  }
}
</script>

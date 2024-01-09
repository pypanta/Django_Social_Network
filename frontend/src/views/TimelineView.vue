<template>
  <section class="timeline">
    <UserInfo
      :userProfile="store.userData"
      :friendsCount="store.getFriendsCount"
      :friends="store.getFriends"
    />

    <div class="status">
      <div class="status-form">
        <form @submit.prevent="handleSubmit">
          <textarea
            v-model="body"
            rows="5"
            placeholder="What are you thinking about?"
          ></textarea>
          <div class="form-group">
            <div>
              <label for="myfile">Attach image:</label>
              <input type="file" multiple id="myfile" name="myfile">
            </div>
            <input type="submit" value="Post" class="btn">
          </div>
        </form>
      </div>
      <Posts :posts="posts" />
    </div>

    <div class="suggestions">
      <SuggestedUsers />
      <Trends @tagPosts="(value) => posts = value[0]" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import UserInfo from '@/components/UserInfo.vue'
import Posts from '@/components/Posts.vue'
import Trends from '@/components/Trends.vue'
import fetchData from '@/utils/handleFetch.js'
import extractTags from '@/utils/extractTagsFromPost.js'
import userAvatar from "../assets/images/user-avatar.png"
import postImage from "../assets/images/post-1.jpg"

const store = useUserStore()

const posts = ref([])
const body = ref('')

onMounted(async () => {
  const response = await fetchData('posts', 'GET')
  if (response.ok) {
    posts.value = await response.json()
  } else {
    throw response
  }
})

const handleSubmit = async () => {
  const files = document.querySelector('input[type="file"]')
  const formData  = new FormData()
  formData.append('body', body.value)
  for (let i of files.files) {
    formData.append('images', i)
  }
  const tags = extractTags(formData.get('body'))
  formData.append('tags', tags)
  const response = await fetchData('posts', 'POST', formData)
  if (response.ok) {
    const data = await response.json()
    posts.value.unshift(data)
    body.value = ''
    files.value = null
  } else {
    throw response
  }
}
</script>

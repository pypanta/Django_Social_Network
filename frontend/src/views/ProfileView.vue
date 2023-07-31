<template>
  <section class="timeline">
    <div class="user-info">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
      <p class="user-info-name">
        {{ userProfile.username ? userProfile.username : userProfile.email }}
      </p>
      <div class="user-info-stats">
        <a href="#">250 friends</a>
        <a href=#>98 posts</a>
      </div>
    </div>

    <div class="status">
      <div v-if="isLoggedInUser" class="status-form">
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
      <Trends />
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Posts from '@/components/Posts.vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Trends from '@/components/Trends.vue'
import fetchData from '@/utils/handleFetch.js'
import createdBy from '@/utils/createdby.js'
import userAvatar from "../assets/images/user-avatar.png"
import postImage from "../assets/images/post-1.jpg"

const route = useRoute()
const store = useUserStore()

const userProfile = reactive({
  id: null,
  first_name: '',
  last_name: '',
  username: '',
  email: ''
})
const posts = ref([])
const body = ref('')

onMounted(async () => {
  const response = await fetchData(`posts/${route.params.id}`, 'GET')
  if (response.ok) {
    const data = await response.json()
    for (let key in data.user) {
      if (key in userProfile) {
        userProfile[key] = data.user[key]
      }
    }
    posts.value = data.posts
  } else {
    throw response
  }
})

const isLoggedInUser = computed(() => {
  return userProfile.id === store.userData.id
})

const handleSubmit = async () => {
  const files = document.querySelector('input[type="file"]')
  const formData  = new FormData()
  formData.append('body', body.value)
  for (let i of files.files) {
    formData.append('images', i)
  }
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

<style scoped>
.notLoggedInUser:first-of-type {
  margin-top: 0;
}
</style>

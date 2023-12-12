<template>
  <section class="search">
    <div class="search-main">
      <form @submit.prevent="search" class="search-form">
        <div class="form-group">
          <input v-model="searchTerm" type="search" placeholder="What are you looking for?">
          <button class="btn">Search</button>
        </div>
        <div class="form-group">
          <p><strong>Search in</strong>:</p>
          <input v-model="searchType.users" type="checkbox" name="users">
          <label for="users">Users</label>
          <select v-model="selectedUserFilter">
            <option selected disabled value="">Ordered By</option>
            <option value="username">Username ASC</option>
            <option value="-username">Username DESC</option>
            <option value="email">E-mail ASC</option>
            <option value="-email">E-mail DESC</option>
          </select>
          <input v-model="searchType.posts" type="checkbox" name="posts">
          <label for="posts">Posts</label>
          <select v-model="selectedPostFilter">
            <option selected disabled value="">Ordered By</option>
            <option value="body">Post ASC</option>
            <option value="-body">Post DESC</option>
            <option value="created_at">Created At ASC</option>
            <option value="-created_at">Created At DESC</option>
            <option value="created_by">Created By ASC</option>
            <option value="-created_by">Created By DESC</option>
          </select>
        </div>
      </form>
      <div class="search-result">
        <div v-for="user in users" :key="user.id" class="user-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
          <p class="user-info-name">
          <router-link :to="{ name: 'profile', params: {id: user.id }}">
            {{ filterUsername(user) }}
          </router-link>
          </p>
          <div class="user-info-stats">
            <a @click="showFollowers = !showFollowers">
              {{ user.followers.length }} friends
            </a>
            <Friends
              v-if="showFollowers"
              :friends="user.followers"
              @close="showFollowers = false"
            />
            <router-link :to="{ name: 'profile', params: { id: user.id }}">
              {{ user.posts.length }} posts
            </router-link>
          </div>
        </div>
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
import { ref, reactive } from 'vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Posts from '@/components/Posts.vue'
import Trends from '@/components/Trends.vue'
import Friends from '@/components/Friends.vue'
import fetchData from '@/utils/handleFetch.js'
import { filterUsername } from '@/utils/filters.js'
import userAvatar from "../assets/images/user-avatar.png"

const searchTerm = ref('')
const searchType = reactive({
  users: false,
  posts: false
})
const selectedUserFilter = ref('')
const selectedPostFilter = ref('')
const users = ref([])
const posts = ref([])
const showFollowers = ref(false)

function generateURL(urlPoint) {
  let url = null;
  if (urlPoint === 'user') {
    url = `user/search/?q=${searchTerm.value}`;
    if (selectedUserFilter.value !== '') {
      url = `user/search/?q=${searchTerm.value}&ordering=${selectedUserFilter.value}`;
    }
  }
  if (urlPoint === 'posts') {
    url = `posts/search/?q=${searchTerm.value}`;
    if (selectedPostFilter.value !== '') {
      url = `posts/search/?q=${searchTerm.value}&ordering=${selectedPostFilter.value}`;
    }
  }
  return url;
}

const search = async () => {
  if (searchType.users && !searchType.posts) {
    const url = generateURL('user')
    const response = await fetchData(url, 'GET')
    if (response.ok) {
      users.value = await response.json()
      searchTerm.value = ''
      posts.value = []
    }
  } else if (searchType.posts && !searchType.users) {
    const url = generateURL('posts')
    const response = await fetchData(url, 'GET')
    if (response.ok) {
      posts.value = await response.json()
      searchTerm.value = ''
      users.value = []
    }
  } else {
    const users_response = await fetchData(
      `user/search/?q=${searchTerm.value}`, 'GET'
    )
    const posts_response = await fetchData(
      `posts/search/?q=${searchTerm.value}`, 'GET'
    )
    if (users_response.ok && posts_response.ok) {
      users.value = await users_response.json()
      posts.value = await posts_response.json()
      searchTerm.value = ''
    }
  }
}
</script>

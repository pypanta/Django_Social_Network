<template>
  <div v-if="suggestedFriendships.length" class="suggested-users">
    <p>People you may know</p>
    <div
      v-for="user in suggestedFriendships"
      :key="user.id"
      class="suggested-users-group"
    >
      <img
        :src="user.avatar_path ? user.avatar_path : userAvatar"
        alt="Avatar" class="user-avatar-50"
      >
      <p>{{ filterUsername(user) }}</p>
      <router-link
        :to="{ name: 'profile', params: { id: user.id } }"
        class="btn btn-small"
      >Show</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import fetchData from '@/utils/handleFetch.js'
import { filterUsername } from '@/utils/filters.js'
import userAvatar from "../assets/images/user-avatar.png"

const store = useUserStore()

const suggestedFriendships = ref([])

onMounted(async () => {
  const response = await fetchData('user/suggest-friendships', 'GET')
  if (response.ok) {
    suggestedFriendships.value = await response.json()
    console.log(suggestedFriendships.value)
  } else {
    throw response
  }
})
</script>

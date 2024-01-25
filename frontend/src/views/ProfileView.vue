<template>
  <Toast />
  <section class="timeline">
    <UserInfo
      :userProfile="userProfile"
      :isLoggedInUser="isLoggedInUser"
      :posts="posts"
      :followersCount="followersCount"
      :followingCount="followingCount"
      @updateFollowers="updateFriends"
      @updateFollowing="followingCount -= 1"
    />

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
      <Trends @tagPosts="(value) => posts = value[0]" />
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import UserInfo from '@/components/UserInfo.vue'
import Posts from '@/components/Posts.vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Trends from '@/components/Trends.vue'
import Toast from '@/components/Toast.vue'
import fetchData from '@/utils/handleFetch.js'
import { filterUsername, isAuthenticatedUser } from '@/utils/filters.js'
import extractTags from '@/utils/extractTagsFromPost.js'
import postImage from "../assets/images/post-1.jpg"

const route = useRoute()
const store = useUserStore()
const toast = useToastStore()

const userProfile = reactive({
  id: null,
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  following: [],
  followers: [],
  posts_count: 0,
  avatar_path: ''
})
const posts = ref([])
const body = ref('')
const isFollowed = ref(false)
const isLoggedInUser = ref(false)
const followersCount = ref(0)
const followingCount = ref(0)
const showFollowers = ref(false)
const showFollowing = ref(false)

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

  // Check if user is followed
  for (let user of userProfile.followers) {
    if (store.userData.id === user.id) {
      isFollowed.value = true
    }
  }
  isLoggedInUser.value = isAuthenticatedUser(userProfile.id, store.userData.id)

  // Get followers count
  followersCount.value = userProfile.followers.filter(
    f => f.status === 'AC'
  ).length
  followingCount.value = userProfile.following.filter(
    f => f.status === 'AC'
  ).length

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

const updateFriends = (value) => {
  console.log(value)
  if (value === 'follow') {
    followersCount.value += 1
  } else if (value === 'unfollow') {
    followersCount.value -= 1
  } else {
    followersCount.value += value
  }
}

const updateMessage = (value) => {
  const message_class = value[0] === 'accepted' ? 'message-success' : 'message-danger'
  toast.showToast(5000, `Friendship with ${value[1]} is ${value[0]}`, message_class)
}
</script>

<style scoped>
.notLoggedInUser:first-of-type {
  margin-top: 0;
}
</style>

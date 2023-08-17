<template>
  <Toast />
  <section class="timeline">
    <div class="user-info">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
      <p class="user-info-name">
        {{ userProfile.username ? userProfile.username : userProfile.email }}
      </p>
      <div class="user-info-stats">
        <a v-if="isLoggedInUser()" @click="showFollowers = !showFollowers">
          {{ followersCount }} followers
        </a>
        <a
          v-else-if="!isLoggedInUser() && followersCount > 0"
          @click="showFollowers = !showFollowers"
        >
          {{ followersCount }} followers
        </a>
        <a v-else>
          {{ followersCount }} followers
        </a>
        <a v-if="isLoggedInUser()" @click="showFollowing = !showFollowing">
          {{ followingCount }} following
        </a>
        <a
          v-else-if="!isLoggedInUser() && followingCount > 0"
          @click="showFollowing = !showFollowing"
        >
          {{ followingCount }} following
        </a>
        <a v-else>
          {{ followingCount }} following
        </a>
        <Friends
          v-if="showFollowers"
          :friends="userProfile.followers"
          :isLoggedInUser="isLoggedInUser()"
          @close="showFollowers = false"
          @unfollow="handleFollow"
          @updateFollowersCount="updateFriends"
          @friendshipRequest="updateMessage"
        />
        <Friends
          v-if="showFollowing"
          :friends="userProfile.following"
          :following="true"
          :isLoggedInUser="isLoggedInUser()"
          @close="showFollowing = false"
          @unfollow="handleFollow"
        />
        <a href=#>{{ posts.length }} posts</a>
      </div>
      <button
        v-if="isFollowed && !isLoggedInUser()"
        @click="handleFollow('unfollow')"
        class="btn"
      >
        Unfollow
      </button>
      <button
        v-else-if="!isLoggedInUser()"
        @click="handleFollow('follow')"
        class="btn"
      >
        Follow
      </button>
    </div>

    <div class="status">
      <div v-if="isLoggedInUser()" class="status-form">
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
import { useToastStore } from '@/stores/toast'
import Posts from '@/components/Posts.vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Trends from '@/components/Trends.vue'
import Friends from '@/components/Friends.vue'
import Toast from '@/components/Toast.vue'
import fetchData from '@/utils/handleFetch.js'
import createdBy from '@/utils/createdby.js'
import userAvatar from "../assets/images/user-avatar.png"
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
  followers: []
})
const posts = ref([])
const body = ref('')
const isFollowed = ref(false)
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

  // Get followers count
  followersCount.value = userProfile.followers.filter(
    f => f.status === 'AC'
  ).length
  followingCount.value = userProfile.following.filter(
    f => f.status === 'AC'
  ).length

})

const isLoggedInUser = () => {
  return userProfile.id === store.userData.id
}

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

const handleFollow = async (status) => {
  let url = 'user/follow'
  let data = userProfile
  if (status === 'unfollow') {
    url = 'user/unfollow'
  } else if (typeof status === 'object') {
    url = 'user/unfollow'
    data = status[0]
  }

  const response = await fetchData(url, 'POST', data)
  if (response.ok) {
    if (status === 'follow') {
      isFollowed.value = true
      followersCount.value += 1
      toast.showToast(5000, `Follow ${createdBy(userProfile)}`, 'message-success')
      // Add user to followers
      userProfile.followers.push(store.userData)
    } else if (status[1] === 'following') {
      // Decrease followingCount only if friendship if accepted
      if (status[0].status === 'AC') followingCount.value -= 1

      // Remove user from following users
      userProfile.following = userProfile.following.filter(
        p => p.id !== status[0].id
      )
      toast.showToast(5000, `Unfollow ${createdBy(status[0])}`, 'message-danger')
    } else {
      isFollowed.value = false
      followersCount.value -= 1
      toast.showToast(5000, `Unfollow ${createdBy(userProfile)}`, 'message-danger')
      // Remove user from followers
      userProfile.followers = userProfile.followers.filter(
        p => p.id !== store.userData.id
      )
    }
  }
}

const updateFriends = (value) => {
  followersCount.value += value
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

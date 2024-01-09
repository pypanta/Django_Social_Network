<template>
  <div v-if="route.name === 'profile'" class="user-info">
    <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
    <p class="user-info-name">
      {{ filterUsername(userProfile) }}
    </p>
    <div class="user-info-stats">
      <a v-if="isLoggedInUser" @click="showFollowers = !showFollowers">
        {{ followersCount }} followers
      </a>
      <a
        v-else-if="!isLoggedInUser && followersCount > 0"
        @click="showFollowers = !showFollowers"
      >
        {{ followersCount }} followers
      </a>
      <a v-else>
        {{ followersCount }} followers
      </a>
      <a v-if="isLoggedInUser" @click="showFollowing = !showFollowing">
        {{ followingCount }} following
      </a>
      <a
        v-else-if="!isLoggedInUser && followingCount > 0"
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
        :isLoggedInUser="isLoggedInUser"
        @close="showFollowers = false"
        @unfollow="handleFollow"
        @updateFollowersCount="updateFollowersCount"
        @friendshipRequest="updateMessage"
      />
      <Friends
        v-if="showFollowing"
        :friends="userProfile.following"
        :following="true"
        :isLoggedInUser="isLoggedInUser"
        @close="showFollowing = false"
        @unfollow="handleFollow"
      />
      <a href=#>{{ userProfile.posts_count }} posts</a>
    </div>
    <button
      v-if="isFollowed && !isLoggedInUser"
      @click="handleFollow('unfollow')"
      class="btn"
    >
      Unfollow
    </button>
    <button
      v-else-if="!isLoggedInUser"
      @click="handleFollow('follow')"
      class="btn"
    >
      Follow
    </button>
    <button
      v-if="!isLoggedInUser"
      @click="startConversation"
      class="btn-small">
        Start conversation
    </button>
  </div>
  <div v-else class="user-info">
    <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
    <p class="user-info-name">
      {{ filterUsername(userProfile) }}
    </p>
    <div class="user-info-stats">
      <a @click="showFriends = !showFriends">
        {{ friendsCount }} friends
      </a>
      <Friends
        v-if="showFriends"
        :friends="friends"
        @close="showFriends = false"
      />
      <router-link :to="{ name: 'profile', params: {id: userProfile.id} }">
        {{ userProfile.posts.length }} posts
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Friends from '@/components/Friends.vue'
import Toast from '@/components/Toast.vue'
import { filterUsername } from '@/utils/filters.js'
import userAvatar from "../assets/images/user-avatar.png"
import fetchData from '@/utils/handleFetch.js'

const props = defineProps({
  userProfile: Object,
  isLoggedInUser: Boolean,
  posts: Array,
  followersCount: Number,
  followingCount: Number,
  friendsCount: Number,
  friends: Array
})

const emit = defineEmits(['updateFollowers', 'updateFollowing'])

const route = useRoute()
const router = useRouter()
const store = useUserStore()
const toast = useToastStore()

const showFollowers = ref(false)
const showFollowing = ref(false)
const showFriends = ref(false)

const isFollowed = computed(() => {
  const followers = props.userProfile.followers.filter(f => f.id === store.userData.id)
  if (followers.length > 0) return true
  return false
})

const updateFollowersCount = (value) => {
  emit('updateFollowers', value)
}

const handleFollow = async (status) => {
  let url = 'user/follow'
  let data = props.userProfile
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
      emit('updateFollowers', 'follow')
      toast.showToast(5000, `Follow ${filterUsername(props.userProfile)}`, 'message-success')
      // Add user to followers
      props.userProfile.followers.push(store.userData)
    } else if (status[1] === 'following') {
      // Decrease followingCount only if friendship if accepted
      if (status[0].status === 'AC') emit('updateFollowing', 1)

      // Remove user from following users
      props.userProfile.following = props.userProfile.following.filter(
        p => p.id !== status[0].id
      )
      toast.showToast(5000, `Unfollow ${filterUsername(status[0])}`, 'message-danger')
    } else {
      isFollowed.value = false
      emit('updateFollowers', 'unfollow')
      toast.showToast(5000, `Unfollow ${filterUsername(props.userProfile)}`, 'message-danger')
      // Remove user from followers
      props.userProfile.followers = props.userProfile.followers.filter(
        p => p.id !== store.userData.id
      )
    }
  }
}

const startConversation = async () => {
  const response = await fetchData(`chat/${route.params.id}/create`, 'POST')
  if (response.ok) {
    router.push({name: 'chat'})
  } else {
    throw response
  }
}
</script>

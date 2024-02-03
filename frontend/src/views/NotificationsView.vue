<template>
  <section class="timeline">
    <UserInfo
      :userProfile="store.userData"
      :friendsCount="store.getFriendsCount"
      :friends="store.getFriends"
    />
    <div class="status">
      <article
        v-for="notification in notifications"
        :key="notification.id"
        class="status-post"
      >
        <div class="status-post-info">{{ notification.time_ago }} ago</div>
        <div class="status-post-body">
          <a
            @click="readNotification(notification.id, notification.object_id, notification.notification_type)"
            class="notification-link"
          >{{ notification.message }}
          </a>
        </div>
      </article>
      <div v-if="notifications.length" class="manage-notifications">
        <a @click="readNotification" class="read-all">
          Mark all as read
        </a>
      </div>
      <div v-else>
        <h2>You have no notifications</h2>
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
import { useRouter } from 'vue-router'
import UserInfo from '@/components/UserInfo.vue'
import Trends from '@/components/Trends.vue'
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import { useUserStore } from '@/stores/user'
import fetchData from '@/utils/handleFetch.js'

const router = useRouter()
const store = useUserStore()

const notifications = ref([])

// Get notifications
onMounted(async () => {
  const response = await fetchData('notifications', 'GET')
  if (response.ok) {
    notifications.value = await response.json()
  } else {
    throw response
  }
})

// Mark notification(s) as read
const readNotification = async (notification_id=null,
                                notification_object_id=null,
                                notification_type=null) => {
  if (notification_id && notification_object_id) {
    const response = await fetchData('notifications',
                                     'POST', {'id': notification_id})
    if (response.ok) {
      if (notification_type === 'postlike' ||
          notification_type === 'postcomment') {
        router.push({ name: 'postview',
                      params: { id: notification_object_id } })
      } else if (notification_type == 'newfriendrequest' ||
                 notification_type === 'acceptedfriendrequest' ||
                 notification_type === 'rejectedfriendrequest') {
        router.push({ name: 'profile',
                      params: { id: notification_object_id } })
      }
    } else {
      throw response
    }
  } else {
    if (confirm("Are you sure you want to mark all notifications as read?")) {
      const response = await fetchData('notifications',
                                       'POST', {'all': true})
      if (response.ok) {
        notifications.value = []
      } else {
        throw response
      }
    }
  }
}
</script>

<style scoped>
.status-post:first-of-type {
  margin-top: 0;
}

.notification-link,
.read-all {
  color: hsl(210, 100%, 40%);
  text-decoration: underline;
}

.notification-link:hover,
.notification-link:active {
  color: hsl(210, 100%, 60%);
}

.manage-notifications {
  margin-top: var(--20px);
}

.read-all {
  padding-bottom: var(--5px);
  font-weight: 500;
}

.read-all:hover,
.read-all:active {
  color: hsl(0, 100%, 50%);
}
</style>

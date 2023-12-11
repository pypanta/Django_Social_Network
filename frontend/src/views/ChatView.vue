<template>
  <section v-if="conversations.length" class="messages">
    <div>
      <div
        v-for="conversation in conversations"
        :key="conversation.id"
        @click="getActiveConversation(conversation.id)"
        class="messages-info"
      >
        <div
          @click="getActiveConversation(conversation.id)"
          :class="{ 'active': activeConversation.id === conversation.id }"
        >
          <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
          <p>{{ filterConversationUser(conversation.users) }}</p>
          <p>{{ conversation.modified_at_time_ago }} ago</p>
        </div>
        <a @click="deleteConversation(conversation.id)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="messages-trash-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </a>
      </div>
    </div>

    <div class="messages-wrapper">
      <div
        v-for="message in activeConversation.messages" :key="message.id"
        class="messages-container"
      >
        <div
          v-if="store.userData.id === message.created_by.id"
          class="message-left"
        >
          <div>
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
            <p>
              <small>
                <b>{{ filterUsername(message.created_by) }} said:</b>
              </small>
              {{ message.body }}
            </p>
            <p>{{ message.created_at_time_ago }} ago</p>
          </div>
        </div>
        <div v-else class="message-right">
          <div>
            <p>
            <small>
              <b>{{filterUsername(message.created_by) }} said:</b>
            </small>
              {{ message.body }}
            </p>
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
            <p>{{ message.created_at_time_ago }} ago</p>
          </div>
        </div>
      </div>
      <div class="messages-post">
        <form @submit.prevent="submitForm" class="messages-post-form">
          <textarea
            v-model="messageData.body"
            rows="6"
            placeholder="What do you want to say?"
          ></textarea>
          <input type="submit" value="Send" class="btn">
        </form>
      </div>
    </div>
  </section>
  <section v-else class="messages">
    <h2>{{ noConversationsMessage }}</h2>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import fetchData from '@/utils/handleFetch.js'
import { filterUsername } from '@/utils/filters.js'
import userAvatar from "../assets/images/user-avatar.png"

const store = useUserStore()
const router = useRouter()
const conversations = ref([])
const noConversationsMessage = ref("You don't have any conversations yet!")
const activeConversation = ref({})
const messageBody = ref('')
const messageData = reactive({
  body: '',
})

onMounted(() => {
  getConversations()
})

const getConversations = async () => {
  const response = await fetchData('chat', 'GET')
  if (response.ok) {
    conversations.value = await response.json()
    if (conversations.value.length) {
      activeConversation.value = conversations.value[0]
      getMessages()
    }
  } else {
    throw response
  }
}

const getMessages = async () => {
  const response = await fetchData(`chat/${activeConversation.value.id}`, 'GET')
  if (response.ok) {
    activeConversation.value = await response.json()
  } else {
    throw response
  }
}

const submitForm = async () => {
  const response = await fetchData(`chat/${activeConversation.value.id}/send`,
                                   'POST', messageData)
  if (response.ok) {
    const message = await response.json()
    activeConversation.value.messages.push(message)
    messageData.body = ''
  } else {
    throw response
  }
}

const getActiveConversation = (id) => {
  activeConversation.value.id = id
  getMessages()
}

const filterConversationUser = (users) => {
  const user = users.filter(u => u.id !== store.userData.id)[0]
  return filterUsername(user)
}

const deleteConversation = async (id) => {
  const response = await fetchData(`chat/${id}/delete`, 'DELETE')
  if (response.ok) {
    conversations.value = conversations.value.filter(c => c.id !== id)
    router.push({name: 'chat'})
  } else {
    throw response
  }
}
</script>

<style scoped>
.active {
  padding: var(--5px);
  color: hsl(0, 0%, 100%);
  background-color: hsl(220, 100%, 55%);
  border-radius: var(--10px);
}
</style>

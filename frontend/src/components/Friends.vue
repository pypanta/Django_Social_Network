<template>
  <div v-if="friends.length" id="userModal" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
      <ul class="modal-list">
        <li v-for="friend in friends" :key="friend.id">
          <div v-if="isLoggedInUser && friend.status === 'PE'">
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
            <div class="modal-links">
              <router-link :to="{ name: 'profile', params: { id: friend.id }}">
                {{ createdBy(friend) }}
              </router-link>
              <div v-if="!following">
                <a
                  @click="handleFriendshipRequest(friend.id, 'accept')"
                  title="Accept friendship"
                >
                  &#10004;
                </a>
                <a
                  @click="handleFriendshipRequest(friend.id, 'reject')"
                  title="Reject friendship"
                >
                  &#10008;
                </a>
              </div>
              <a
                v-if="following && isLoggedInUser"
                @click="$emit('unfollow', [friend, 'following'])"
                class="btn-unfollow"
                >Unfollow
              </a>
            </div>
          </div>
          <div v-else-if="friend.status === 'AC'">
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
            <div class="modal-links">
              <router-link :to="{ name: 'profile', params: { id: friend.id }}">
                {{ createdBy(friend) }}
              </router-link>
              <a
                v-if="following && isLoggedInUser"
                @click="$emit('unfollow', [friend, 'following'])"
                class="btn-unfollow"
                >Unfollow
              </a>
            </div>
          </div>
        </li>
      </ul>
      <button @click="$emit('close')" class="close">Close</button>
    </div>
  </div>
</template>

<script setup>
import createdBy from '@/utils/createdby.js'
import fetchData from '@/utils/handleFetch.js'
import userAvatar from "../assets/images/user-avatar.png"

const props = defineProps(['friends', 'following', 'isLoggedInUser'])
const emit = defineEmits(['friendId'])

const handleFriendshipRequest = async (id, status) => {
  const response = await fetchData(
    'user/accept', 'POST', {id: id, status: status}
  )
  if (response.ok) {
    const user = createdBy(props.friends.filter(u => u.id === id)[0])
    if (status === 'accept') {
      props.friends = props.friends.filter(f => {
        if (f.id === id) f.status = 'AC'
      })
      emit('updateFollowersCount', 1)
      emit('friendshipRequest', ['accepted', user])
    } else {
      props.friends = props.friends.filter(f => {
        if (f.id === id) f.status = 'RE'
      })
      emit('updateFollowersCount', 0)
      emit('friendshipRequest', ['rejected', user])
    }
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: hsl(195, 100%, 90%);
  border-radius: 5px;
}

.close {
  margin-top: 20px;
  padding: 5px;
  font-size: 1rem;
  cursor: pointer;
  color: #fff;
  background-color: hsl(195, 100%, 20%);
  border: none;
  border-radius: 5px;
}

.close:focus,
.close:hover {
  background-color: hsl(195, 100%, 30%);
}

.modal-list {
  list-style: none;
}

.modal-list > li > div {
  display: flex;
  gap: 10px;
}

.modal-list > li:not(:last-of-type) {
  margin-bottom: 10px;
}

.modal-links {
  align-self: center;
  flex-grow: 2;
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.modal-links > a {
  white-space: nowrap;
  text-decoration: none;
  font-weight: 700;
}

.modal-links > a:first-of-type {
  color: hsl(195, 100%, 20%);
  font-size: 1.2rem;
}

.modal-links > div {
  display: flex;
  align-items: center;
  gap: 5px;
}

.modal-links > div > a {
  font-size: 1.2rem;
}

.modal-links > div > a:first-of-type {
  color: hsl(140, 100%, 30%);
}

.modal-links > div > a:last-of-type {
  color: hsl(12, 100%, 50%);
}

.modal-links > .btn-unfollow {
  padding: 5px;
  font-size: .7rem;
  color: #fff;
  background-color: hsl(0, 100%, 60%);
  border-radius: 5px;
}

.modal-links > .btn-unfollow:focus,
.modal-links > .btn-unfollow:hover {
  background-color: hsl(0, 100%, 70%);
}

/* MEDIA */
@media (max-width: 380px) {
  .modal-list > li > div, .modal-links {
    flex-direction: column;
  }
  .modal-list > li > div > *, .modal-links > * {
    align-self: center;
  }
  .modal-list > li > div {
    gap: 5px;
  }
  .modal-list > li > div:not(:last-of-type) {
    margin-bottom: 20px;
  }
  .modal-links {
    gap: 10px;
  }
  .modal-links > a:first-of-type {
    margin-right: 0;
    font-size: 1rem;
  }
  .modal-links > .btn-unfollow {
    font-size: .6rem;
  }
  .close {
    margin-top: 30px;
  }
}
</style>

import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import fetchData from '@/utils/handleFetch.js'

export const useUserStore = defineStore('user', () => {
  const isAuthenticated = ref(false);
  const message = ref('');
  const userData = reactive({
    id: null,
    first_name: '',
    last_name: '',
    username: '',
    email: ''
  });

  const getUsername = computed(() => {
    if (userData.first_name && userData.last_name) {
      return `${userData.first_name} ${userData.last_name}`
    } else if (userData.username) {
      return userData.username;
    } else {
      return userData.email;
    }
  })

  async function getUser() {
    const response = await fetchData('user', 'GET');
    if (response !== undefined && response.ok) {
      const data = await response.json();
      if (data.first_name && data.last_name) {
        message.value = `Hello ${data.first_name} ${data.last_name}`;
      } else if (data.username) {
        message.value = `Hello ${data.username}`;
      } else {
        message.value = `Hello ${data.email}`;
      }
      isAuthenticated.value = true;
      for (let key in data) {
        if (key in userData) {
          userData[key] = data[key];
        }
      }
    } else {
      isAuthenticated.value = false;
      message.value = 'You are not authenticated.';
    }
  }

  return { isAuthenticated, message, userData, getUser, getUsername }
})

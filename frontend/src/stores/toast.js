import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', () => {
  const ms = ref(0)
  const message = ref('')
  const classes = ref('')
  const isVisible = ref(false)

  function showToast(ms, msg, cls='') {
    ms = parseInt(ms)
    message.value = msg
    classes.value = cls
    isVisible.value = true

    setTimeout(() => {
      isVisible.value = false
    }, ms)
  }

  return {
    ms,
    message,
    classes,
    isVisible,
    showToast
  }
})

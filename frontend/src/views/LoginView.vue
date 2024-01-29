<template>
  <Toast />
  <section class="auth">
    <div>
      <h2>Log In</h2>
      <p>Dolor veritatis iste excepturi velit delectus. Consequatur quasi nisi earum temporibus vero id harum Est perferendis at nobis animi nesciunt. Vel voluptatum odio earum similique officiis eveniet placeat.</p>
      <p>Amet magnam aperiam magnam eligendi sunt Ut eaque eius magnam fugiat maxime Assumenda sapiente iste odio perferendis libero Enim tempore quos totam laboriosam consectetur. Dignissimos eum dolores soluta cum eligendi.</p>
      <p>
        Don't have an account?
        <router-link :to="{ name: 'signup' }">
          Click here
        </router-link> to create one!
      </p>
    </div>
    <div>
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="auth-form-group">
          <label>E-mail or Username</label>
          <input
            v-model="data.email"
            type="text"
            placeholder="Your e-mail address or username"
          />
        </div>
        <div class="auth-form-group">
          <label>Password</label>
          <input
            v-model="data.password"
            type="password"
            placeholder="Your password"
          />
        </div>
        <div class="auth-form-group">
          <p v-if="errors.detail" class="error">
            {{ errors.detail }}
          </p>
        </div>
        <input type="submit" value="Log In" class="btn btn-success">
      </form>
    </div>
  </section>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import Toast from '@/components/Toast.vue'
import fetchData from '@/utils/handleFetch.js'

const store = useUserStore()
const { isAuthenticated, message, userData } = storeToRefs(store)

const router = useRouter()

const data = reactive({
  email: '',
  password: ''
})

const errors = reactive({
  detail: ''
})

const handleSubmit = async () => {
  const response = await fetchData('login', 'POST', data)
  if (response.ok) {
    store.isAuthenticated = true
    store.getUser()
    router.push({ name: 'home' })
  } else {
    const responseError = {
      status: response.status,
      body: await response.json()
    }
    for (const error in errors) {
      if (error in responseError['body']) {
        errors[error] = responseError['body'][error]
      } else {
        errors[error] = ''
      }
    }
    throw new Error(JSON.stringify(responseError))
  }
}
</script>

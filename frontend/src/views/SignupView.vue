<template>
  <section class="auth">
    <div>
      <h2>Sign Up</h2>
      <p>Dolor veritatis iste excepturi velit delectus. Consequatur quasi nisi earum temporibus vero id harum Est perferendis at nobis animi nesciunt. Vel voluptatum odio earum similique officiis eveniet placeat.</p>
      <p>Amet magnam aperiam magnam eligendi sunt Ut eaque eius magnam fugiat maxime Assumenda sapiente iste odio perferendis libero Enim tempore quos totam laboriosam consectetur. Dignissimos eum dolores soluta cum eligendi.</p>
      <p>
        Already have an account?
        <router-link :to="{ name: 'login'}">Click here</router-link> to log in!
      </p>
    </div>
    <div>
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="auth-form-group">
          <label>First Name</label>
          <input v-model="data.first_name" type="text" placeholder="Your first name">
        </div>
        <div class="auth-form-group">
          <label>Last Name</label>
          <input v-model="data.last_name" type="text" placeholder="Your last name">
        </div>
        <div class="auth-form-group">
          <label>E-mail</label>
          <input v-model="data.email" type="email" placeholder="Your e-mail address">
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>
        <div class="auth-form-group">
          <label>Password</label>
          <input v-model="data.password" type="password" placeholder="Your password">
          <p v-if="errors.password" class="error">{{ errors.password }}</p>
        </div>
        <div class="auth-form-group">
          <label>Repeat password</label>
          <input v-model="data.password_confirm" type="password" placeholder="Repeat your password">
          <p v-if="errors.password_confirm" class="error">
            {{ errors.password_confirm }}
          </p>
        </div>
        <div class="auth-form-group">
          <p v-if="errors.non_field_errors" class="error">
            {{ errors.non_field_errors }}
          </p>
        </div>
        <input type="submit" value="Sign Up" class="btn btn-success">
      </form>
    </div>
  </section>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import fetchData from '@/utils/handleFetch.js'

const router = useRouter()

const data = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  password_confirm: ''
})

const errors = reactive({
  email: '',
  password: '',
  password_confirm: '',
  non_field_errors: ''
})

const handleSubmit = async () => {
  const response = await fetchData('signup', 'POST', data)
  if (response.ok) {
    router.push({ name: 'login' })
  } else {
    const responseError = {
      status: response.status,
      body: await response.json()
    }
    for (const error in errors) {
      if (error in responseError['body']) {
        errors[error] = responseError['body'][error][0]
      } else {
        errors[error] = ''
      }
    }
    throw new Error(JSON.stringify(responseError))
  }
}
</script>

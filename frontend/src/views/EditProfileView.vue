<template>
  <Toast />
  <section class="auth">
    <div>
      <h2>Edit Profile</h2>
      <p>Dolor veritatis iste excepturi velit delectus. Consequatur quasi nisi earum temporibus vero id harum Est perferendis at nobis animi nesciunt. Vel voluptatum odio earum similique officiis eveniet placeat.</p>
      <p>Amet magnam aperiam magnam eligendi sunt Ut eaque eius magnam fugiat maxime Assumenda sapiente iste odio perferendis libero Enim tempore quos totam laboriosam consectetur. Dignissimos eum dolores soluta cum eligendi.</p>
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
          <label>Username</label>
          <input v-model="data.username" type="text" placeholder="Your username">
        </div>
        <div class="auth-form-group">
          <label>E-mail</label>
          <input v-model="data.email" type="email" placeholder="Your e-mail address">
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>
        <div class="auth-form-group">
          <label for="myfile">Avatar image:</label>
          <img :src="data.avatar_path" alt="">
          <input type="file" ref="avatar">
        </div>
        <div class="auth-form-group">
          <p v-if="errors.non_field_errors" class="error">
            {{ errors.non_field_errors }}
          </p>
        </div>
        <input type="submit" value="Submit" class="btn btn-success">
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Toast from '@/components/Toast.vue'
import fetchData from '@/utils/handleFetch.js'

const router = useRouter()
const store = useUserStore()
const toast = useToastStore()

const data = reactive({
  id: store.userData.id,
  first_name: store.userData.first_name,
  last_name: store.userData.last_name,
  username: store.userData.username,
  email: store.userData.email,
  avatar: null,
  avatar_path: store.userData.avatar_path
})

const avatar = ref(null)

const errors = reactive({
  email: '',
  non_field_errors: ''
})

const handleSubmit = async () => {
  if (avatar.value.files.length) data.avatar = avatar.value.files[0]
  const formData = new FormData()
  for (let i in data) {
    if (i === 'avatar_path' || data[i] === null) continue
    formData.append(i, data[i])
  }

  const response = await fetchData(`user/${data.id}/edit`, 'PUT', formData)
  if (response.ok) {
    toast.showToast(5000, 'Profile saved!', 'message-success')
    router.push({ name: 'profile', params: { id: data.id } })
  } else {
    const responseError = {
      status: response.status,
      body: await response.json()
    }
    for (const error in errors) {
      if (error in responseError['body']) {
        errors[error] = responseError['body'][error]
        toast.showToast(5000,
                        `${responseError['body'][error]}`,
                        'message-danger')
      } else {
        errors[error] = ''
      }
    }
    throw new Error(JSON.stringify(responseError))
  }
}
</script>

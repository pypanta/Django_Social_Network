<template>
  <Toast />
  <section class="auth">
    <div>
      <h2>Edit Profile</h2>
      <p>Dolor veritatis iste excepturi velit delectus. Consequatur quasi nisi earum temporibus vero id harum Est perferendis at nobis animi nesciunt. Vel voluptatum odio earum similique officiis eveniet placeat.</p>
      <p>Amet magnam aperiam magnam eligendi sunt Ut eaque eius magnam fugiat maxime Assumenda sapiente iste odio perferendis libero Enim tempore quos totam laboriosam consectetur. Dignissimos eum dolores soluta cum eligendi.</p>
      <!-- Password Change Form -->
      <div class="password-change">
        <button
          @click="passwordChange.active = !passwordChange.active"
          :class="passwordChange.active ? 'active' : ''"
          class="btn btn-small"
        >
          {{ passwordChange.text }}
        </button>
        <form
          v-if="passwordChange.active"
          @submit.prevent="handlePasswordChange"
          class="auth-form"
        >
          <div class="auth-form-group">
            <label>Your Old Password</label>
            <div class="inputs-group">
              <input
                v-model="newPassword.old_password"
                :type="passwordShow.old.type"
                placeholder="Your new password"
              >
              <input
                v-if="newPassword.old_password"
                v-model="passwordShow.old.isChecked"
                @click="showPassword('old')"
                :title="passwordShow.old.title"
                type="checkbox"
              >
            </div>
          </div>
          <div class="auth-form-group">
            <label>Your New Password</label>
            <div class="inputs-group">
              <input
                v-model="newPassword.new_password"
                :type="passwordShow.new.type"
                placeholder="Your new password"
              >
              <input
                v-if="newPassword.new_password"
                v-model="passwordShow.new.isChecked"
                type="checkbox"
                @click="showPassword('new')"
                :title="passwordShow.new.title"
              >
            </div>
          </div>
          <div class="auth-form-group">
            <label>Confirm Your New Password</label>
            <div class="inputs-group">
              <input
                v-model="newPassword.new_password_confirm"
                :type="passwordShow.newConfirm.type"
                placeholder="Repeat your new password"
              >
              <input
                v-if="newPassword.new_password_confirm"
                v-model="passwordShow.newConfirm.isChecked"
                type="checkbox"
                @click="showPassword('newConfirm')"
                :title="passwordShow.newConfirm.title"
              >
            </div>
          </div>
          <div class="auth-form-group">
            <p v-if="errors.message" class="error">
              {{ errors.message }}
            </p>
          </div>
          <input type="submit" value="Submit" class="btn btn-success">
        </form>
      </div>
    </div>
    <!-- Edit Profile Form -->
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
import { ref, reactive, watch } from 'vue'
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

const passwordChange = reactive({
  active: false,
  text: 'Change Your Password',
})

const passwordShow = reactive({
  old: { isChecked: false, title: 'Show password', type: 'password' },
  new: { isChecked: false, title: 'Show password', type: 'password' },
  newConfirm: { isChecked: false, title: 'Show password', type: 'password' },
})

const newPassword = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const errors = reactive({
  email: '',
  non_field_errors: '',
  message: ''
})

const avatar = ref(null)

watch(passwordChange, (value) => {
  if (value.active) {
    value.text = 'Close the Form'
  } else {
    value.text = 'Change Your Password'
  }
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

const handlePasswordChange = async () => {
  const response = await fetchData(`user/change-password`, 'POST', newPassword)
  if (response.ok) {
    const data = await response.json()
    toast.showToast(5000, data.message, 'message-success')

    // Reset change password form field inputs
    for (const field in newPassword) newPassword[field] = ''

    // Reset change password form input attributes
    for (const field in passwordShow) {
      passwordShow[field].isChecked = false
      passwordShow[field].title = 'Show password'
      passwordShow[field].type = 'password'
    }

    // Reset error message
    errors.message = ''

    passwordChange.active = false
  } else {
    const data = await response.json()
    if (data.message) {
      errors.message = data.message
      toast.showToast(5000, data.message, 'message-danger')
    }
    throw response
  }
}

const showPassword = (key) => {
  if (passwordShow[key].isChecked) {
    passwordShow[key].type = 'password'
    passwordShow[key].title = 'Show password'
    passwordShow[key].isChecked = false
  } else {
    passwordShow[key].type = 'text'
    passwordShow[key].title = 'Hide password'
    passwordShow[key].isChecked = true
  }
}
</script>

<style scoped>
.password-change {
  margin-top: var(--20px);
}

.password-change > button {
  background-color: hsl(0, 100%, 50%);
}

.password-change > button.active {
  margin-bottom: var(--10px);
  background-color: hsl(30, 100%, 60%);
}

.inputs-group {
  display: flex;
  gap: var(--10px);
}
.inputs-group > input:first-of-type {
  width: 100%;
  padding: var(--20px);
  font-size: var(--15px);
  border: 1px solid hsl(0, 0%, 85%);
  border-radius: var(--10px);
}
</style>

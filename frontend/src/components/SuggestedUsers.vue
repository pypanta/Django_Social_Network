<template>
  <div class="suggested-users">
    <p>People you may know</p>
    <div class="suggested-users-group">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
      <p>User Name</p>
      <button>Show</button>
    </div>
    <div class="suggested-users-group">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
      <p>User Name</p>
      <button>Show</button>
    </div>
    <div class="suggested-users-group">
      <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
      <p>User Name</p>
      <button>Show</button>
    </div>
  </div>
</template>

<script setup>
import userAvatar from "../assets/images/user-avatar.png"
</script>

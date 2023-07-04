<template>
  <section class="messages">
    <div class="messages-info">
      <div>
        <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
        <p>User Name</p>
        <p>20 minutes ago</p>
      </div>
      <div>
        <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
        <p>User Name</p>
        <p>20 minutes ago</p>
      </div>
      <div>
        <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
        <p>User Name</p>
        <p>20 minutes ago</p>
      </div>
    </div>

    <div class="messages-wrapper">
      <div class="messages-container">
        <div class="message-right">
          <div>
            <p>Adipisicing facilis beatae nemo a debitis provident Delectus voluptate culpa sed itaque dolorem facilis.</p>
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
          </div>
          <p>2 minutes ago</p>
        </div>
        <div class="message-left">
          <div>
            <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
            <p>Dolor est numquam quidem architecto at Doloremque nemo quos esse commodi natus Ex fugit odio facere vero consectetur! A iusto tempore rem recusandae vel.</p>
          </div>
          <p>2 minutes ago</p>
        </div>
      </div>
      <div class="messages-post">
        <form class="messages-post-form">
          <textarea rows="6" placeholder="What do you want to say?"></textarea>
          <input type="submit" value="Post" class="btn">
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import userAvatar from "../assets/images/user-avatar.png"
</script>

<template>
  <section class="search">
    <div class="search-main">
      <div class="search-form">
        <input type="search" placeholder="What are you looking for?">
        <button class="btn">Search</button>
      </div>
      <div class="search-result">
        <div class="user-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
          <p class="user-info-name">User Name</p>
          <div class="user-info-stats">
            <a href="#">250 friends</a>
            <a href=#>98 posts</a>
          </div>
        </div>
        <div class="user-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
          <p class="user-info-name">User Name</p>
          <div class="user-info-stats">
            <a href="#">250 friends</a>
            <a href=#>98 posts</a>
          </div>
        </div>
        <div class="user-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
          <p class="user-info-name">User Name</p>
          <div class="user-info-stats">
            <a href="#">250 friends</a>
            <a href=#>98 posts</a>
          </div>
        </div>
        <div class="user-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-200">
          <p class="user-info-name">User Name</p>
          <div class="user-info-stats">
            <a href="#">250 friends</a>
            <a href=#>98 posts</a>
          </div>
        </div>
      </div>
      <article class="status-post">
        <section class="status-post-info">
          <img :src="userAvatar" alt="Avatar" class="user-avatar-50">
          <p class="status-post-info-name">User Name</p>
          <p class="status-post-info-time">24 minutes ago</p>
        </section>
        <section class="status-post-body">
          <p>Post with image.</p>
          <p>Dolor veritatis deserunt esse sit tempora Inventore ea sit reiciendis natus odio At facere sed quas autem quos Itaque dolorem.</p>
          <img :src="postImage" alt="Post Image">
        </section>
        <footer class="status-post-footer">
          <div>
            <a href="#">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </a>
            <span>24 likes</span>
          </div>
          <div>
            <a href="#">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
              </svg>
            </a>
            <span>0 comments</span>
          </div>
          <div>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="status-post-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
            </svg>
          </div>
        </footer>
      </article>
    </div>

    <div class="suggestions">
      <SuggestedUsers />
      <Trends />
    </div>
  </section>
</template>

<script setup>
import SuggestedUsers from '@/components/SuggestedUsers.vue'
import Trends from '@/components/Trends.vue'
import userAvatar from "../assets/images/user-avatar.png"
</script>

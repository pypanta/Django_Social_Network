import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import TimelineView from '../views/TimelineView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import TagView from '../views/TagView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import NotificationsView from '../views/NotificationsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      beforeEnter: async (to, from) => {
        const store = useUserStore()
        await store.getUser()
        if (store.isAuthenticated) return {name: 'home'}
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: async (to, from) => {
        const store = useUserStore()
        await store.getUser()
        if (store.isAuthenticated) return {name: 'home'}
      }
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: TimelineView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/profile/edit',
      name: 'editprofileview',
      component: EditProfileView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/tag/:name',
      name: 'tagview',
      component: TagView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const store = useUserStore()
  await store.getUser()
  if (to.name !== 'login' && to.name !== 'signup' && !store.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router

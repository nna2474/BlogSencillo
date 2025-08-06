import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import PostDetail from '../views/PostDetail.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import NewPost from '../views/NewPost.vue';
import { useAuthStore } from '@/stores/useAuthStore'

const routes = [
  { path: '/', component: HomeView },
  { path: '/post/:id', component: PostDetail },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/new-post',
    component: NewPost,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router

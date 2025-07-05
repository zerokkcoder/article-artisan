import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Dashboard from '../pages/Dashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  // 动态导入store以避免循环依赖
  import('../stores/user').then(({ useUserStore }) => {
    const userStore = useUserStore()
    
    // 初始化用户状态
    if (!userStore.user) {
      userStore.initializeUser()
    }
    
    const isAuthenticated = userStore.isAuthenticated
    
    if (to.meta.requiresAuth && !isAuthenticated) {
      next('/login')
    } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
      next('/dashboard')
    } else {
      next()
    }
  })
})

export default router
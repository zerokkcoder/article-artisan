import { createRouter, createWebHashHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

// 懒加载页面组件以优化性能
const Login = () => import('../pages/Login.vue')
const Register = () => import('../pages/Register.vue')
const Home = () => import('../pages/Home.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Welcome = () => import('../views/Welcome.vue')

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
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Welcome',
        component: Welcome
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  
  // 初始化用户状态
  if (!userStore.user) {
    userStore.initializeUser()
  }
  
  const isAuthenticated = userStore.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/home')
  } else {
    next()
  }
})

export default router
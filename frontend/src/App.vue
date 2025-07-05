<script setup lang="ts">
import { ref } from 'vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Dashboard from '@/components/Dashboard.vue'

interface User {
  username: string
  token: string
}

const currentView = ref<'login' | 'register' | 'dashboard'>('login')
const user = ref<User | null>(null)

const handleSwitchToRegister = () => {
  currentView.value = 'register'
}

const handleSwitchToLogin = () => {
  currentView.value = 'login'
}

const handleRegisterSuccess = () => {
  currentView.value = 'login'
}

const handleLoginSuccess = (userData: User) => {
  user.value = userData
  currentView.value = 'dashboard'
  // 可以在这里保存用户信息到 localStorage
  localStorage.setItem('user', JSON.stringify(userData))
}

const handleLogout = () => {
  user.value = null
  currentView.value = 'login'
  // 清除本地存储的用户信息
  localStorage.removeItem('user')
}

// 检查是否有已保存的用户信息
const checkSavedUser = () => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      user.value = JSON.parse(savedUser)
      currentView.value = 'dashboard'
    } catch (error) {
      localStorage.removeItem('user')
    }
  }
}

// 初始化时检查用户状态
checkSavedUser()
</script>

<template>
  <div id="app">
    <!-- 登录页面 -->
    <Login 
      v-if="currentView === 'login'"
      @switch-to-register="handleSwitchToRegister"
      @login-success="handleLoginSuccess"
    />
    
    <!-- 注册页面 -->
    <Register 
      v-else-if="currentView === 'register'"
      @switch-to-login="handleSwitchToLogin"
      @register-success="handleRegisterSuccess"
    />
    
    <!-- 主界面 -->
    <Dashboard 
      v-else-if="currentView === 'dashboard' && user"
      :user="user"
      @logout="handleLogout"
    />
  </div>
</template>

<style scoped>
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>

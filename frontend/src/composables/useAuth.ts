import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { showMessage } from '@/utils/message'
import { useUserStore } from '@/stores/user'

export function useAuth() {
  const router = useRouter()
  const userStore = useUserStore()

  const handleLogin = async (username: string, password: string) => {
    const success = await userStore.login(username, password)
    
    if (success) {
      showMessage.success('登录成功！')
      router.push('/home')
    } else {
      showMessage.error(userStore.error || '登录失败')
    }
  }

  const handleRegister = async (username: string, email: string, password: string, confirmPassword: string) => {
    const success = await userStore.register(username, email, password, confirmPassword)
    
    if (success) {
      showMessage.success('注册成功！')
      router.push('/home')
    } else {
      showMessage.error(userStore.error || '注册失败')
    }
  }

  const logout = () => {
    userStore.clearUser()
    showMessage.success('已退出登录')
    router.push('/login')
  }

  const switchToLogin = () => {
    router.push('/login')
  }

  const switchToRegister = () => {
    router.push('/register')
  }

  return {
    // 状态
    user: computed(() => userStore.user),
    isLoading: computed(() => userStore.isLoading),
    error: computed(() => userStore.error),
    
    // 方法
    login: handleLogin,
    register: handleRegister,
    logout,
    switchToLogin,
    switchToRegister
  }
}
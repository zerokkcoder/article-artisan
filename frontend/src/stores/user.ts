import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const username = computed(() => user.value?.username || '')

  // Actions
  const setUser = (userData: User) => {
    user.value = userData
    error.value = null
    // 持久化到localStorage
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const clearUser = () => {
    user.value = null
    error.value = null
    localStorage.removeItem('user')
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  const setError = (errorMessage: string) => {
    error.value = errorMessage
  }

  const initializeUser = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch (e) {
        console.error('Failed to parse stored user data:', e)
        localStorage.removeItem('user')
      }
    }
  }

  const login = async (username: string, password: string): Promise<boolean> => {
    setLoading(true)
    setError('')
    
    try {
      const { authApi } = await import('../services/api')
      const response = await authApi.login({ username, password })
      
      if (response.success && response.data) {
        setUser(response.data.user)
        return true
      } else {
        setError('登录失败')
        return false
      }
    } catch (err: any) {
      setError(err.message || '登录失败，请稍后重试')
      return false
    } finally {
      setLoading(false)
    }
  }

  const register = async (username: string, email: string, password: string, confirmPassword: string): Promise<boolean> => {
    setLoading(true)
    setError('')
    
    try {
      const { authApi } = await import('../services/api')
      const response = await authApi.register({ username, email, password, confirmPassword })
      
      if (response.success && response.data) {
        setUser(response.data.user)
        return true
      } else {
        setError('注册失败')
        return false
      }
    } catch (err: any) {
      setError(err.message || '注册失败，请稍后重试')
      return false
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    clearUser()
  }

  return {
    // State
    user,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    username,
    // Actions
    setUser,
    clearUser,
    setLoading,
    setError,
    initializeUser,
    login,
    register,
    logout
  }
})
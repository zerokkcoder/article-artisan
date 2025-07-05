import type {
  ApiResponse,
  LoginRequest,
  RegisterRequest,
  LoginResponse
} from '@/types/api'

// 检查PyWebView API是否可用
function isApiAvailable(): boolean {
  return typeof window !== 'undefined' && 'pywebview' in window && !!window.pywebview?.api
}

// 安全调用PyWebView API
async function safeApiCall<T>(method: string, ...args: any[]): Promise<T> {
  if (!isApiAvailable()) {
    throw new Error('PyWebView API not available')
  }
  
  try {
    const api = window.pywebview!.api as any
    
    // 处理嵌套的API调用，如 'auth_api.login'
    const methodParts = method.split('.')
    let target = api
    
    // 遍历到最后一个属性之前
    for (let i = 0; i < methodParts.length - 1; i++) {
      target = target[methodParts[i]]
      if (!target) {
        throw new Error(`API module '${methodParts.slice(0, i + 1).join('.')}' not found`)
      }
    }
    
    // 获取最终的方法
    const finalMethod = methodParts[methodParts.length - 1]
    if (typeof target[finalMethod] !== 'function') {
      throw new Error(`API method '${method}' is not a function`)
    }
    
    return await target[finalMethod](...args)
  } catch (error) {
    console.error(`API call failed: ${method}`, error)
    throw error
  }
}

// 认证相关API
export const authApi = {
  /**
   * 用户登录
   */
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    try {
      if (isApiAvailable()) {
        // 调用Python后端API
        const result = await safeApiCall('auth_api.login', credentials.username, credentials.password)
        return result as ApiResponse<LoginResponse>
      } else {
        // 开发模式下的模拟登录
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        if (credentials.username === 'admin' && credentials.password === '123456') {
          return {
            success: true,
            data: {
              token: 'mock-jwt-token-admin-' + Date.now(),
              user: {
                id: '1',
                username: credentials.username,
                email: 'admin@example.com',
                avatar: 'https://via.placeholder.com/40'
              },
              expiresIn: 3600
            },
            message: '登录成功'
          }
        } else {
          return {
            success: false,
            data: null,
            message: '用户名或密码错误',
            error: '用户名或密码错误'
          }
        }
      }
    } catch (error) {
      return {
        success: false,
        data: null,
        message: '登录失败',
        error: error instanceof Error ? error.message : '网络错误'
      }
    }
  },

  /**
   * 用户注册
   */
  async register(userData: RegisterRequest): Promise<ApiResponse<LoginResponse>> {
    try {
      if (isApiAvailable()) {
         // 调用Python后端API
         const result = await safeApiCall('auth_api.register', userData.username, userData.email, userData.password, userData.confirmPassword)
         return result as ApiResponse<LoginResponse>
      } else {
        // 开发模式下的模拟注册
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        return {
          success: true,
          data: {
            token: 'mock-jwt-token',
            user: {
              id: '2',
              username: userData.username,
              email: userData.email,
              avatar: ''
            },
            expiresIn: 3600
          },
          message: '注册成功'
        }
      }
    } catch (error) {
      return {
        success: false,
        data: null,
        message: '注册失败',
        error: error instanceof Error ? error.message : '网络错误'
      }
    }
  },

  /**
   * 用户登出
   */
  async logout(): Promise<ApiResponse<{ message: string }>> {
    try {
      if (isApiAvailable()) {
        // 调用Python后端API
        const result = await safeApiCall('auth_api.logout')
        return result as ApiResponse<{ message: string }>
      } else {
        // 开发模式下的模拟登出
        await new Promise(resolve => setTimeout(resolve, 500))
        return {
          success: true,
          data: { message: '登出成功' },
          message: '登出成功'
        }
      }
    } catch (error) {
      return {
        success: false,
        data: null,
        message: '登出失败',
        error: error instanceof Error ? error.message : '网络错误'
      }
    }
  }
}

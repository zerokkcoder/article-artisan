import type {
  ApiResponse,
  LoginRequest,
  RegisterRequest,
  LoginResponse
} from '@/types/api'

// 认证相关API
export const authApi = {
  /**
   * 用户登录
   */
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    try {
      // 模拟 API 调用
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      if (credentials.username === 'admin' && credentials.password === 'admin') {
        return {
          success: true,
          data: {
            token: 'mock-jwt-token',
            user: {
              id: '1',
              username: credentials.username,
              email: 'admin@example.com',
              avatar: ''
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
      // 模拟 API 调用
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
      await new Promise(resolve => setTimeout(resolve, 500))
      return {
        success: true,
        data: { message: '登出成功' },
        message: '登出成功'
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

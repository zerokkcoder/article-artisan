/**
 * API 服务层
 * 封装与 PyWebView 后端的通信逻辑
 */

import type {
  ApiResponse,
  DataModel,
  SystemInfo,
  MessageResult
} from '@/types/env'
import { safeApiCall, isApiAvailable } from '@/utils'
import { APP_CONFIG } from '@/constants'

/**
 * API 服务类
 */
class ApiService {
  private timeout: number

  constructor(timeout: number = APP_CONFIG.DEFAULT_TIMEOUT) {
    this.timeout = timeout
  }

  /**
   * 检查 API 是否可用
   */
  isAvailable(): boolean {
    return isApiAvailable()
  }

  /**
   * 获取数据
   */
  async getData(): Promise<ApiResponse<DataModel>> {
    return safeApiCall(
      async () => {
        return await window.pywebview.api.get_data()
      },
      {
        success: false,
        data: {
          message: '模拟数据'
        },
        message: 'API 不可用，使用模拟数据'
      }
    )
  }

  /**
   * 获取系统信息
   */
  async getSystemInfo(): Promise<ApiResponse<SystemInfo>> {
    return safeApiCall(
      async () => {
        return await window.pywebview.api.get_system_info()
      },
      {
        success: false,
        data: {
          platform: 'unknown',
          python_version: '0.0.0',
          current_dir: '/unknown'
        },
        message: 'API 不可用，使用模拟数据'
      }
    )
  }

  /**
   * 发送消息
   */
  async sendMessage(message: string): Promise<ApiResponse<MessageResult>> {
    if (!message.trim()) {
      return {
        success: false,
        data: { success: false, message: '消息不能为空' },
        message: '消息不能为空'
      }
    }

    return safeApiCall(
      async () => {
        const result = await window.pywebview.api.set_message(message)
        return result
      },
      {
        success: false,
        data: {
          success: false,
          message: `模拟响应: ${message}`
        },
        message: 'API 不可用，使用模拟响应'
      }
    )
  }

  /**
   * 批量获取数据
   */
  async getBatchData(): Promise<{
    data: ApiResponse<DataModel>
    systemInfo: ApiResponse<SystemInfo>
  }> {
    const [data, systemInfo] = await Promise.all([
      this.getData(),
      this.getSystemInfo()
    ])

    return { data, systemInfo }
  }

  /**
   * 带重试的 API 调用
   */
  async callWithRetry<T>(
    apiCall: () => Promise<T>,
    maxRetries: number = APP_CONFIG.RETRY_ATTEMPTS
  ): Promise<T> {
    let lastError: Error

    for (let i = 0; i <= maxRetries; i++) {
      try {
        return await apiCall()
      } catch (error) {
        lastError = error as Error
        if (i < maxRetries) {
          // 指数退避策略
          const delay = Math.pow(2, i) * 1000
          await new Promise(resolve => setTimeout(resolve, delay))
        }
      }
    }

    throw lastError!
  }

  /**
   * 设置超时时间
   */
  setTimeout(timeout: number): void {
    this.timeout = timeout
  }

  /**
   * 获取当前超时时间
   */
  getTimeout(): number {
    return this.timeout
  }
}

// 创建单例实例
export const apiService = new ApiService()

// 导出类型
export type { ApiService }

// 导出便捷方法
export const {
  getData,
  getSystemInfo,
  sendMessage,
  getBatchData,
  isAvailable: checkApiAvailable
} = apiService

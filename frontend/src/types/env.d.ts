/// <reference types="vite/client" />

// 环境变量类型声明
interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_VERSION: string
  readonly VITE_DEV_SERVER_PORT: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_BUILD_OPTIMIZE: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// PyWebView API 类型声明
declare global {
  interface Window {
    pywebview: {
      api: {
        get_data: () => Promise<ApiResponse<DataModel>>
        set_message: (message: string) => Promise<ApiResponse<MessageResult>>
        get_system_info: () => Promise<ApiResponse<SystemInfo>>
      }
    }
  }
}

// API 响应类型
export interface ApiResponse<T = any> {
  success?: boolean
  message?: string
  data?: T
}

// 数据模型类型
export interface DataModel {
  message: string
  [key: string]: any
}

export interface MessageResult {
  success: boolean
  message: string
}

export interface SystemInfo {
  platform: string
  python_version: string
  current_dir: string
}

export {}

/// <reference types="vite/client" />

// PyWebView API类型定义
declare global {
  interface Window {
    pywebview?: {
      api: {
        login: (username: string, password: string) => Promise<any>
        register: (username: string, email: string, password: string, confirmPassword: string) => Promise<any>
        logout: () => Promise<any>
        get_current_user: () => Promise<any>
        get_data: () => Promise<any>
        set_message: (message: string) => Promise<any>
        get_system_info: () => Promise<any>
        [key: string]: (...args: any[]) => Promise<any>
      }
    }
  }
}
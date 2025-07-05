/**
 * 应用常量定义
 */

// API 相关常量
export const API_ENDPOINTS = {
  DATA: '/api/data',
  SYSTEM_INFO: '/api/system',
  MESSAGE: '/api/message'
} as const

// 消息类型
export const MESSAGE_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
} as const

// 应用配置
export const APP_CONFIG = {
  DEFAULT_TIMEOUT: 5000,
  RETRY_ATTEMPTS: 3,
  DEBOUNCE_DELAY: 300,
  THROTTLE_LIMIT: 1000
} as const

// 存储键名
export const STORAGE_KEYS = {
  USER_PREFERENCES: 'user_preferences',
  LAST_SESSION: 'last_session',
  CACHE_DATA: 'cache_data'
} as const

// 事件名称
export const EVENT_NAMES = {
  API_READY: 'api:ready',
  API_ERROR: 'api:error',
  DATA_UPDATED: 'data:updated',
  THEME_CHANGED: 'theme:changed'
} as const

// 主题配置
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
} as const

// 响应状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500
} as const

// 文件类型
export const FILE_TYPES = {
  IMAGE: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'],
  DOCUMENT: ['pdf', 'doc', 'docx', 'txt', 'md'],
  ARCHIVE: ['zip', 'rar', '7z', 'tar', 'gz']
} as const

// 正则表达式
export const REGEX_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^1[3-9]\d{9}$/,
  URL: /^https?:\/\/.+/,
  IPV4: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
} as const

// 类型定义
export type MessageType = (typeof MESSAGE_TYPES)[keyof typeof MESSAGE_TYPES]
export type Theme = (typeof THEMES)[keyof typeof THEMES]
export type HttpStatus = (typeof HTTP_STATUS)[keyof typeof HTTP_STATUS]

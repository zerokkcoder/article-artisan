export interface ApiResponse<T> {
  success: boolean
  data: T | null
  message: string
  error?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirmPassword: string
}

export interface User {
  id: string
  username: string
  email: string
  avatar?: string
}

export interface LoginResponse {
  user: User
  token: string
  expiresIn: number
}

export interface ErrorResponse {
  success: false
  message: string
  error: string
}
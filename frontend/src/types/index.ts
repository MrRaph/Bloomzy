export interface User {
  id: number
  email: string
  username: string
  bio?: string
  location?: string
  expertise_level?: string
  phone?: string
  preferred_units?: string
  notifications_enabled?: boolean
  avatar_url?: string
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  username: string
  recaptcha_token?: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}
import axios from 'axios'
import type { User, AuthTokens, LoginCredentials, SignupData } from '@/types'

const api = axios.create({
  baseURL: 'http://localhost:5001',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('http://localhost:5001/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })
          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)
          error.config.headers.Authorization = `Bearer ${access_token}`
          return api.request(error.config)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (credentials: LoginCredentials) => 
    api.post<AuthTokens>('/auth/login', credentials),
  
  signup: (data: SignupData) => 
    api.post<AuthTokens>('/auth/signup', data),
  
  logout: () => 
    api.post('/auth/logout'),
  
  getProfile: () => 
    api.get<User>('/auth/profile'),
  
  updateProfile: (data: Partial<User>) => 
    api.put<User>('/auth/profile', data),
  
  refreshToken: () => 
    api.post<{ access_token: string }>('/auth/refresh')
}

export default api
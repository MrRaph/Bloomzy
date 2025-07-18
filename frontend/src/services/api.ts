
import axios from 'axios'
import type { AuthTokens, User, LoginCredentials, SignupData } from '@/types'

// Configuration de l'URL de base de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

// Création d'une instance axios avec l'URL de base
const apiClient = axios.create({
  baseURL: API_BASE_URL
})

// Intercepteur pour ajouter le token JWT dans les headers Authorization
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

// Indoor Plants API
export const fetchIndoorPlants = async (search?: string): Promise<any[]> => {
  const params = search ? { search } : {}
  const res = await apiClient.get<any[]>('/indoor-plants/', { params })
  return res.data
}

export const createIndoorPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post('/indoor-plants/', payload)
  return res.data
}

export const authApi = {
  login: (credentials: LoginCredentials) => 
    apiClient.post<AuthTokens>('/auth/login', credentials),
  
  signup: (data: SignupData) => 
    apiClient.post<AuthTokens>('/auth/signup', data),
  
  logout: () => 
    apiClient.post('/auth/logout'),
  
  getProfile: () => 
    apiClient.get<User>('/auth/profile'),
  
  updateProfile: (data: Partial<User>) => 
    apiClient.put<User>('/auth/profile', data),
  
  refreshToken: () => 
    apiClient.post<{ access_token: string }>('/auth/refresh')
}

// export default supprimé car l'instance api n'est plus utilisée
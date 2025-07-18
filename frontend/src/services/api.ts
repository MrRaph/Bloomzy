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

// Indoor Plants API (Catalogue des espèces)
export const fetchIndoorPlants = async (search?: string): Promise<any[]> => {
  const params = search ? { search } : {}
  const res = await apiClient.get<any[]>('/indoor-plants/', { params })
  return res.data
}

export const createIndoorPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post('/indoor-plants/', payload)
  return res.data
}

export const updateIndoorPlant = async (id: number, payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.put(`/indoor-plants/${id}/`, payload)
  return res.data
}

export const deleteIndoorPlant = async (id: number): Promise<void> => {
  await apiClient.delete(`/indoor-plants/${id}/`)
}

// User Plants API (Mes plantes personnelles)
export const fetchMyPlants = async (): Promise<any> => {
  const res = await apiClient.get('/api/plants/my-plants')
  return res.data
}

export const createMyPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post('/api/plants/my-plants', payload)
  return res.data
}

export const getMyPlant = async (id: number): Promise<any> => {
  const res = await apiClient.get(`/api/plants/my-plants/${id}`)
  return res.data
}

export const updateMyPlant = async (id: number, payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.put(`/api/plants/my-plants/${id}`, payload)
  return res.data
}

export const deleteMyPlant = async (id: number): Promise<void> => {
  await apiClient.delete(`/api/plants/my-plants/${id}`)
}

export const uploadPlantPhoto = async (plantId: number, photo: File): Promise<any> => {
  const formData = new FormData()
  formData.append('photo', photo)
  const res = await apiClient.post(`/api/plants/my-plants/${plantId}/photo`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return res.data
}

// Watering API
export const recordWatering = async (payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post('/api/plants/watering', payload)
  return res.data
}

export const getWateringHistory = async (plantId: number): Promise<any> => {
  const res = await apiClient.get(`/api/plants/${plantId}/watering-history`)
  return res.data
}

export const getWateringSchedule = async (plantId: number): Promise<any> => {
  const res = await apiClient.get(`/api/plants/${plantId}/watering-schedule`)
  return res.data
}

// Auth API
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
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

export const getIndoorPlant = async (id: number): Promise<any> => {
  const res = await apiClient.get(`/indoor-plants/${id}/`)
  return res.data
}

// User Plants API (Mes plantes personnelles)
export const fetchMyPlants = async (): Promise<any> => {
  const res = await apiClient.get('/user-plants')
  return res.data
}

export const createMyPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post('/user-plants', payload)
  return res.data
}

export const getMyPlant = async (id: string): Promise<any> => {
  const res = await apiClient.get(`/user-plants/${id}`)
  return res.data
}

export const updateMyPlant = async (id: string, payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.put(`/user-plants/${id}`, payload)
  return res.data
}

export const deleteMyPlant = async (id: string): Promise<void> => {
  await apiClient.delete(`/user-plants/${id}`)
}

export const uploadPlantPhoto = async (plantId: string, photo: File): Promise<any> => {
  const formData = new FormData()
  formData.append('photo', photo)
  const res = await apiClient.post(`/user-plants/${plantId}/photo`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return res.data
}

// Watering API
export const recordWatering = async (plantId: string, payload: Record<string, any>): Promise<any> => {
  const res = await apiClient.post(`/user-plants/${plantId}/watering`, payload)
  return res.data
}

export const getWateringHistory = async (plantId: string): Promise<any> => {
  const res = await apiClient.get(`/user-plants/${plantId}/watering`)
  return res.data
}

export const getWateringSchedule = async (plantId: string): Promise<any> => {
  const res = await apiClient.get(`/user-plants/${plantId}/watering-schedule`)
  return res.data
}

// Notifications API
export const notificationsApi = {
  getNotifications: (params?: { status?: string; type?: string; limit?: number; offset?: number }) => 
    apiClient.get('/notifications', { params }),
  
  getNotification: (id: string) => 
    apiClient.get(`/notifications/${id}`),
  
  markAsOpened: (id: string) => 
    apiClient.post(`/notifications/${id}/mark-opened`),
  
  markAsActedUpon: (id: string, action: string) => 
    apiClient.post(`/notifications/${id}/mark-acted`, { action }),
  
  dismissNotification: (id: string) => 
    apiClient.post(`/notifications/${id}/dismiss`),
  
  cancelNotification: (id: string) => 
    apiClient.post(`/notifications/${id}/cancel`),
  
  getPreferences: () => 
    apiClient.get('/notifications/preferences'),
  
  updatePreferences: (preferences: any) => 
    apiClient.put('/notifications/preferences', { preferences }),
  
  scheduleNotification: (data: any) => 
    apiClient.post('/notifications/schedule', data),
  
  getAnalytics: (period_days?: number) => 
    apiClient.get('/notifications/analytics', { params: { period_days } }),
  
  sendTestNotification: (data: any) => 
    apiClient.post('/notifications/test', data)
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
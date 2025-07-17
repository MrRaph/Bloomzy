
import axios from 'axios'
import type { AuthTokens, User, LoginCredentials, SignupData } from '@/types'
// Utilisation directe d'axios pour faciliter le mock dans les tests

// Indoor Plants API
export const fetchIndoorPlants = async (search?: string): Promise<any[]> => {
  const params = search ? { search } : {}
  const res = await axios.get<any[]>('/indoor-plants/', { params })
  return res.data
}

export const createIndoorPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await axios.post('/indoor-plants/', payload)
  return res.data
}

export const authApi = {
  login: (credentials: LoginCredentials) => 
    axios.post<AuthTokens>('/auth/login', credentials),
  
  signup: (data: SignupData) => 
    axios.post<AuthTokens>('/auth/signup', data),
  
  logout: () => 
    axios.post('/auth/logout'),
  
  getProfile: () => 
    axios.get<User>('/auth/profile'),
  
  updateProfile: (data: Partial<User>) => 
    axios.put<User>('/auth/profile', data),
  
  refreshToken: () => 
    axios.post<{ access_token: string }>('/auth/refresh')
}

// export default supprimé car l'instance api n'est plus utilisée
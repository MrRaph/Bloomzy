
import axios from 'axios'
// Utilisation directe d'axios pour faciliter le mock dans les tests

// Indoor Plants API
export const fetchIndoorPlants = async (search?: string): Promise<any[]> => {
  const params = search ? { search } : {}
  const res = await axios.get('/indoor-plants/', { params })
  return res.data
}

export const createIndoorPlant = async (payload: Record<string, any>): Promise<any> => {
  const res = await axios.post('/indoor-plants/', payload)
  return res.data
}

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

// export default supprimé car l'instance api n'est plus utilisée
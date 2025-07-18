export interface IndoorPlant {
  id: number
  name: string
  species: string
  family?: string
  difficulty?: string
  created_at: string
  updated_at: string
}

export interface UserPlant {
  id: number
  user_id: number
  species_id: number
  custom_name: string
  location?: string
  pot_size?: string
  soil_type?: string
  acquired_date?: string
  current_photo_url?: string
  health_status: 'healthy' | 'sick' | 'dying' | 'dead'
  notes?: string
  light_exposure?: string
  local_humidity?: number
  ambient_temperature?: number
  last_repotting?: string
  created_at: string
  updated_at: string
  species?: {
    id: number
    scientific_name: string
    common_names: string
    family: string
    difficulty: string
  }
}

export interface WateringRecord {
  id: number
  plant_id: number
  watered_at: string
  amount_ml?: number
  water_type?: 'tap' | 'filtered' | 'rainwater' | 'distilled' | 'other'
  notes?: string
  created_at: string
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
  persistent?: boolean
}
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
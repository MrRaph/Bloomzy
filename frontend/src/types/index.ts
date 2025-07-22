export interface IndoorPlant {
  id: number
  scientific_name: string
  common_names?: string
  family?: string
  origin?: string
  difficulty?: string
  watering_frequency?: number
  light?: string
  humidity?: string
  temperature?: string
  soil_type?: string
  adult_size?: string
  growth_rate?: string
  toxicity?: string
  air_purification?: boolean
  flowering?: string
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
  username?: string
  first_name?: string
  last_name?: string
  bio?: string
  profile_picture?: string
  location?: string
  timezone?: string
  language?: string
  notifications_enabled?: boolean
  email_notifications?: boolean
  created_at: string
  updated_at: string
  is_active?: boolean
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

export interface ApiKey {
  id: number
  user_id: number
  service_name: 'openai' | 'claude' | 'gemini' | 'huggingface'
  key_name: string
  encrypted_key: string
  is_active: boolean
  created_at: string
  updated_at: string
  last_used_at?: string
}

export interface CreateApiKeyData {
  service_name: 'openai' | 'claude' | 'gemini' | 'huggingface'
  key_name: string
  api_key: string
}

export interface UpdateApiKeyData {
  key_name?: string
  api_key?: string
  is_active?: boolean
}

export interface GrowthEntry {
  id: number
  plant_id: number
  entry_date: string
  entry_type: 'photo' | 'measurement' | 'observation'
  photo_url?: string
  photo_description?: string
  height_cm?: number
  width_cm?: number
  leaf_count?: number
  stem_count?: number
  leaf_color?: 'green' | 'yellow' | 'brown' | 'red' | 'purple' | 'variegated'
  stem_firmness?: 'firm' | 'soft' | 'brittle'
  has_flowers: boolean
  has_fruits: boolean
  health_notes?: string
  growth_notes?: string
  user_observations?: string
  ai_health_score?: number
  ai_growth_analysis?: string
  ai_recommendations?: string
  created_at: string
  updated_at: string
}

export interface CreateGrowthEntryData {
  entry_type: 'photo' | 'measurement' | 'observation'
  entry_date?: string
  photo_description?: string
  height_cm?: number
  width_cm?: number
  leaf_count?: number
  stem_count?: number
  leaf_color?: 'green' | 'yellow' | 'brown' | 'red' | 'purple' | 'variegated'
  stem_firmness?: 'firm' | 'soft' | 'brittle'
  has_flowers?: boolean
  has_fruits?: boolean
  health_notes?: string
  growth_notes?: string
  user_observations?: string
}

export interface UpdateGrowthEntryData {
  entry_date?: string
  photo_description?: string
  height_cm?: number
  width_cm?: number
  leaf_count?: number
  stem_count?: number
  leaf_color?: 'green' | 'yellow' | 'brown' | 'red' | 'purple' | 'variegated'
  stem_firmness?: 'firm' | 'soft' | 'brittle'
  has_flowers?: boolean
  has_fruits?: boolean
  health_notes?: string
  growth_notes?: string
  user_observations?: string
}

export interface GrowthAnalytics {
  total_entries: number
  date_range: {
    start: string
    end: string
  }
  entry_types: Record<string, number>
  growth_trends: {
    height: Array<[string, number]>
    width: Array<[string, number]>
    leaf_count: Array<[string, number]>
  }
  health_trends: {
    ai_health_scores: Array<[string, number]>
    leaf_color_distribution: Record<string, number>
  }
  growth_rates?: {
    height_cm_per_day: number
    total_growth_cm: number
    growth_period_days: number
  }
}

export interface GrowthComparison {
  comparison_period_days: number
  first_entry: GrowthEntry | null
  last_entry: GrowthEntry | null
  changes: {
    height_cm?: number
    width_cm?: number
    leaf_count?: number
    ai_health_score?: number
  }
  photo_comparison?: {
    first_photo: string | null
    last_photo: string | null
  }
}
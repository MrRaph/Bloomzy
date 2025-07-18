import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/services/api'
import type { User, LoginCredentials, SignupData } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => {
    return !!user.value && !!localStorage.getItem('access_token')
  })

  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.login(credentials)
      const { access_token, refresh_token } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      await fetchProfile()
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur de connexion'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const signup = async (data: SignupData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.signup(data)
      const { access_token, refresh_token } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      
      await fetchProfile()
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'inscription'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  const fetchProfile = async () => {
    try {
      const response = await authApi.getProfile()
      user.value = response.data
    } catch (err) {
      console.error('Profile fetch error:', err)
      user.value = null
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authApi.updateProfile(data)
      user.value = response.data
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de la mise à jour du profil'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const refreshToken = async () => {
    try {
      const response = await authApi.refreshToken()
      localStorage.setItem('access_token', response.data.access_token)
      return true
    } catch (err) {
      return false
    }
  }

  const initializeAuth = async () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      await fetchProfile()
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    signup,
    logout,
    fetchProfile,
    updateProfile,
    initializeAuth,
    refreshToken
  }
})
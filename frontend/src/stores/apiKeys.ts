import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ApiKey, CreateApiKeyData, UpdateApiKeyData } from '@/types'
import { apiKeysApi } from '@/services/api'
import { useNotifications } from '@/composables/useNotifications'

export const useApiKeysStore = defineStore('apiKeys', () => {
  const apiKeys = ref<ApiKey[]>([])
  const supportedServices = ref<string[]>(['openai', 'claude', 'gemini', 'huggingface'])
  const isLoading = ref(false)
  const { showNotification } = useNotifications()

  // Actions
  const fetchApiKeys = async (): Promise<void> => {
    isLoading.value = true
    try {
      const response = await apiKeysApi.list()
      apiKeys.value = response.data
    } catch (error: any) {
      showNotification('Erreur lors du chargement des clés API', 'error')
      console.error('Fetch API keys error:', error)
    } finally {
      isLoading.value = false
    }
  }

  const createApiKey = async (data: CreateApiKeyData): Promise<boolean> => {
    isLoading.value = true
    try {
      const response = await apiKeysApi.create(data)
      apiKeys.value.push(response.data)
      showNotification(`Clé API "${data.key_name}" créée avec succès`, 'success')
      return true
    } catch (error: any) {
      const message = error.response?.data?.error || 'Erreur lors de la création de la clé API'
      showNotification(message, 'error')
      console.error('Create API key error:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  const updateApiKey = async (id: number, data: UpdateApiKeyData): Promise<boolean> => {
    isLoading.value = true
    try {
      const response = await apiKeysApi.update(id, data)
      const index = apiKeys.value.findIndex(key => key.id === id)
      if (index !== -1) {
        apiKeys.value[index] = response.data
      }
      showNotification('Clé API mise à jour avec succès', 'success')
      return true
    } catch (error: any) {
      const message = error.response?.data?.error || 'Erreur lors de la mise à jour de la clé API'
      showNotification(message, 'error')
      console.error('Update API key error:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  const deleteApiKey = async (id: number): Promise<boolean> => {
    isLoading.value = true
    try {
      await apiKeysApi.delete(id)
      apiKeys.value = apiKeys.value.filter(key => key.id !== id)
      showNotification('Clé API supprimée avec succès', 'success')
      return true
    } catch (error: any) {
      const message = error.response?.data?.error || 'Erreur lors de la suppression de la clé API'
      showNotification(message, 'error')
      console.error('Delete API key error:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  const testApiKey = async (id: number): Promise<boolean> => {
    isLoading.value = true
    try {
      const response = await apiKeysApi.test(id)
      const result = response.data
      if (result.success) {
        showNotification('Test de la clé API réussi', 'success')
        return true
      } else {
        showNotification(`Échec du test: ${result.message}`, 'error')
        return false
      }
    } catch (error: any) {
      const message = error.response?.data?.error || 'Erreur lors du test de la clé API'
      showNotification(message, 'error')
      console.error('Test API key error:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  const toggleApiKeyStatus = async (id: number): Promise<void> => {
    const apiKey = apiKeys.value.find(key => key.id === id)
    if (apiKey) {
      await updateApiKey(id, { is_active: !apiKey.is_active })
    }
  }

  const fetchSupportedServices = async (): Promise<void> => {
    try {
      const response = await apiKeysApi.getSupportedServices()
      supportedServices.value = response.data
    } catch (error) {
      console.error('Fetch supported services error:', error)
      // Utiliser les services par défaut en cas d'erreur
    }
  }

  // Getters
  const getApiKeysByService = (serviceName: string): ApiKey[] => {
    return apiKeys.value.filter(key => key.service_name === serviceName)
  }

  const getActiveApiKeys = (): ApiKey[] => {
    return apiKeys.value.filter(key => key.is_active)
  }

  const getApiKeyById = (id: number): ApiKey | undefined => {
    return apiKeys.value.find(key => key.id === id)
  }

  // Actions d'initialisation
  const init = async (): Promise<void> => {
    await Promise.all([
      fetchApiKeys(),
      fetchSupportedServices()
    ])
  }

  return {
    // State
    apiKeys,
    supportedServices,
    isLoading,
    
    // Actions
    fetchApiKeys,
    createApiKey,
    updateApiKey,
    deleteApiKey,
    testApiKey,
    toggleApiKeyStatus,
    fetchSupportedServices,
    init,
    
    // Getters
    getApiKeysByService,
    getActiveApiKeys,
    getApiKeyById
  }
})
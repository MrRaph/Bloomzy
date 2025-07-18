import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  fetchMyPlants, 
  createMyPlant, 
  updateMyPlant, 
  deleteMyPlant,
  uploadPlantPhoto,
  recordWatering,
  getWateringHistory,
  getWateringSchedule
} from '@/services/api'
import type { UserPlant, WateringRecord } from '@/types'

export const useMyPlantsStore = defineStore('myPlants', () => {
  const plants = ref<UserPlant[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const healthyPlants = computed(() => 
    plants.value.filter(plant => plant.health_status === 'healthy')
  )

  const plantsNeedingAttention = computed(() => 
    plants.value.filter(plant => plant.health_status !== 'healthy')
  )

  const fetchPlants = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetchMyPlants()
      plants.value = response.plants || []
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors du chargement des plantes'
    } finally {
      isLoading.value = false
    }
  }

  const addPlant = async (plantData: Omit<UserPlant, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newPlant = await createMyPlant(plantData)
      plants.value.unshift(newPlant)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'ajout de la plante'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const updatePlant = async (id: number, plantData: Partial<UserPlant>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedPlant = await updateMyPlant(id, plantData)
      const index = plants.value.findIndex(plant => plant.id === id)
      if (index !== -1) {
        plants.value[index] = updatedPlant
      }
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de la mise à jour de la plante'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const deletePlant = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await deleteMyPlant(id)
      plants.value = plants.value.filter(plant => plant.id !== id)
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de la suppression de la plante'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const uploadPhoto = async (plantId: number, photo: File) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await uploadPlantPhoto(plantId, photo)
      // Met à jour l'URL de la photo dans la plante locale
      const plant = plants.value.find(p => p.id === plantId)
      if (plant) {
        plant.current_photo_url = response.photo_url
      }
      return response
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'upload de la photo'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const addWatering = async (wateringData: Omit<WateringRecord, 'id' | 'created_at'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newWatering = await recordWatering(wateringData)
      return newWatering
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors de l\'enregistrement de l\'arrosage'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getPlantWateringHistory = async (plantId: number) => {
    try {
      const response = await getWateringHistory(plantId)
      return response.watering_history || []
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors du chargement de l\'historique'
      return []
    }
  }

  const getPlantWateringSchedule = async (plantId: number) => {
    try {
      const schedule = await getWateringSchedule(plantId)
      return schedule
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Erreur lors du chargement du planning'
      return null
    }
  }

  return {
    plants,
    isLoading,
    error,
    healthyPlants,
    plantsNeedingAttention,
    fetchPlants,
    addPlant,
    updatePlant,
    deletePlant,
    uploadPhoto,
    addWatering,
    getPlantWateringHistory,
    getPlantWateringSchedule
  }
})

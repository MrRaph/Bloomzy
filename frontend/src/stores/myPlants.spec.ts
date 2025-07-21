import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMyPlantsStore } from '@/stores/myPlants'

// Mock des services API
vi.mock('@/services/api', () => ({
  fetchMyPlants: vi.fn(),
  createMyPlant: vi.fn(),
  updateMyPlant: vi.fn(),
  deleteMyPlant: vi.fn(),
  uploadPlantPhoto: vi.fn(),
  recordWatering: vi.fn(),
  getWateringHistory: vi.fn(),
  getWateringSchedule: vi.fn()
}))

const mockUserPlant = {
  id: 1,
  user_id: 1,
  species_id: 1,
  custom_name: 'Mon Ficus',
  location: 'Salon',
  health_status: 'healthy' as const,
  created_at: '2023-01-01',
  updated_at: '2023-01-01',
  species: {
    id: 1,
    scientific_name: 'Ficus benjamina',
    common_names: 'Ficus pleureur',
    family: 'Moraceae',
    difficulty: 'Facile'
  }
}

const mockPlantResponse = {
  plants: [mockUserPlant],
  total: 1
}

describe('MyPlants Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('fetchPlants', () => {
    it('charge les plantes de l\'utilisateur', async () => {
      const { fetchMyPlants } = await import('@/services/api')
      vi.mocked(fetchMyPlants).mockResolvedValue(mockPlantResponse)

      const store = useMyPlantsStore()
      await store.fetchPlants()

      expect(store.plants).toEqual(mockPlantResponse.plants)
      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
    })

    it('gère les erreurs de chargement', async () => {
      const { fetchMyPlants } = await import('@/services/api')
      vi.mocked(fetchMyPlants).mockRejectedValue(new Error('Network error'))

      const store = useMyPlantsStore()
      await store.fetchPlants()

      expect(store.plants).toEqual([])
      expect(store.error).toBeTruthy()
    })
  })

  describe('addPlant', () => {
    it('ajoute une nouvelle plante', async () => {
      const { createMyPlant } = await import('@/services/api')
      vi.mocked(createMyPlant).mockResolvedValue(mockUserPlant)

      const store = useMyPlantsStore()
      const plantData = {
        species_id: 1,
        custom_name: 'Mon Ficus',
        location: 'Salon',
        health_status: 'healthy' as const
      }

      const result = await store.addPlant(plantData)

      expect(result).toBe(true)
      expect(store.plants).toHaveLength(1)
      expect(store.plants[0]).toEqual(mockUserPlant)
      expect(createMyPlant).toHaveBeenCalledWith(plantData)
    })

    it('gère les erreurs d\'ajout', async () => {
      const { createMyPlant } = await import('@/services/api')
      vi.mocked(createMyPlant).mockRejectedValue(new Error('Validation error'))

      const store = useMyPlantsStore()
      const result = await store.addPlant({
        species_id: 1,
        custom_name: 'Test',
        health_status: 'healthy'
      })

      expect(result).toBe(false)
      expect(store.error).toBeTruthy()
    })
  })

  describe('updatePlant', () => {
    it('met à jour une plante existante', async () => {
      const { updateMyPlant } = await import('@/services/api')
      const updatedPlant = { ...mockUserPlant, custom_name: 'Ficus modifié' }
      vi.mocked(updateMyPlant).mockResolvedValue(updatedPlant)

      const store = useMyPlantsStore()
      store.plants = [mockUserPlant]

      const result = await store.updatePlant(1, { custom_name: 'Ficus modifié' })

      expect(result).toBe(true)
      expect(store.plants[0].custom_name).toBe('Ficus modifié')
    })
  })

  describe('deletePlant', () => {
    it('supprime une plante', async () => {
      const { deleteMyPlant } = await import('@/services/api')
      vi.mocked(deleteMyPlant).mockResolvedValue()

      const store = useMyPlantsStore()
      store.plants = [mockUserPlant]

      const result = await store.deletePlant(1)

      expect(result).toBe(true)
      expect(store.plants).toHaveLength(0)
    })
  })

  describe('computed properties', () => {
    it('calcule correctement les plantes en bonne santé', () => {
      const store = useMyPlantsStore()
      store.plants = [
        { ...mockUserPlant, health_status: 'healthy' },
        { ...mockUserPlant, id: 2, health_status: 'sick' }
      ]

      expect(store.healthyPlants).toHaveLength(1)
      expect(store.healthyPlants[0].health_status).toBe('healthy')
    })

    it('calcule correctement les plantes nécessitant attention', () => {
      const store = useMyPlantsStore()
      store.plants = [
        { ...mockUserPlant, health_status: 'healthy' },
        { ...mockUserPlant, id: 2, health_status: 'sick' },
        { ...mockUserPlant, id: 3, health_status: 'dying' }
      ]

      expect(store.plantsNeedingAttention).toHaveLength(2)
    })
  })

  describe('watering functionality', () => {
    it('enregistre un arrosage', async () => {
      const { recordWatering } = await import('@/services/api')
      const wateringRecord = {
        id: 1,
        plant_id: 1,
        watered_at: '2023-01-01',
        amount_ml: 250,
        water_type: 'tap' as const,
        created_at: '2023-01-01'
      }
      vi.mocked(recordWatering).mockResolvedValue(wateringRecord)

      const store = useMyPlantsStore()
      const result = await store.addWatering({
        plant_id: 1,
        amount_ml: 250,
        water_type: 'tap',
        watered_at: '2023-01-01'
      })

      expect(result).toEqual(wateringRecord)
      expect(recordWatering).toHaveBeenCalled()
    })

    it('récupère l\'historique d\'arrosage', async () => {
      const { getWateringHistory } = await import('@/services/api')
      const history = {
        plant_id: 1,
        watering_history: [
          {
            id: 1,
            plant_id: 1,
            watered_at: '2023-01-01',
            amount_ml: 250,
            created_at: '2023-01-01'
          }
        ],
        total: 1
      }
      vi.mocked(getWateringHistory).mockResolvedValue(history)

      const store = useMyPlantsStore()
      const result = await store.getPlantWateringHistory(1)

      expect(result).toEqual(history.watering_history)
    })
  })
})

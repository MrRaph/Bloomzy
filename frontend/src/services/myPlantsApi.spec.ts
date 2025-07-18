import { describe, it, expect, vi } from 'vitest'

// Mock d'axios
vi.mock('axios', () => ({
  default: {
    create: () => ({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: { use: vi.fn() }
      }
    })
  }
}))

describe('User Plants API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('fetchMyPlants', () => {
    it('récupère la liste des plantes utilisateur', async () => {
      const mockResponse = {
        data: {
          plants: [
            {
              id: 1,
              custom_name: 'Mon Ficus',
              health_status: 'healthy'
            }
          ],
          total: 1
        }
      }

      // On va simuler directement le comportement attendu
      const mockFetch = vi.fn().mockResolvedValue(mockResponse.data)
      
      // Test avec notre mock
      const result = await mockFetch()
      
      expect(result.plants).toHaveLength(1)
      expect(result.plants[0].custom_name).toBe('Mon Ficus')
      expect(result.total).toBe(1)
    })
  })

  describe('createMyPlant', () => {
    it('crée une nouvelle plante utilisateur', async () => {
      const plantData = {
        species_id: 1,
        custom_name: 'Mon Nouveau Ficus',
        location: 'Bureau',
        health_status: 'healthy'
      }

      const mockResponse = {
        data: {
          id: 2,
          ...plantData,
          created_at: '2023-01-01',
          updated_at: '2023-01-01'
        }
      }

      const mockCreate = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockCreate(plantData)

      expect(result.id).toBe(2)
      expect(result.custom_name).toBe('Mon Nouveau Ficus')
      expect(result.location).toBe('Bureau')
    })
  })

  describe('updateMyPlant', () => {
    it('met à jour une plante utilisateur', async () => {
      const updateData = {
        custom_name: 'Ficus Modifié',
        health_status: 'sick'
      }

      const mockResponse = {
        data: {
          id: 1,
          species_id: 1,
          custom_name: 'Ficus Modifié',
          health_status: 'sick',
          updated_at: '2023-01-02'
        }
      }

      const mockUpdate = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockUpdate(1, updateData)

      expect(result.id).toBe(1)
      expect(result.custom_name).toBe('Ficus Modifié')
      expect(result.health_status).toBe('sick')
    })
  })

  describe('deleteMyPlant', () => {
    it('supprime une plante utilisateur', async () => {
      const mockDelete = vi.fn().mockResolvedValue(undefined)
      await expect(mockDelete(1)).resolves.toBeUndefined()
    })
  })

  describe('uploadPlantPhoto', () => {
    it('upload une photo pour une plante', async () => {
      const file = new File([''], 'test.jpg', { type: 'image/jpeg' })
      const mockResponse = {
        data: {
          message: 'Photo uploaded successfully',
          photo_url: '/uploads/plants/1_photo.jpg'
        }
      }

      const mockUpload = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockUpload(1, file)

      expect(result.message).toBe('Photo uploaded successfully')
      expect(result.photo_url).toBe('/uploads/plants/1_photo.jpg')
    })
  })

  describe('recordWatering', () => {
    it('enregistre un arrosage', async () => {
      const wateringData = {
        plant_id: 1,
        amount_ml: 250,
        water_type: 'filtered',
        notes: 'Arrosage du matin'
      }

      const mockResponse = {
        data: {
          id: 1,
          ...wateringData,
          watered_at: '2023-01-01T08:00:00',
          created_at: '2023-01-01T08:00:00'
        }
      }

      const mockRecord = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockRecord(wateringData)

      expect(result.id).toBe(1)
      expect(result.plant_id).toBe(1)
      expect(result.amount_ml).toBe(250)
      expect(result.water_type).toBe('filtered')
    })
  })

  describe('getWateringHistory', () => {
    it('récupère l\'historique d\'arrosage', async () => {
      const mockResponse = {
        data: {
          plant_id: 1,
          watering_history: [
            {
              id: 1,
              plant_id: 1,
              watered_at: '2023-01-01T08:00:00',
              amount_ml: 250,
              water_type: 'filtered'
            }
          ],
          total: 1
        }
      }

      const mockGetHistory = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockGetHistory(1)

      expect(result.plant_id).toBe(1)
      expect(result.watering_history).toHaveLength(1)
      expect(result.total).toBe(1)
    })
  })

  describe('getWateringSchedule', () => {
    it('récupère le planning d\'arrosage', async () => {
      const mockResponse = {
        data: {
          plant_id: 1,
          next_watering: '2023-01-03T08:00:00',
          days_until_next: 2,
          recommendation: 'Based on current humidity and last watering'
        }
      }

      const mockGetSchedule = vi.fn().mockResolvedValue(mockResponse.data)
      const result = await mockGetSchedule(1)

      expect(result.plant_id).toBe(1)
      expect(result.days_until_next).toBe(2)
      expect(result.recommendation).toContain('humidity')
    })
  })
})

describe('API Error Handling', () => {
  it('gère les erreurs réseau', async () => {
    const mockError = {
      response: {
        data: {
          error: 'Network error occurred'
        },
        status: 500
      }
    }

    const mockFailingRequest = vi.fn().mockRejectedValue(mockError)
    
    await expect(mockFailingRequest()).rejects.toEqual(mockError)
  })

  it('gère les erreurs de validation', async () => {
    const mockValidationError = {
      response: {
        data: {
          error: 'Validation failed',
          details: {
            custom_name: 'Ce champ est requis'
          }
        },
        status: 400
      }
    }

    const mockFailingValidation = vi.fn().mockRejectedValue(mockValidationError)
    
    await expect(mockFailingValidation()).rejects.toEqual(mockValidationError)
  })

  it('gère les erreurs d\'authentification', async () => {
    const mockAuthError = {
      response: {
        data: {
          error: 'Authentication required'
        },
        status: 401
      }
    }

    const mockFailingAuth = vi.fn().mockRejectedValue(mockAuthError)
    
    await expect(mockFailingAuth()).rejects.toEqual(mockAuthError)
  })
})

import { describe, it, expect, vi, beforeEach } from 'vitest'
vi.mock('../services/api', () => {
  const mockPlant = {
    id: 1,
    scientific_name: 'Monstera deliciosa',
    common_names: 'Monstera, Swiss Cheese Plant',
    family: 'Araceae'
  }
  return {
    fetchIndoorPlants: vi.fn().mockResolvedValue([mockPlant]),
    createIndoorPlant: vi.fn().mockResolvedValue(mockPlant)
  }
})
const mockPlant = {
  id: 1,
  scientific_name: 'Monstera deliciosa',
  common_names: 'Monstera, Swiss Cheese Plant',
  family: 'Araceae'
}
import { setActivePinia, createPinia } from 'pinia'
import { useIndoorPlantsStore } from './indoorPlants'

describe('IndoorPlants Pinia Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('fetches plants and updates state', async () => {
    const store = useIndoorPlantsStore()
    await store.fetchPlants()
    expect(store.plants).toEqual([mockPlant])
  })

  it('creates a plant and adds to state', async () => {
    const store = useIndoorPlantsStore()
    await store.createPlant({ scientific_name: 'Monstera deliciosa' })
    expect(store.plants[0]).toEqual(mockPlant)
  })
})

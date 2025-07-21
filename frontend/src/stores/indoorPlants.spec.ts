import { describe, it, expect, vi, beforeEach } from 'vitest'
vi.mock('../services/api', () => {
  const mockPlant = {
    id: 1,
    scientific_name: 'Monstera deliciosa',
    common_names: 'Monstera',
    created_at: '',
    updated_at: ''
  }
  return {
    fetchIndoorPlants: vi.fn().mockResolvedValue([mockPlant]),
    createIndoorPlant: vi.fn().mockResolvedValue(mockPlant),
    updateIndoorPlant: vi.fn().mockImplementation((_id, payload) => Promise.resolve({ ...mockPlant, ...payload })),
    deleteIndoorPlant: vi.fn().mockResolvedValue(undefined)
  }
})
const mockPlant = {
  id: 1,
  scientific_name: 'Monstera deliciosa',
  common_names: 'Monstera',
  created_at: '',
  updated_at: ''
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

  it('addPlant ajoute une plante', async () => {
    const store = useIndoorPlantsStore()
    await store.addPlant({ scientific_name: 'Monstera deliciosa', common_names: 'Monstera' })
    expect(store.plants[0]).toEqual(mockPlant)
  })

  it('updatePlant modifie une plante', async () => {
    const store = useIndoorPlantsStore()
    store.plants = [mockPlant]
    await store.updatePlant(1, { common_names: 'Ficus' })
    expect(store.plants[0].common_names).toBe('Ficus')
  })

  it('deletePlant supprime une plante', async () => {
    const store = useIndoorPlantsStore()
    store.plants = [mockPlant]
    await store.deletePlant(1)
    expect(store.plants.length).toBe(0)
  })
})

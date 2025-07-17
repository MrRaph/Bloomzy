import { describe, it, expect, vi } from 'vitest'
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))
import { fetchIndoorPlants, createIndoorPlant } from './api'
import axios from 'axios'

const mockPlant = {
  id: 1,
  scientific_name: 'Monstera deliciosa',
  common_names: 'Monstera, Swiss Cheese Plant',
  family: 'Araceae'
}

describe('IndoorPlants API service', () => {
  it('fetches the list of indoor plants', async () => {
    (axios.get as any).mockResolvedValue({ data: [mockPlant] })
    const plants = await fetchIndoorPlants()
    expect(plants).toEqual([mockPlant])
  })

  it('creates a new indoor plant', async () => {
    (axios.post as any).mockResolvedValue({ data: mockPlant })
    const plant = await createIndoorPlant({ scientific_name: 'Monstera deliciosa' })
    expect(plant).toEqual(mockPlant)
  })
})

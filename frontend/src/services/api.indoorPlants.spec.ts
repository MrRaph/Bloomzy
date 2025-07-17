import { describe, it, expect, vi } from 'vitest'

// Mock axios et axios.create
vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn()
    }))
  }
}))

import { fetchIndoorPlants, createIndoorPlant } from './api'
import axios from 'axios'

const mockAxiosInstance = {
  get: vi.fn(),
  post: vi.fn()
}

// Mock axios.create pour retourner notre instance mockée
vi.mocked(axios.create).mockReturnValue(mockAxiosInstance as any)

const mockPlant = {
  id: 1,
  scientific_name: 'Monstera deliciosa',
  common_names: 'Monstera, Swiss Cheese Plant',
  family: 'Araceae'
}

describe('IndoorPlants API service', () => {
  it('fetches the list of indoor plants', async () => {
    mockAxiosInstance.get.mockResolvedValue({ data: [mockPlant] })
    const plants = await fetchIndoorPlants()
    expect(plants).toEqual([mockPlant])
  })

  it('creates a new indoor plant', async () => {
    mockAxiosInstance.post.mockResolvedValue({ data: mockPlant })
    const plant = await createIndoorPlant({ scientific_name: 'Monstera deliciosa' })
    expect(plant).toEqual(mockPlant)
  })
})

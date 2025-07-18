import { describe, it, expect, vi } from 'vitest'
import { fetchIndoorPlants, createIndoorPlant } from '@/services/api'

vi.mock('axios', () => ({
  default: {
    create: () => ({
      get: vi.fn().mockResolvedValue({ data: [{ id: 1, name: 'Ficus' }] }),
      post: vi.fn().mockResolvedValue({ data: { id: 2, name: 'Monstera' } })
    })
  }
}))

describe('fetchIndoorPlants', () => {
  it('retourne la liste des plantes', async () => {
    const res = await fetchIndoorPlants()
    expect(Array.isArray(res)).toBe(true)
    expect(res[0].name).toBe('Ficus')
  })
  it('accepte un paramètre de recherche', async () => {
    const res = await fetchIndoorPlants('ficus')
    expect(res[0].name).toBe('Ficus')
  })
})

describe('createIndoorPlant', () => {
  it('crée une plante et retourne ses infos', async () => {
    const res = await createIndoorPlant({ name: 'Monstera' })
    expect(res.name).toBe('Monstera')
  })
})

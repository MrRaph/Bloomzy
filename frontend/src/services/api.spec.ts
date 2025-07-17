import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as api from './api'
import axios from 'axios'

vi.mock('axios')

const mockPlants = [
  { id: 1, name: 'Monstera', type: 'indoor' },
  { id: 2, name: 'Ficus', type: 'indoor' }
]

describe('Indoor Plants API service', () => {
  describe('fetchIndoorPlants', () => {
    beforeEach(() => {
      vi.clearAllMocks()
    })

    it('retourne la liste des plantes', async () => {
      vi.spyOn(axios, 'get').mockResolvedValue({
        data: [
          { id: 1, name: 'Monstera', type: 'indoor' },
          { id: 2, name: 'Ficus', type: 'indoor' }
        ],
        status: 200,
        statusText: 'OK',
        headers: {},
        config: { url: '/indoor-plants/' }
      })
      const result = await api.fetchIndoorPlants()
      expect(result).toEqual([
        { id: 1, name: 'Monstera', type: 'indoor' },
        { id: 2, name: 'Ficus', type: 'indoor' }
      ])
      expect(axios.get).toHaveBeenCalledWith('/indoor-plants/', { params: {} })
    })

    it('utilise le paramètre de recherche', async () => {
      vi.spyOn(axios, 'get').mockResolvedValue({
        data: [
          { id: 1, name: 'Monstera', type: 'indoor' },
          { id: 2, name: 'Ficus', type: 'indoor' }
        ],
        status: 200,
        statusText: 'OK',
        headers: {},
        config: { url: '/indoor-plants/' }
      })
      await api.fetchIndoorPlants('monstera')
      expect(axios.get).toHaveBeenCalledWith('/indoor-plants/', { params: { search: 'monstera' } })
    })
  })

  describe('createIndoorPlant', () => {
    beforeEach(() => {
      vi.clearAllMocks()
    })

    it('crée une plante', async () => {
      const payload = { name: 'Aloe Vera', type: 'indoor' }
      vi.spyOn(axios, 'post').mockResolvedValue({
        data: { id: 3, ...payload },
        status: 201,
        statusText: 'Created',
        headers: {},
        config: { url: '/indoor-plants/' }
      })
      const result = await api.createIndoorPlant(payload)
      expect(result).toEqual({ id: 3, ...payload })
      expect(axios.post).toHaveBeenCalledWith('/indoor-plants/', payload)
    })
  })
})

describe('authApi', () => {
  const tokens = { access_token: 'token', refresh_token: 'refresh' }
  const user = { id: 1, username: 'test', email: 'test@test.com' }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('login retourne les tokens', async () => {
    vi.spyOn(axios, 'post').mockResolvedValue({
      data: tokens,
      status: 200,
      statusText: 'OK',
      headers: {},
      config: { url: '/auth/login' }
    })
    const result = await api.authApi.login({ email: 'test@test.com', password: 'pass' })
    expect(result.data).toEqual(tokens)
    expect(axios.post).toHaveBeenCalledWith('/auth/login', { email: 'test@test.com', password: 'pass' })
  })

  it('signup retourne les tokens', async () => {
    vi.spyOn(axios, 'post').mockResolvedValue({
      data: tokens,
      status: 201,
      statusText: 'Created',
      headers: {},
      config: { url: '/auth/signup' }
    })
    const result = await api.authApi.signup({ username: 'test', email: 'test@test.com', password: 'pass' })
    expect(result.data).toEqual(tokens)
    expect(axios.post).toHaveBeenCalledWith('/auth/signup', { username: 'test', email: 'test@test.com', password: 'pass' })
  })

  it('logout appelle le bon endpoint', async () => {
    vi.spyOn(axios, 'post').mockResolvedValue({
      data: {},
      status: 200,
      statusText: 'OK',
      headers: {},
      config: { url: '/auth/logout' }
    })
    await api.authApi.logout()
    expect(axios.post).toHaveBeenCalledWith('/auth/logout')
  })

  it('getProfile retourne le user', async () => {
    vi.spyOn(axios, 'get').mockResolvedValue({
      data: user,
      status: 200,
      statusText: 'OK',
      headers: {},
      config: { url: '/auth/profile' }
    })
    const result = await api.authApi.getProfile()
    expect(result.data).toEqual(user)
    expect(axios.get).toHaveBeenCalledWith('/auth/profile')
  })

  it('updateProfile met à jour le user', async () => {
    vi.spyOn(axios, 'put').mockResolvedValue({
      data: user,
      status: 200,
      statusText: 'OK',
      headers: {},
      config: { url: '/auth/profile' }
    })
    const result = await api.authApi.updateProfile({ username: 'new' })
    expect(result.data).toEqual(user)
    expect(axios.put).toHaveBeenCalledWith('/auth/profile', { username: 'new' })
  })

  it('refreshToken retourne le nouvel access_token', async () => {
    vi.spyOn(axios, 'post').mockResolvedValue({
      data: { access_token: 'newtoken' },
      status: 200,
      statusText: 'OK',
      headers: {},
      config: { url: '/auth/refresh' }
    })
    const result = await api.authApi.refreshToken()
    expect(result.data).toEqual({ access_token: 'newtoken' })
    expect(axios.post).toHaveBeenCalledWith('/auth/refresh')
  })
})

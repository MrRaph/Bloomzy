// Mock localStorage pour Vitest (Node.js)
class LocalStorageMock {
  store: Record<string, string> = {}
  get length() { return Object.keys(this.store).length }
  clear() { this.store = {} }
  getItem(key: string) { return this.store[key] || null }
  setItem(key: string, value: string) { this.store[key] = value }
  removeItem(key: string) { delete this.store[key] }
  key(index: number) { return Object.keys(this.store)[index] || null }
}
globalThis.localStorage = new LocalStorageMock()
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from './auth'

vi.mock('../services/api', () => {
  const mockTokens = { access_token: 'token', refresh_token: 'refresh' }
  const mockUser = { id: 1, username: 'test', email: 'test@test.com' }
  return {
    authApi: {
      login: vi.fn().mockResolvedValue({ data: mockTokens }),
      logout: vi.fn().mockResolvedValue({}),
      getProfile: vi.fn().mockResolvedValue({ data: mockUser })
    }
  }
})

describe('Auth Pinia Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })


  it('logs in and sets tokens in localStorage', async () => {
    const store = useAuthStore()
    await store.login({ email: 'test@test.com', password: 'pass' })
    expect(localStorage.getItem('access_token')).toBe('token')
    expect(localStorage.getItem('refresh_token')).toBe('refresh')
    expect(store.user).toEqual({ id: 1, username: 'test', email: 'test@test.com' })
  })

  it('logs out and clears tokens in localStorage', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'token')
    localStorage.setItem('refresh_token', 'refresh')
    await store.logout()
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(store.user).toBeNull()
  })

  it('fetches user profile', async () => {
    const store = useAuthStore()
    await store.fetchProfile()
    expect(store.user).toEqual({ id: 1, username: 'test', email: 'test@test.com' })
  })
})

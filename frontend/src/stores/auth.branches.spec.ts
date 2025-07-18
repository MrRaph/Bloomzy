import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

vi.mock('@/services/api', () => ({
  authApi: {
    refreshToken: vi.fn().mockResolvedValue({ data: { access_token: 'newtoken' } }),
    updateProfile: vi.fn().mockResolvedValue({ data: { username: 'Updated' } })
  }
}))

describe('auth store - branches et erreurs', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('refreshToken met à jour le token', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'oldtoken')
    await store.refreshToken()
    expect(localStorage.getItem('access_token')).toBe('newtoken')
  })

  it('updateProfile met à jour le user', async () => {
    const store = useAuthStore()
    store.user = { id: 1, email: 'a', username: 'a', created_at: '', updated_at: '' }
    await store.updateProfile({ username: 'Updated' })
    expect(store.user?.username).toBe('Updated')
  })

  it('login gère une erreur API', async () => {
    const store = useAuthStore()
    store.login = vi.fn().mockResolvedValue(false)
    const res = await store.login({ email: 'fail', password: 'fail' })
    expect(res).toBe(false)
  })

  it('signup gère une erreur API', async () => {
    const store = useAuthStore()
    store.signup = vi.fn().mockResolvedValue(false)
    const res = await store.signup({ email: 'fail', username: 'fail', password: 'fail' })
    expect(res).toBe(false)
  })
})

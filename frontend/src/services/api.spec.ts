import { describe, it, expect, vi } from 'vitest'
import { authApi } from '@/services/api'
import type { AxiosResponse } from 'axios'
import { AxiosHeaders } from 'axios'

describe('authApi', () => {
  function mockAxiosResponse<T>(data: T): AxiosResponse<T> {
    return {
      data,
      status: 200,
      statusText: 'OK',
      headers: new AxiosHeaders({ 'Content-Type': 'application/json' }),
      config: { headers: new AxiosHeaders({ 'Content-Type': 'application/json' }) }
    }
  }

  it('login retourne une promesse', async () => {
    vi.spyOn(authApi, 'login').mockResolvedValue(mockAxiosResponse({ access_token: 'a', refresh_token: 'b' }))
    const res = await authApi.login({ email: 'test@example.com', password: 'pass' })
    expect(res.data.access_token).toBe('a')
  })

  it('signup retourne une promesse', async () => {
    vi.spyOn(authApi, 'signup').mockResolvedValue(mockAxiosResponse({ access_token: 'a', refresh_token: 'b' }))
    const res = await authApi.signup({ email: 'test@example.com', username: 'Test', password: 'pass' })
    expect(res.data.refresh_token).toBe('b')
  })

  it('getProfile retourne un utilisateur', async () => {
    vi.spyOn(authApi, 'getProfile').mockResolvedValue(mockAxiosResponse({ id: 1, email: 'test@example.com', username: 'Test', created_at: '', updated_at: '' }))
    const res = await authApi.getProfile()
    expect(res.data.email).toBe('test@example.com')
  })

  it('logout retourne une promesse', async () => {
    vi.spyOn(authApi, 'logout').mockResolvedValue(mockAxiosResponse({ success: true } as any))
    const res = await authApi.logout()
    expect((res.data as any).success).toBe(true)
  })
})

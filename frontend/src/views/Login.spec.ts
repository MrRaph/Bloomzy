/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import Login from './Login.vue'

vi.mock('@/stores/auth')

const routerPush = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({ push: routerPush })
}))

describe('Login.vue', () => {
  let authStoreMock: any

  beforeEach(() => {
    authStoreMock = {
      isAuthenticated: false,
      isAuthReady: true,
      isLoading: false,
      error: '',
      login: vi.fn().mockResolvedValue(true),
      user: { username: 'TestUser', email: 'test@example.com' }
    }
    ;(useAuthStore as any).mockReturnValue(authStoreMock)
    routerPush.mockClear()
  })

  it('affiche le titre de connexion', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [createPinia()]
      }
    })
    expect(wrapper.text()).toMatch(/connexion|login|se connecter/i)
  })

  it('redirige vers /dashboard après login', async () => {
    const wrapper = mount(Login)
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')
    expect(authStoreMock.login).toHaveBeenCalled()
    await Promise.resolve()
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })

  it('redirige vers /dashboard si déjà authentifié au mount', () => {
    authStoreMock.isAuthenticated = true
    mount(Login)
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })
})

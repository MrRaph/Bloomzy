/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import Signup from './Signup.vue'

vi.mock('@/stores/auth')

const routerPush = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({ push: routerPush })
}))

describe('Signup.vue', () => {
  let authStoreMock: any

  beforeEach(() => {
    authStoreMock = {
      isAuthenticated: false,
      isLoading: false,
      error: '',
      signup: vi.fn().mockResolvedValue(true),
      user: { username: 'TestUser', email: 'test@example.com' }
    }
    ;(useAuthStore as any).mockReturnValue(authStoreMock)
    routerPush.mockClear()
  })

  it('affiche le titre d’inscription', () => {
    const wrapper = mount(Signup, {
      global: {
        plugins: [createPinia()]
      }
    })
    expect(wrapper.text()).toMatch(/inscription|signup|créer un compte/i)
  })

  it('redirige vers /dashboard après inscription', async () => {
    const wrapper = mount(Signup)
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="text"]').setValue('TestUser')
    await wrapper.findAll('input[type="password"]')[0].setValue('password123')
    await wrapper.findAll('input[type="password"]')[1].setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')
    expect(authStoreMock.signup).toHaveBeenCalled()
    await Promise.resolve()
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })

  it('redirige vers /dashboard si déjà authentifié au mount', () => {
    authStoreMock.isAuthenticated = true
    mount(Signup)
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })
})

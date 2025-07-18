/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Home from './Home.vue'
import { useAuthStore } from '@/stores/auth'

vi.mock('@/stores/auth')

describe('Home.vue', () => {
  it('affiche le titre Bloomzy', () => {
    (useAuthStore as any).mockReturnValue({ isAuthenticated: false, initializeAuth: () => {} })
    const wrapper = mount(Home, {
      global: { stubs: { RouterLink: RouterLinkStub } }
    })
    expect(wrapper.text()).toMatch(/Bloomzy/i)
  })

  it('affiche les boutons Connexion/Inscription si non connecté', () => {
    (useAuthStore as any).mockReturnValue({ isAuthenticated: false, initializeAuth: () => {} })
    const wrapper = mount(Home, {
      global: { stubs: { RouterLink: RouterLinkStub } }
    })
    expect(wrapper.text()).toContain('Commencer maintenant')
    expect(wrapper.text()).toContain('Se connecter')
  })

  it('affiche le message de bienvenue si connecté', () => {
    (useAuthStore as any).mockReturnValue({ isAuthenticated: true, user: { username: 'TestUser' }, initializeAuth: () => {} })
    const wrapper = mount(Home, {
      global: { stubs: { RouterLink: RouterLinkStub } }
    })
    expect(wrapper.text()).toContain('Bienvenue, TestUser')
  })
})

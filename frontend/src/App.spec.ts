import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import App from '@/App.vue'
import { useAuthStore } from '@/stores/auth'

vi.mock('@/stores/auth')

describe('App.vue navigation', () => {
  let authStoreMock: any

  beforeEach(() => {
    authStoreMock = {
      isAuthenticated: true,
      isAuthReady: true,
      user: { username: 'TestUser', email: 'test@example.com' },
      logout: vi.fn()
    }
    ;(useAuthStore as any).mockReturnValue(authStoreMock)
  })

  it('affiche le menu utilisateur complet quand connecté', () => {
    const wrapper = mount(App, {
      global: {
        stubs: { RouterLink: RouterLinkStub, RouterView: true }
      }
    })
    const links = wrapper.findAllComponents(RouterLinkStub)
    const expected = [
      '/dashboard',
      '/profile',
      '/plants',
      '/journal',
      '/community'
    ]
    expected.forEach((to) => {
      expect(links.some(l => l.props('to') === to)).toBe(true)
    })
    expect(wrapper.text()).not.toContain('Connexion')
    expect(wrapper.text()).not.toContain('Inscription')
  })

  it('affiche Connexion/Inscription si non connecté', () => {
    authStoreMock.isAuthenticated = false
    authStoreMock.isAuthReady = true
    const wrapper = mount(App, {
      global: {
        stubs: { RouterLink: RouterLinkStub, RouterView: true }
      }
    })
    expect(wrapper.text()).toContain('Connexion')
    expect(wrapper.text()).toContain('Inscription')
  })
})

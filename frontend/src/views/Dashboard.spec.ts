import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import { useAuthStore } from '@/stores/auth'

vi.mock('@/stores/auth')

const mockUser = {
  username: 'TestUser',
  email: 'test@example.com'
}

describe('Dashboard.vue', () => {
  let authStoreMock: any

  beforeEach(() => {
    authStoreMock = {
      user: mockUser,
      isAuthenticated: true
    }
    ;(useAuthStore as any).mockReturnValue(authStoreMock)
  })

  it('affiche le nom d’utilisateur si présent', () => {
    const wrapper = mount(Dashboard, {
      global: {
        stubs: { RouterLink: RouterLinkStub }
      }
    })
    expect(wrapper.text()).toContain('Bienvenue sur votre dashboard, TestUser')
  })

  it('affiche l’email si username absent', () => {
    authStoreMock.user = { email: 'test2@example.com' }
    const wrapper = mount(Dashboard, {
      global: {
        stubs: { RouterLink: RouterLinkStub }
      }
    })
    expect(wrapper.text()).toContain('Bienvenue sur votre dashboard, test2@example.com')
  })

  it('n’affiche rien si aucun utilisateur', () => {
    authStoreMock.user = null
    const wrapper = mount(Dashboard, {
      global: {
        stubs: { RouterLink: RouterLinkStub }
      }
    })
    // Le message doit être générique ou vide
    expect(wrapper.text()).toContain('Bienvenue sur votre dashboard,')
  })

  it('affiche tous les liens du menu dashboard', () => {
    const wrapper = mount(Dashboard, {
      global: {
        stubs: { RouterLink: RouterLinkStub }
      }
    })
    const links = wrapper.findAllComponents(RouterLinkStub)
    const expected = [
      '/profile',
      '/my-plants',
      '/indoor-plants',
      '/journal',
      '/community',
      '/settings'
    ]
    expect(links).toHaveLength(expected.length)
    expected.forEach((to, i) => {
      expect(links[i].props('to')).toBe(to)
    })
  })
})

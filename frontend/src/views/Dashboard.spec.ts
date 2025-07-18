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

  it('affiche le nom d’utilisateur ou l’email', () => {
    const wrapper = mount(Dashboard, {
      global: {
        stubs: { RouterLink: RouterLinkStub }
      }
    })
    expect(wrapper.text()).toContain('Bienvenue sur votre dashboard, TestUser')
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
      '/plants',
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

/// <reference types="vitest/globals" />
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Profile from './Profile.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: []
})
router.push = vi.fn()

describe('Profile.vue', () => {
  it('affiche le titre du profil', () => {
    const wrapper = mount(Profile, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    expect(wrapper.text()).toMatch(/profil|profile|mon compte/i)
  })
})

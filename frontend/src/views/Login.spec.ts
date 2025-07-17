/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Login from './Login.vue'

describe('Login.vue', () => {
  it('affiche le titre de connexion', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [createPinia()]
      }
    })
    expect(wrapper.text()).toMatch(/connexion|login|se connecter/i)
  })
})

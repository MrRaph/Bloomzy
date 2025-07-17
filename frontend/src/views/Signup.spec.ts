/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Signup from './Signup.vue'

describe('Signup.vue', () => {
  it('affiche le titre d’inscription', () => {
    const wrapper = mount(Signup, {
      global: {
        plugins: [createPinia()]
      }
    })
    expect(wrapper.text()).toMatch(/inscription|signup|créer un compte/i)
  })
})

/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import Home from './Home.vue'

describe('Home.vue', () => {
  it('affiche le titre Bloomzy', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [createPinia()]
      }
    })
    expect(wrapper.text()).toMatch(/Bloomzy/i)
  })
})

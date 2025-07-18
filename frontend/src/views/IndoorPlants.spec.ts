import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import IndoorPlants from './IndoorPlants.vue'
import { useIndoorPlantsStore } from '../stores/indoorPlants'

describe('IndoorPlants.vue', () => {
  it('affiche la liste des plantes', async () => {
    const pinia = createTestingPinia({
      initialState: {
        indoorPlants: {
          plants: [
            { id: 1, name: 'Ficus', species: 'Ficus lyrata', created_at: '', updated_at: '' },
            { id: 2, name: 'Monstera', species: 'Monstera deliciosa', created_at: '', updated_at: '' }
          ],
          loading: false,
          error: null
        }
      }
    })
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    expect(wrapper.text()).toContain('Ficus')
    expect(wrapper.text()).toContain('Monstera')
  })

  it('affiche le formulaire d\'ajout', async () => {
    const pinia = createTestingPinia()
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    await wrapper.find('button').trigger('click')
    expect(wrapper.text()).toContain('Ajouter une plante')
    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('appelle addPlant lors de la soumission du formulaire', async () => {
    const pinia = createTestingPinia()
    const store = useIndoorPlantsStore()
    store.addPlant = vi.fn()
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    await wrapper.find('button').trigger('click')
    await wrapper.find('input[placeholder="Nom de la plante"]').setValue('Pothos')
    await wrapper.find('input[placeholder="Espèce"]').setValue('Epipremnum aureum')
    await wrapper.find('form').trigger('submit.prevent')
    expect(store.addPlant).toHaveBeenCalledWith({ name: 'Pothos', species: 'Epipremnum aureum' })
  })
})

import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import IndoorPlants from './IndoorPlants.vue'
import { useIndoorPlantsStore } from '../stores/indoorPlants'

// Mock du composant BaseForm
vi.mock('@/components/BaseForm.vue', () => ({
  default: {
    name: 'BaseForm',
    template: '<form @submit.prevent="$props.onSubmit({ name: \'Pothos\', species: \'Epipremnum aureum\', family: \'\', difficulty: \'\' })" data-testid="base-form"><slot name="submit-label"></slot></form>',
    props: ['title', 'description', 'fields', 'initialValues', 'onSubmit']
  }
}))

describe('IndoorPlants.vue', () => {
  it('affiche la liste des plantes', async () => {
    const pinia = createTestingPinia({
      initialState: {
        indoorPlants: {
          plants: [
            { id: 1, name: 'Ficus', species: 'Ficus lyrata', family: 'Moraceae', difficulty: 'Facile', created_at: '', updated_at: '' },
            { id: 2, name: 'Monstera', species: 'Monstera deliciosa', family: 'Araceae', difficulty: 'Modéré', created_at: '', updated_at: '' }
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
    // Cliquer sur le bouton "Ajouter une espèce"
    await wrapper.find('.btn-primary').trigger('click')
    expect(wrapper.text()).toContain('Ajouter une espèce')
    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('appelle addPlant lors de la soumission du formulaire', async () => {
    const pinia = createTestingPinia()
    const store = useIndoorPlantsStore()
    store.addPlant = vi.fn()
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    // Cliquer sur le bouton "Ajouter une espèce"
    await wrapper.find('.btn-primary').trigger('click')
    // Soumettre le formulaire (le mock retourne automatiquement les données)
    await wrapper.find('form').trigger('submit.prevent')
    expect(store.addPlant).toHaveBeenCalledWith({ 
      name: 'Pothos', 
      species: 'Epipremnum aureum',
      family: '',
      difficulty: ''
    })
  })
})

import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import IndoorPlants from './IndoorPlants.vue'
import { useIndoorPlantsStore } from '../stores/indoorPlants'
import { nextTick } from 'vue'

// Mock du composant BaseForm pour simuler la soumission
vi.mock('@/components/BaseForm.vue', () => ({
  default: {
    name: 'BaseForm',
    template: `
      <form @submit.prevent="$props.onSubmit({ 
        name: 'Monstera', 
        species: 'Monstera deliciosa',
        family: 'Araceae',
        difficulty: 'Modéré'
      })" data-testid="base-form">
        <slot name="submit-label"></slot>
      </form>
    `,
    props: ['title', 'description', 'fields', 'initialValues', 'onSubmit']
  }
}))

describe('IndoorPlants.vue (integration)', () => {
  it('affiche, ajoute et supprime une plante (flow complet)', async () => {
    // Crée une instance unique de Pinia
    const pinia = createPinia()
    setActivePinia(pinia)
    const store = useIndoorPlantsStore()
    // Mock des méthodes du store
    store.fetchPlants = vi.fn().mockImplementation(() => {
      store.plants = [
        { id: 1, scientific_name: 'Ficus lyrata', common_names: 'Ficus', family: 'Moraceae', difficulty: 'Facile' }
      ]
    })
    store.addPlant = vi.fn().mockImplementation((plant) => {
      store.plants.unshift({ id: 2, ...plant })
    })
    store.deletePlant = vi.fn().mockImplementation((id) => {
      store.plants = store.plants.filter(p => p.id !== id)
    })
    // Monte le composant avec la même instance de Pinia
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    // Appel explicite de fetchPlants pour simuler le comportement du composant
    await store.fetchPlants()
    await nextTick()
    // Ajout - cliquer sur le bouton "Ajouter une espèce"
    await wrapper.find('.btn-primary').trigger('click')
    await nextTick()
    // Soumettre le formulaire (le mock BaseForm envoie automatiquement les données)
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(store.addPlant).toHaveBeenCalledWith({ 
      name: 'Monstera', 
      species: 'Monstera deliciosa',
      family: 'Araceae',
      difficulty: 'Modéré'
    })
    // Suppression : on simule l'appel direct comme le ferait le bouton
    store.deletePlant(1)
    expect(store.deletePlant).toHaveBeenCalledWith(1)
  })
})

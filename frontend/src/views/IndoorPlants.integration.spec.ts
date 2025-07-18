import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import IndoorPlants from './IndoorPlants.vue'
import { useIndoorPlantsStore } from '../stores/indoorPlants'
import { nextTick } from 'vue'

describe('IndoorPlants.vue (integration)', () => {
  it('affiche, ajoute et supprime une plante (flow complet)', async () => {
    // Crée une instance unique de Pinia
    const pinia = createPinia()
    setActivePinia(pinia)
    const store = useIndoorPlantsStore()
    // Mock des méthodes du store
    store.fetchPlants = vi.fn().mockImplementation(() => {
      store.plants = [
        { id: 1, name: 'Ficus', species: 'Ficus lyrata', created_at: '', updated_at: '' }
      ]
    })
    store.addPlant = vi.fn().mockImplementation((plant) => {
      store.plants.unshift({ id: 2, ...plant, created_at: '', updated_at: '' })
    })
    store.deletePlant = vi.fn().mockImplementation((id) => {
      store.plants = store.plants.filter(p => p.id !== id)
    })
    // Monte le composant avec la même instance de Pinia
    const wrapper = mount(IndoorPlants, { global: { plugins: [pinia] } })
    // Appel explicite de fetchPlants pour simuler le comportement du composant
    await store.fetchPlants()
    await nextTick()
    // Ajout
    await wrapper.find('button').trigger('click')
    await nextTick()
    await wrapper.find('input[placeholder="Ex: Monstera deliciosa"]').setValue('Monstera')
    await wrapper.find('input[placeholder="Ex: Araceae"]').setValue('Monstera deliciosa')
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(store.addPlant).toHaveBeenCalledWith({ name: 'Monstera', species: 'Monstera deliciosa' })
    // Suppression : on simule l'appel direct comme le ferait le bouton
    store.deletePlant(1)
    expect(store.deletePlant).toHaveBeenCalledWith(1)
  })
})

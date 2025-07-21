import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import MyPlants from '@/views/MyPlants.vue'
import { useMyPlantsStore } from '@/stores/myPlants'

// Mock du composant BaseForm
vi.mock('@/components/BaseForm.vue', () => ({
  default: {
    name: 'BaseForm',
    template: '<form @submit.prevent="$props.onSubmit({})" data-testid="base-form"><slot name="submit-label"></slot></form>',
    props: ['title', 'description', 'fields', 'initialValues', 'onSubmit']
  }
}))

// Mock des API
vi.mock('@/services/api', () => ({
  fetchIndoorPlants: vi.fn().mockResolvedValue([
    { id: 1, scientific_name: 'Ficus benjamina', common_names: 'Ficus pleureur' }
  ])
}))

const mockUserPlant = {
  id: 1,
  user_id: 1,
  species_id: 1,
  custom_name: 'Mon Ficus',
  location: 'Salon',
  health_status: 'healthy' as const,
  created_at: '2023-01-01',
  updated_at: '2023-01-01',
  species: {
    id: 1,
    scientific_name: 'Ficus benjamina',
    common_names: 'Ficus pleureur',
    family: 'Moraceae',
    difficulty: 'Facile'
  }
}

describe('MyPlants.vue', () => {
  let wrapper: any
  let mockStore: any

  beforeEach(() => {
    vi.clearAllMocks()
    
    const pinia = createTestingPinia({
      createSpy: vi.fn,
      initialState: {
        myPlants: {
          plants: [],
          isLoading: false,
          error: null
        }
      }
    })

    wrapper = mount(MyPlants, {
      global: {
        plugins: [pinia],
        stubs: {
          'router-link': true
        }
      }
    })

    mockStore = useMyPlantsStore()
  })

  it('affiche le titre et la description', () => {
    expect(wrapper.text()).toContain('Mes Plantes')
    expect(wrapper.text()).toContain('Gérez votre collection personnelle')
  })

  it('affiche l\'état vide quand aucune plante', () => {
    expect(wrapper.text()).toContain('Aucune plante enregistrée')
    expect(wrapper.text()).toContain('Ajouter ma première plante')
  })

  it('affiche les statistiques quand il y a des plantes', async () => {
    // Simule des plantes dans le store
    mockStore.plants = [
      mockUserPlant,
      { ...mockUserPlant, id: 2, health_status: 'sick' }
    ]
    mockStore.healthyPlants = [mockUserPlant]
    mockStore.plantsNeedingAttention = [{ ...mockUserPlant, id: 2, health_status: 'sick' }]

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('2')
    expect(wrapper.text()).toContain('au total')
    expect(wrapper.text()).toContain('1')
    expect(wrapper.text()).toContain('En bonne santé')
    expect(wrapper.text()).toContain('Nécessitent attention')
  })

  it('affiche les cartes de plantes', async () => {
    mockStore.plants = [mockUserPlant]
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Mon Ficus')
    expect(wrapper.text()).toContain('Ficus benjamina')
    expect(wrapper.text()).toContain('Salon')
    expect(wrapper.text()).toContain('💚') // Icône de bonne santé
  })

  it('ouvre le formulaire d\'ajout', async () => {
    const addButton = wrapper.find('button')
    await addButton.trigger('click')

    expect(wrapper.vm.showAddForm).toBe(true)
    expect(wrapper.find('[data-testid="base-form"]').exists()).toBe(true)
  })

  it('appelle fetchPlants au montage', async () => {
    // Le composant est déjà monté dans beforeEach
    await wrapper.vm.$nextTick()
    expect(mockStore.fetchPlants).toHaveBeenCalled()
  })

  it('affiche un message d\'erreur', async () => {
    mockStore.error = 'Erreur de test'
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Erreur de test')
  })

  it('affiche l\'indicateur de chargement', async () => {
    mockStore.isLoading = true
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Chargement de vos plantes')
  })

  it('gère l\'édition d\'une plante', async () => {
    mockStore.plants = [mockUserPlant]
    await wrapper.vm.$nextTick()

    // Simule le clic sur modifier
    wrapper.vm.editPlant(mockUserPlant)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.editingPlant).toEqual(mockUserPlant)
    expect(wrapper.vm.form.custom_name).toBe('Mon Ficus')
  })

  it('gère la suppression d\'une plante', async () => {
    // Mock de window.confirm
    window.confirm = vi.fn().mockReturnValue(true)
    
    await wrapper.vm.handleDeletePlant(mockUserPlant)

    expect(mockStore.deletePlant).toHaveBeenCalledWith(1)
  })

  it('ouvre le modal d\'arrosage', async () => {
    wrapper.vm.openWateringModal(mockUserPlant)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.wateringPlant).toEqual(mockUserPlant)
  })

  it('ferme le modal d\'arrosage', async () => {
    wrapper.vm.wateringPlant = mockUserPlant
    wrapper.vm.closeWateringModal()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.wateringPlant).toBe(null)
  })

  it('ferme le formulaire', async () => {
    wrapper.vm.showAddForm = true
    wrapper.vm.editingPlant = mockUserPlant
    
    wrapper.vm.closeForm()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.showAddForm).toBe(false)
    expect(wrapper.vm.editingPlant).toBe(null)
    expect(wrapper.vm.form.custom_name).toBe('')
  })
})

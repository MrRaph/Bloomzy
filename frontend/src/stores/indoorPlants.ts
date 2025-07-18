import { defineStore } from 'pinia'
import { fetchIndoorPlants, createIndoorPlant, updateIndoorPlant, deleteIndoorPlant } from '../services/api'
import type { IndoorPlant } from '../types'


export const useIndoorPlantsStore = defineStore('indoorPlants', {
  state: () => ({
    plants: [] as IndoorPlant[],
    loading: false,
    error: null as string | null
  }),
  actions: {
    async fetchPlants(search?: string) {
      this.loading = true
      try {
        const backendPlants = await fetchIndoorPlants(search)
        this.plants = backendPlants.map((p: any) => ({
          id: p.id,
          name: p.name ?? p.scientific_name,
          species: p.species ?? (p.common_names ? (Array.isArray(p.common_names) ? p.common_names[0] : p.common_names.split(',')[0].trim()) : ''),
          created_at: p.created_at,
          updated_at: p.updated_at
        }))
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async addPlant(payload: Omit<IndoorPlant, 'id' | 'created_at' | 'updated_at'>) {
      this.loading = true
      try {
        // Adapter le payload pour l'API backend (mapping frontend -> backend)
        const apiPayload = {
          scientific_name: payload.name,
          common_names: [payload.species]
        }
        // Appel API, puis conversion backend -> frontend ou mock
        const backendPlant = await createIndoorPlant(apiPayload)
        const plant: IndoorPlant = {
          id: backendPlant.id,
          name: backendPlant.name ?? backendPlant.scientific_name,
          species: backendPlant.species ?? (backendPlant.common_names ? (Array.isArray(backendPlant.common_names) ? backendPlant.common_names[0] : backendPlant.common_names.split(',')[0].trim()) : ''),
          created_at: backendPlant.created_at,
          updated_at: backendPlant.updated_at
        }
        this.plants.unshift(plant)
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async updatePlant(id: number, payload: Partial<Omit<IndoorPlant, 'id' | 'created_at' | 'updated_at'>>) {
      this.loading = true
      try {
        const updated = await updateIndoorPlant(id, payload) as IndoorPlant
        const idx = this.plants.findIndex((p) => p.id === id)
        if (idx !== -1) this.plants[idx] = updated
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async deletePlant(id: number) {
      this.loading = true
      try {
        await deleteIndoorPlant(id)
        this.plants = this.plants.filter((p) => p.id !== id)
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    }
  }
})

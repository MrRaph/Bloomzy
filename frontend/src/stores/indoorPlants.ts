import { defineStore } from 'pinia'
import { fetchIndoorPlants, createIndoorPlant } from '../services/api'

export const useIndoorPlantsStore = defineStore('indoorPlants', {
  state: () => ({
    plants: [] as any[],
    loading: false,
    error: null as string | null
  }),
  actions: {
    async fetchPlants(search?: string) {
      this.loading = true
      try {
        this.plants = await fetchIndoorPlants(search)
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async createPlant(payload: Record<string, any>) {
      this.loading = true
      try {
        const plant = await createIndoorPlant(payload)
        this.plants.unshift(plant)
        this.error = null
      } catch (e: any) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    }
  }
})

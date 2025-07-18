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
        this.plants = await fetchIndoorPlants(search) as IndoorPlant[]
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
        // Adapter le payload pour l'API backend
        const apiPayload = {
          scientific_name: payload.name,
          common_names: payload.species
        }
        const plant = await createIndoorPlant(apiPayload) as IndoorPlant
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

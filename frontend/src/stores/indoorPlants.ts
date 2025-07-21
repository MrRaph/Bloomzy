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
          scientific_name: p.scientific_name,
          common_names: p.common_names,
          family: p.family,
          difficulty: p.difficulty,
          origin: p.origin,
          watering_frequency: p.watering_frequency,
          light: p.light,
          humidity: p.humidity,
          temperature: p.temperature,
          soil_type: p.soil_type,
          adult_size: p.adult_size,
          growth_rate: p.growth_rate,
          toxicity: p.toxicity,
          air_purification: p.air_purification,
          flowering: p.flowering
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
        // Appel API direct avec le payload aligné
        const backendPlant = await createIndoorPlant(payload)
        const plant: IndoorPlant = {
          id: backendPlant.id,
          scientific_name: backendPlant.scientific_name,
          common_names: backendPlant.common_names,
          family: backendPlant.family,
          difficulty: backendPlant.difficulty,
          origin: backendPlant.origin,
          watering_frequency: backendPlant.watering_frequency,
          light: backendPlant.light,
          humidity: backendPlant.humidity,
          temperature: backendPlant.temperature,
          soil_type: backendPlant.soil_type,
          adult_size: backendPlant.adult_size,
          growth_rate: backendPlant.growth_rate,
          toxicity: backendPlant.toxicity,
          air_purification: backendPlant.air_purification,
          flowering: backendPlant.flowering
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

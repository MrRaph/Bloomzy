<template>
  <div class="indoor-plants-view">
    <h1>Mes plantes d'intérieur</h1>
    <button @click="showAddForm = true">Ajouter une plante</button>
    <ul v-if="plants && plants.length">
      <li v-for="plant in plants" :key="plant.id">
        <span>{{ plant.name }} ({{ plant.species }})</span>
        <button @click="editPlant(plant)">Modifier</button>
        <button @click="deletePlant(plant.id)">Supprimer</button>
      </li>
    </ul>
    <div v-else>Aucune plante enregistrée.</div>

    <!-- Formulaire d'ajout/modification -->
    <div v-if="showAddForm || editingPlant">
      <h2>{{ editingPlant ? 'Modifier' : 'Ajouter' }} une plante</h2>
      <form @submit.prevent="submitForm">
        <input v-model="form.name" placeholder="Nom de la plante" required />
        <input v-model="form.species" placeholder="Espèce" required />
        <button type="submit">{{ editingPlant ? 'Enregistrer' : 'Ajouter' }}</button>
        <button type="button" @click="cancelForm">Annuler</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useIndoorPlantsStore } from '../stores/indoorPlants';

const store = useIndoorPlantsStore();
const plants = store.plants;
const showAddForm = ref(false);
const editingPlant = ref(null as null | any);
const form = ref({ name: '', species: '' });

onMounted(() => {
  store.fetchPlants();
});

function editPlant(plant: any) {
  editingPlant.value = plant;
  form.value = { name: plant.name, species: plant.species };
  showAddForm.value = false;
}

function deletePlant(id: number) {
  store.deletePlant(id);
}

function submitForm() {
  if (editingPlant.value) {
    store.updatePlant(editingPlant.value.id, form.value);
    editingPlant.value = null;
  } else {
    store.addPlant(form.value);
  }
  form.value = { name: '', species: '' };
  showAddForm.value = false;
}

function cancelForm() {
  editingPlant.value = null;
  showAddForm.value = false;
  form.value = { name: '', species: '' };
}
</script>

<style scoped>
.indoor-plants-view {
  max-width: 600px;
  margin: 0 auto;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
button {
  margin-left: 0.5rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>

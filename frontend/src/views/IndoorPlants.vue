<template>
  <div class="indoor-plants-view">
    <h1>Catalogue des plantes d'intérieur</h1>
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
      <BaseForm
        :title="editingPlant ? 'Modifier une plante' : 'Ajouter une plante'"
        :description="editingPlant ? 'Modifiez les informations de votre plante' : 'Ajoutez une nouvelle plante à votre collection'"
        :fields="plantFields"
        :initial-values="form"
        :on-submit="submitForm"
      >
        <template #submit-label>{{ editingPlant ? 'Enregistrer' : 'Ajouter' }}</template>
        <template #footer>
          <div class="form-actions">
            <button type="button" @click="cancelForm" class="btn btn-secondary">
              Annuler
            </button>
          </div>
        </template>
      </BaseForm>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useIndoorPlantsStore } from '../stores/indoorPlants';
import BaseForm from '@/components/BaseForm.vue';

const store = useIndoorPlantsStore();
const plants = store.plants;
const showAddForm = ref(false);
const editingPlant = ref(null as null | any);
const form = ref({ name: '', species: '' });

const plantFields = [
  {
    name: 'name',
    label: 'Nom de la plante',
    type: 'text',
    required: true,
    placeholder: 'Ex: Monstera deliciosa'
  },
  {
    name: 'species',
    label: 'Espèce',
    type: 'text',
    required: true,
    placeholder: 'Ex: Araceae'
  }
];

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

function submitForm(formData: Record<string, any>) {
  if (editingPlant.value) {
    store.updatePlant(editingPlant.value.id, formData);
    editingPlant.value = null;
  } else {
    const plantData = {
      name: formData.name as string,
      species: formData.species as string
    };
    store.addPlant(plantData);
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

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}
</style>

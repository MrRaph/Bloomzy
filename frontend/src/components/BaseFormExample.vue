<template>
  <BaseForm
    title="🌱 Exemple de formulaire"
    description="Test du composant BaseForm avec le style d'authentification"
    :fields="fields"
    :loading="loading"
    :general-error="error"
    loading-text="Traitement en cours..."
    :validate="validateForm"
    @submit="handleSubmit"
  >
    <template #submit-label>Envoyer le formulaire</template>
    <template #footer>
      <p>
        Besoin d'aide ? 
        <a href="#" class="link">Contactez-nous</a>
      </p>
    </template>
  </BaseForm>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseForm from './BaseForm.vue'

const loading = ref(false)
const error = ref('')

const fields = [
  {
    name: 'email',
    label: 'Email',
    type: 'email',
    required: true,
    placeholder: 'votre@email.com',
    autocomplete: 'email'
  },
  {
    name: 'name',
    label: 'Nom de la plante',
    type: 'text',
    required: true,
    placeholder: 'Ex: Monstera Deliciosa'
  },
  {
    name: 'description',
    label: 'Description',
    type: 'textarea',
    required: false,
    placeholder: 'Décrivez votre plante...',
    rows: 4,
    hint: 'Ajoutez quelques détails sur votre plante'
  }
]

const validateForm = (values: Record<string, any>) => {
  const errors: Record<string, string> = {}
  
  if (!values.email || !values.email.includes('@')) {
    errors.email = 'Email invalide'
  }
  
  if (!values.name || values.name.trim().length < 2) {
    errors.name = 'Le nom doit contenir au moins 2 caractères'
  }
  
  return errors
}

const handleSubmit = async (values: Record<string, any>) => {
  loading.value = true
  error.value = ''
  
  try {
    // Simulation d'un appel API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    console.log('Formulaire soumis:', values)
    
    // Simulation d'une erreur parfois
    if (Math.random() > 0.7) {
      throw new Error('Erreur simulée')
    }
    
    alert('Formulaire envoyé avec succès!')
  } catch (err) {
    error.value = 'Une erreur est survenue lors de l\'envoi'
  } finally {
    loading.value = false
  }
}
</script>
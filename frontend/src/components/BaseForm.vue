<template>
  <div class="form-page">
    <div class="form-container">
      <div class="form-header" v-if="title || description">
        <h1 v-if="title">{{ title }}</h1>
        <p v-if="description">{{ description }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="base-form">
        <div v-for="field in fields" :key="field.name" class="form-group">
          <label v-if="field.type !== 'checkbox'" :for="field.name">{{ field.label }}</label>
          <label v-else class="checkbox-label">
            <input
              type="checkbox"
              :id="field.name"
              v-model="formData[field.name]"
              :required="field.required"
              :disabled="loading"
            />
            {{ field.label }}
          </label>
          <input
            v-if="field.type !== 'textarea' && field.type !== 'select' && field.type !== 'checkbox'"
            :type="field.type"
            :id="field.name"
            v-model="formData[field.name]"
            :placeholder="field.placeholder"
            :required="field.required"
            :disabled="loading"
            :autocomplete="field.autocomplete || 'off'"
          />
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.name"
            v-model="formData[field.name]"
            :placeholder="field.placeholder"
            :required="field.required"
            :disabled="loading"
            :rows="field.rows || 3"
          />
          <select
            v-else-if="field.type === 'select'"
            :id="field.name"
            v-model="formData[field.name]"
            :required="field.required"
            :disabled="loading"
          >
            <option v-for="option in field.options" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <div v-if="field.hint" class="field-hint">{{ field.hint }}</div>
          <div v-if="errors[field.name]" class="error-message">{{ errors[field.name] }}</div>
        </div>

        <div class="error-message" v-if="generalError">
          {{ generalError }}
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
          <span v-if="loading">{{ loadingText || 'Traitement...' }}</span>
          <span v-else>
            <slot name="submit-label">Envoyer</slot>
          </span>
        </button>
      </form>

      <div class="form-footer" v-if="$slots.footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';

interface Field {
  name: string;
  label: string;
  type: string;
  required?: boolean;
  placeholder?: string;
  autocomplete?: string;
  hint?: string;
  rows?: number;
  options?: { value: string; label: string }[];
}

const props = defineProps<{
  fields: Field[];
  title?: string;
  description?: string;
  initialValues?: Record<string, any>;
  validate?: (values: Record<string, any>) => Record<string, string>;
  onSubmit: (values: Record<string, any>) => Promise<void> | void;
  loading?: boolean;
  loadingText?: string;
  generalError?: string;
}>();

const formData = reactive({ ...props.initialValues });
const errors = reactive<Record<string, string>>({});

const isFormValid = computed(() => {
  const requiredFields = props.fields.filter(field => field.required);
  return requiredFields.every(field => formData[field.name] && formData[field.name].toString().trim());
});

watch(
  () => props.initialValues,
  (newVal) => {
    if (newVal) {
      Object.assign(formData, newVal);
    }
  },
  { immediate: true }
);

watch(
  () => props.generalError,
  () => {
    Object.keys(errors).forEach(key => delete errors[key]);
  }
);

async function handleSubmit() {
  Object.keys(errors).forEach(key => delete errors[key]);
  
  if (props.validate) {
    const validation = props.validate(formData);
    Object.assign(errors, validation);
    if (Object.keys(validation).length > 0) return;
  }
  
  try {
    await props.onSubmit({ ...formData });
  } catch (error) {
    console.error('Form submission error:', error);
  }
}
</script>

<style scoped>
@import '../styles/components/base-form.css';
</style>

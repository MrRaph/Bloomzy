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
import { reactive, watch, ref, computed } from 'vue';

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
.form-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 2rem;
}

.form-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h1 {
  font-size: 2rem;
  color: #059669;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: #6b7280;
  font-size: 0.9rem;
}

.base-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled,
.form-group select:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  color: #374151;
  font-size: 0.9rem;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
  padding: 0;
  transform: scale(1.2);
}

.field-hint {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  text-align: center;
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

.btn-primary {
  background: #059669;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #047857;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.form-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.form-footer p {
  color: #6b7280;
  font-size: 0.9rem;
}

.link {
  color: #059669;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .form-container {
    padding: 1.5rem;
  }
  
  .form-header h1 {
    font-size: 1.5rem;
  }
}
</style>

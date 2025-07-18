<template>
  <form @submit.prevent="handleSubmit">
    <div v-for="field in fields" :key="field.name" class="form-group">
      <label :for="field.name">{{ field.label }}</label>
      <input
        v-if="field.type !== 'textarea'"
        :type="field.type"
        class="form-control"
        :id="field.name"
        v-model="formData[field.name]"
        :placeholder="field.placeholder"
        :required="field.required"
        :autocomplete="field.autocomplete || 'off'"
      />
      <textarea
        v-else
        class="form-control"
        :id="field.name"
        v-model="formData[field.name]"
        :placeholder="field.placeholder"
        :required="field.required"
      />
      <div v-if="errors[field.name]" class="form-error">{{ errors[field.name] }}</div>
    </div>
    <button type="submit" class="btn btn-primary" :disabled="loading">
      <slot name="submit-label">Envoyer</slot>
    </button>
    <slot />
  </form>
</template>

<script setup lang="ts">
import { reactive, toRefs, watch, ref } from 'vue';
import type { PropType } from 'vue';

interface Field {
  name: string;
  label: string;
  type: string;
  required?: boolean;
  placeholder?: string;
  autocomplete?: string;
}

defineProps<{
  fields: Field[];
  initialValues?: Record<string, any>;
  validate?: (values: Record<string, any>) => Record<string, string>;
  onSubmit: (values: Record<string, any>) => Promise<void> | void;
  loading?: boolean;
}>();

const props = defineProps();
const formData = reactive({ ...props.initialValues });
const errors = reactive<Record<string, string>>({});
const loading = ref(false);

watch(
  () => props.initialValues,
  (newVal) => {
    if (newVal) {
      Object.assign(formData, newVal);
    }
  },
  { immediate: true }
);

async function handleSubmit() {
  errors.value = {};
  if (props.validate) {
    const validation = props.validate(formData);
    Object.assign(errors, validation);
    if (Object.keys(validation).length > 0) return;
  }
  loading.value = true;
  try {
    await props.onSubmit({ ...formData });
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
.form-error {
  color: #d32f2f;
  font-size: 0.9em;
  margin-top: 0.25em;
}
</style>

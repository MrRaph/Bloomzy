<template>
  <div class="api-keys-view">
    <ApiKeysManager />
  </div>
</template>

<script setup lang="ts">
import ApiKeysManager from '@/components/ApiKeys/ApiKeysManager.vue'
</script>

<style scoped>
.api-keys-view {
  min-height: 100vh;
  background-color: #f7fafc;
  padding: 2rem 0;
}
</style>
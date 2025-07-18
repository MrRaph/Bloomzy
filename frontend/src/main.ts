import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Hydrate l'authentification au démarrage
type MaybePromise<T> = T | Promise<T>
function callMaybePromise<T>(fn: () => MaybePromise<T>) {
  const result = fn()
  if (result instanceof Promise) {
    result.catch(() => {})
  }
}

app.mount('#app')

// Hydratation après le mount (Pinia doit être prêt)
callMaybePromise(() => {
  const authStore = useAuthStore()
  return authStore.initializeAuth?.()
})
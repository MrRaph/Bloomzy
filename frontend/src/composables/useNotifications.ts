import { ref } from 'vue'
import type { Notification } from '@/types'

// Instance singleton pour les notifications
const notificationInstance = ref<any>(null)

export const useNotifications = () => {
  const setNotificationInstance = (instance: any) => {
    notificationInstance.value = instance
  }

  const addNotification = (notification: Omit<Notification, 'id'>) => {
    if (notificationInstance.value) {
      return notificationInstance.value.addNotification(notification)
    }
    console.warn('Notification system not initialized')
    return null
  }

  const removeNotification = (id: string) => {
    if (notificationInstance.value) {
      notificationInstance.value.removeNotification(id)
    }
  }

  const clearAll = () => {
    if (notificationInstance.value) {
      notificationInstance.value.clearAll()
    }
  }

  const success = (message: string, title?: string, options?: Partial<Notification>) => {
    return addNotification({ type: 'success', message, title, ...options })
  }

  const error = (message: string, title?: string, options?: Partial<Notification>) => {
    return addNotification({ type: 'error', message, title, ...options })
  }

  const warning = (message: string, title?: string, options?: Partial<Notification>) => {
    return addNotification({ type: 'warning', message, title, ...options })
  }

  const info = (message: string, title?: string, options?: Partial<Notification>) => {
    return addNotification({ type: 'info', message, title, ...options })
  }

  // Méthodes de convenance pour les actions CRUD des plantes
  const plantActions = {
    created: (plantName: string) => {
      success(`${plantName} a été ajoutée à votre collection`, 'Plante ajoutée')
    },
    
    updated: (plantName: string) => {
      success(`${plantName} a été mise à jour`, 'Plante modifiée')
    },
    
    deleted: (plantName: string) => {
      success(`${plantName} a été supprimée de votre collection`, 'Plante supprimée')
    },
    
    watered: (plantName: string) => {
      success(`Arrosage de ${plantName} enregistré`, 'Arrosage enregistré')
    },
    
    photoUploaded: (plantName: string) => {
      success(`Photo de ${plantName} mise à jour`, 'Photo ajoutée')
    },

    loadError: () => {
      error('Impossible de charger vos plantes. Vérifiez votre connexion.', 'Erreur de chargement')
    },

    saveError: () => {
      error('Impossible de sauvegarder les modifications. Réessayez plus tard.', 'Erreur de sauvegarde')
    },

    networkError: () => {
      error('Problème de connexion réseau. Vérifiez votre connexion internet.', 'Connexion perdue')
    },

    unauthorized: () => {
      error('Votre session a expiré. Veuillez vous reconnecter.', 'Session expirée', {
        persistent: true
      })
    },

    wateringReminder: (plantName: string, daysOverdue: number) => {
      if (daysOverdue > 0) {
        warning(
          `${plantName} devrait être arrosée depuis ${daysOverdue} jour${daysOverdue > 1 ? 's' : ''}`,
          'Arrosage en retard'
        )
      } else {
        info(`Il est temps d'arroser ${plantName}`, 'Rappel d\'arrosage')
      }
    }
  }

  return {
    setNotificationInstance,
    addNotification,
    removeNotification,
    clearAll,
    success,
    error,
    warning,
    info,
    plantActions
  }
}

// Export du type pour TypeScript
export type { Notification }

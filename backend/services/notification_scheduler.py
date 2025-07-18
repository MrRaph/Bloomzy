"""
Scheduler pour les notifications automatiques.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from models.user import db
from models.notification import Notification, NotificationType, NotificationStatus
from models.user_plant import UserPlant
from models.watering_history import WateringHistory
from services.notification_service import NotificationService
from services.watering_algorithm import WateringAlgorithm
import threading
import time

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """Scheduler principal pour les notifications automatiques."""
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.watering_algorithm = WateringAlgorithm()
        self.running = False
        self.thread = None
    
    def start(self):
        """Démarre le scheduler en arrière-plan."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Scheduler de notifications démarré")
    
    def stop(self):
        """Arrête le scheduler."""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Scheduler de notifications arrêté")
    
    def _run_scheduler(self):
        """Boucle principale du scheduler."""
        while self.running:
            try:
                # Vérifier les notifications à envoyer
                self.process_scheduled_notifications()
                
                # Générer de nouvelles notifications d'arrosage
                self.generate_watering_notifications()
                
                # Nettoyer les anciennes notifications
                self.cleanup_old_notifications()
                
                # Attendre avant la prochaine vérification (5 minutes)
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Erreur dans le scheduler: {str(e)}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    def process_scheduled_notifications(self):
        """Traite les notifications programmées qui doivent être envoyées."""
        try:
            # Récupérer les notifications programmées qui doivent être envoyées
            current_time = datetime.utcnow()
            
            notifications_to_send = Notification.query.filter(
                Notification.status == NotificationStatus.SCHEDULED,
                Notification.scheduled_for <= current_time
            ).all()
            
            for notification in notifications_to_send:
                try:
                    success = self.notification_service.send_notification(notification)
                    if success:
                        logger.info(f"Notification {notification.id} envoyée avec succès")
                    else:
                        logger.warning(f"Échec de l'envoi de la notification {notification.id}")
                        
                except Exception as e:
                    logger.error(f"Erreur lors de l'envoi de la notification {notification.id}: {str(e)}")
                    notification.status = NotificationStatus.FAILED
                    notification.updated_at = datetime.utcnow()
                    db.session.commit()
            
            if notifications_to_send:
                logger.info(f"Traité {len(notifications_to_send)} notifications programmées")
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement des notifications programmées: {str(e)}")
    
    def generate_watering_notifications(self):
        """Génère automatiquement les notifications d'arrosage."""
        try:
            # Récupérer toutes les plantes actives
            user_plants = UserPlant.query.filter_by(active=True).all()
            
            notifications_created = 0
            
            for plant in user_plants:
                try:
                    # Vérifier si une notification d'arrosage existe déjà pour cette plante
                    existing_notification = Notification.query.filter(
                        Notification.user_id == plant.user_id,
                        Notification.type == NotificationType.WATERING,
                        Notification.status.in_([NotificationStatus.SCHEDULED, NotificationStatus.SENT]),
                        Notification.data.contains({'plant_id': plant.id})
                    ).first()
                    
                    if existing_notification:
                        continue  # Notification déjà programmée
                    
                    # Calculer le besoin d'arrosage
                    watering_data = self.watering_algorithm.calculate_watering_need(plant.id)
                    
                    if not watering_data:
                        continue
                    
                    # Vérifier si une notification est nécessaire
                    if self.should_create_watering_notification(plant, watering_data):
                        notification = self.notification_service.create_watering_notification(
                            plant, 
                            watering_data.get('urgency_level', 5)
                        )
                        
                        if notification:
                            db.session.add(notification)
                            notifications_created += 1
                            
                except Exception as e:
                    logger.error(f"Erreur lors de la génération de notification pour la plante {plant.id}: {str(e)}")
                    continue
            
            if notifications_created > 0:
                db.session.commit()
                logger.info(f"Créé {notifications_created} nouvelles notifications d'arrosage")
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération des notifications d'arrosage: {str(e)}")
    
    def should_create_watering_notification(self, plant: UserPlant, watering_data: dict) -> bool:
        """Détermine si une notification d'arrosage doit être créée."""
        try:
            urgency_level = watering_data.get('urgency_level', 0)
            
            # Créer une notification si:
            # - Urgence élevée (>= 6)
            # - Ou si la plante n'a pas été arrosée depuis longtemps
            if urgency_level >= 6:
                return True
            
            # Vérifier le dernier arrosage
            last_watering = WateringHistory.query.filter_by(
                user_plant_id=plant.id
            ).order_by(WateringHistory.watering_date.desc()).first()
            
            if last_watering:
                days_since_watering = (datetime.utcnow() - last_watering.watering_date).days
                recommended_frequency = plant.species.watering_frequency
                
                # Notification si on dépasse la fréquence recommandée
                if days_since_watering >= recommended_frequency:
                    return True
            else:
                # Pas d'historique d'arrosage, créer une notification
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du besoin de notification: {str(e)}")
            return False
    
    def schedule_notification(self, notification: Notification):
        """Programme une notification spécifique."""
        try:
            # La notification est déjà en base avec son statut SCHEDULED
            # Le scheduler la traitera automatiquement
            logger.info(f"Notification {notification.id} programmée pour {notification.scheduled_for}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la programmation de la notification: {str(e)}")
    
    def cancel_notification(self, notification_id: str):
        """Annule une notification programmée."""
        try:
            notification = Notification.query.get(notification_id)
            if notification and notification.status == NotificationStatus.SCHEDULED:
                notification.cancel()
                logger.info(f"Notification {notification_id} annulée")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'annulation de la notification: {str(e)}")
    
    def reschedule_notification(self, notification_id: str, new_time: datetime):
        """Reprogramme une notification."""
        try:
            notification = Notification.query.get(notification_id)
            if notification and notification.status == NotificationStatus.SCHEDULED:
                notification.scheduled_for = new_time
                notification.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Notification {notification_id} reprogrammée pour {new_time}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la reprogrammation de la notification: {str(e)}")
    
    def cleanup_old_notifications(self):
        """Nettoie les anciennes notifications."""
        try:
            # Supprimer les notifications de plus de 30 jours
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            
            old_notifications = Notification.query.filter(
                Notification.created_at < cutoff_date,
                Notification.status.in_([
                    NotificationStatus.DELIVERED, 
                    NotificationStatus.OPENED, 
                    NotificationStatus.ACTED_UPON,
                    NotificationStatus.DISMISSED,
                    NotificationStatus.FAILED
                ])
            ).all()
            
            for notification in old_notifications:
                db.session.delete(notification)
            
            if old_notifications:
                db.session.commit()
                logger.info(f"Supprimé {len(old_notifications)} anciennes notifications")
                
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des notifications: {str(e)}")
    
    def generate_maintenance_notifications(self):
        """Génère les notifications de maintenance des plantes."""
        try:
            # TODO: Implémenter la génération de notifications de maintenance
            # - Nettoyage des feuilles
            # - Rotation des pots
            # - Contrôle des parasites
            # - Fertilisation
            pass
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des notifications de maintenance: {str(e)}")
    
    def generate_weather_alerts(self):
        """Génère les alertes météorologiques."""
        try:
            # TODO: Implémenter la génération d'alertes météo
            # - Gel
            # - Canicule
            # - Orage
            # - Sécheresse
            pass
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des alertes météo: {str(e)}")


class NotificationBatchProcessor:
    """Processeur de notifications par lots pour optimiser les performances."""
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.batch_size = 100
    
    def process_batch(self, notifications: List[Notification]):
        """Traite un lot de notifications."""
        try:
            for notification in notifications:
                try:
                    self.notification_service.send_notification(notification)
                except Exception as e:
                    logger.error(f"Erreur lors du traitement de la notification {notification.id}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Erreur lors du traitement du lot: {str(e)}")
    
    def process_all_pending(self):
        """Traite toutes les notifications en attente par lots."""
        try:
            total_processed = 0
            
            while True:
                # Récupérer un lot de notifications
                notifications = Notification.query.filter(
                    Notification.status == NotificationStatus.SCHEDULED,
                    Notification.scheduled_for <= datetime.utcnow()
                ).limit(self.batch_size).all()
                
                if not notifications:
                    break
                
                self.process_batch(notifications)
                total_processed += len(notifications)
                
                # Petit délai entre les lots
                time.sleep(0.1)
            
            if total_processed > 0:
                logger.info(f"Traité {total_processed} notifications en lots")
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement par lots: {str(e)}")


# Instance globale du scheduler
notification_scheduler = NotificationScheduler()
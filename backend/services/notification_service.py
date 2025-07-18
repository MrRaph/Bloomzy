"""
Service de gestion des notifications.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.user import db
from models.notification import (
    Notification, NotificationPreferences, NotificationTemplate,
    NotificationDeliveryLog, NotificationType, NotificationStatus,
    NotificationChannel
)
from models.user import User
from models.user_plant import UserPlant
from services.weather_service import WeatherService
import json

logger = logging.getLogger(__name__)


class NotificationService:
    """Service principal pour la gestion des notifications."""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.default_channels = ['push', 'web']
        self.spam_prevention = SpamPrevention()
    
    def create_default_preferences(self, user_id: str) -> List[NotificationPreferences]:
        """Crée les préférences par défaut pour un utilisateur."""
        try:
            preferences = []
            
            # Préférences par défaut pour chaque type de notification
            default_settings = {
                NotificationType.WATERING: {
                    'enabled': True,
                    'preferred_channels': ['push', 'web'],
                    'preferred_hour': 9,
                    'frequency': 'normal'
                },
                NotificationType.HARVEST: {
                    'enabled': True,
                    'preferred_channels': ['push', 'web'],
                    'preferred_hour': 8,
                    'frequency': 'normal'
                },
                NotificationType.PLANTING: {
                    'enabled': True,
                    'preferred_channels': ['push', 'web'],
                    'preferred_hour': 9,
                    'frequency': 'normal'
                },
                NotificationType.MAINTENANCE: {
                    'enabled': True,
                    'preferred_channels': ['push', 'web'],
                    'preferred_hour': 10,
                    'frequency': 'reduced'
                },
                NotificationType.WEATHER_ALERT: {
                    'enabled': True,
                    'preferred_channels': ['push', 'email'],
                    'preferred_hour': 7,
                    'frequency': 'normal'
                },
                NotificationType.PLANT_CARE_GUIDE: {
                    'enabled': True,
                    'preferred_channels': ['web'],
                    'preferred_hour': 11,
                    'frequency': 'reduced'
                }
            }
            
            for notification_type, settings in default_settings.items():
                preference = NotificationPreferences(
                    user_id=user_id,
                    notification_type=notification_type,
                    enabled=settings['enabled'],
                    preferred_channels=settings['preferred_channels'],
                    preferred_hour=settings['preferred_hour'],
                    frequency=settings['frequency']
                )
                preferences.append(preference)
                db.session.add(preference)
            
            db.session.commit()
            logger.info(f"Préférences par défaut créées pour l'utilisateur {user_id}")
            return preferences
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des préférences par défaut: {str(e)}")
            db.session.rollback()
            return []
    
    def get_user_preferences(self, user_id: str) -> Dict[NotificationType, NotificationPreferences]:
        """Récupère les préférences d'un utilisateur."""
        preferences = NotificationPreferences.query.filter_by(user_id=user_id).all()
        
        if not preferences:
            preferences = self.create_default_preferences(user_id)
        
        return {pref.notification_type: pref for pref in preferences}
    
    def can_send_notification(self, user_id: str, notification_type: NotificationType) -> bool:
        """Vérifie si une notification peut être envoyée."""
        try:
            # Vérifier les préférences utilisateur
            preferences = self.get_user_preferences(user_id)
            user_pref = preferences.get(notification_type)
            
            if not user_pref or not user_pref.enabled:
                return False
            
            # Vérifier les limites anti-spam
            if not self.spam_prevention.can_send_notification(user_id, notification_type):
                return False
            
            # Vérifier les heures de silence
            if self.is_in_quiet_hours(user_pref):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des permissions: {str(e)}")
            return False
    
    def is_in_quiet_hours(self, preference: NotificationPreferences) -> bool:
        """Vérifie si nous sommes dans les heures de silence."""
        if not preference.quiet_hours_start or not preference.quiet_hours_end:
            return False
        
        current_time = datetime.now().time()
        
        # Gestion des heures de silence qui passent minuit
        if preference.quiet_hours_start <= preference.quiet_hours_end:
            return preference.quiet_hours_start <= current_time <= preference.quiet_hours_end
        else:
            return current_time >= preference.quiet_hours_start or current_time <= preference.quiet_hours_end
    
    def calculate_optimal_time(self, user_id: str, notification_type: NotificationType, 
                              target_date: datetime = None) -> datetime:
        """Calcule l'heure optimale pour envoyer une notification."""
        try:
            preferences = self.get_user_preferences(user_id)
            user_pref = preferences.get(notification_type)
            
            if not user_pref:
                preferred_hour = 9  # Par défaut
            else:
                preferred_hour = user_pref.preferred_hour
            
            # Date cible (aujourd'hui par défaut)
            if target_date is None:
                target_date = datetime.now().date()
            elif isinstance(target_date, datetime):
                target_date = target_date.date()
            
            # Ajustement selon le type de notification
            if notification_type == NotificationType.WATERING:
                # Arrosage de préférence le matin
                preferred_hour = min(preferred_hour, 10)
            elif notification_type == NotificationType.HARVEST:
                # Récolte en matinée
                preferred_hour = min(preferred_hour, 11)
            elif notification_type == NotificationType.WEATHER_ALERT:
                # Alertes météo tôt le matin
                preferred_hour = min(preferred_hour, 8)
            
            optimal_time = datetime.combine(target_date, datetime.min.time().replace(hour=preferred_hour))
            
            # Vérifier que ce n'est pas dans le passé
            if optimal_time < datetime.now():
                optimal_time = datetime.now() + timedelta(minutes=5)
            
            return optimal_time
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de l'heure optimale: {str(e)}")
            return datetime.now() + timedelta(minutes=5)
    
    def create_watering_notification(self, user_plant: UserPlant, urgency_level: int = 5) -> Notification:
        """Crée une notification d'arrosage pour une plante."""
        try:
            # Déterminer le niveau d'urgence
            if urgency_level >= 8:
                title = f"🚨 {user_plant.name} a soif !"
                priority = 9
            elif urgency_level >= 6:
                title = f"💧 Temps d'arroser {user_plant.name}"
                priority = 7
            else:
                title = f"🌱 {user_plant.name} aura bientôt besoin d'eau"
                priority = 5
            
            # Contenu avec conseils contextuels
            content = f"Votre {user_plant.species.common_name} "
            
            if urgency_level >= 8:
                content += "semble avoir vraiment soif. Un arrosage est recommandé dès maintenant."
            elif urgency_level >= 6:
                content += "a besoin d'être arrosée. Le moment est idéal pour l'arroser."
            else:
                content += "aura bientôt besoin d'eau. Préparez-vous pour l'arrosage."
            
            # Ajouter des conseils météo si disponible
            try:
                weather_data = self.weather_service.get_current_weather()
                if weather_data:
                    content += self.add_weather_context(content, weather_data, 'watering')
            except Exception:
                pass  # Continuer sans contexte météo
            
            # Créer la notification
            notification = Notification(
                user_id=user_plant.user_id,
                type=NotificationType.WATERING,
                title=title,
                content=content,
                scheduled_for=self.calculate_optimal_time(user_plant.user_id, NotificationType.WATERING),
                priority=priority,
                channels=self.get_preferred_channels(user_plant.user_id, NotificationType.WATERING),
                data={
                    'plant_id': user_plant.id,
                    'plant_name': user_plant.name,
                    'urgency_level': urgency_level
                }
            )
            
            return notification
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la notification d'arrosage: {str(e)}")
            return None
    
    def add_weather_context(self, base_content: str, weather_data: dict, notification_type: str) -> str:
        """Ajoute du contexte météorologique au contenu de la notification."""
        weather_additions = []
        
        if notification_type == 'watering':
            if weather_data.get('precipitation_forecast', 0) > 5:
                weather_additions.append("☔ Pluie prévue dans les prochaines heures, vous pourriez reporter l'arrosage.")
            elif weather_data.get('temperature', 0) > 28:
                weather_additions.append("🌡️ Température élevée, arrosez de préférence tôt le matin ou en soirée.")
            elif weather_data.get('humidity', 50) < 40:
                weather_additions.append("💨 Air sec aujourd'hui, vos plantes peuvent avoir besoin d'un arrosage plus généreux.")
        
        if weather_additions:
            return base_content + "\n\n" + "\n".join(weather_additions)
        
        return base_content
    
    def get_preferred_channels(self, user_id: str, notification_type: NotificationType) -> List[str]:
        """Récupère les canaux préférés pour un type de notification."""
        try:
            preferences = self.get_user_preferences(user_id)
            user_pref = preferences.get(notification_type)
            
            if user_pref and user_pref.preferred_channels:
                return user_pref.preferred_channels
            
            return self.default_channels
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des canaux préférés: {str(e)}")
            return self.default_channels
    
    def send_notification(self, notification: Notification) -> bool:
        """Envoie une notification via tous les canaux configurés."""
        try:
            if not self.can_send_notification(notification.user_id, notification.type):
                logger.info(f"Notification {notification.id} bloquée par les préférences utilisateur")
                return False
            
            delivery_success = False
            
            for channel in notification.channels:
                try:
                    channel_enum = NotificationChannel(channel)
                    success = self.send_via_channel(notification, channel_enum)
                    
                    # Log de livraison
                    log = NotificationDeliveryLog(
                        notification_id=notification.id,
                        channel=channel_enum,
                        success=success,
                        error_message=None if success else "Échec de livraison"
                    )
                    db.session.add(log)
                    
                    if success:
                        delivery_success = True
                        
                except ValueError:
                    logger.warning(f"Canal invalide: {channel}")
                    continue
                except Exception as e:
                    logger.error(f"Erreur lors de l'envoi via {channel}: {str(e)}")
                    continue
            
            # Mettre à jour le statut de la notification
            if delivery_success:
                notification.mark_as_sent()
                self.spam_prevention.record_notification_sent(notification.user_id, notification.type)
            else:
                notification.status = NotificationStatus.FAILED
                notification.updated_at = datetime.utcnow()
            
            db.session.commit()
            return delivery_success
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la notification: {str(e)}")
            return False
    
    def send_via_channel(self, notification: Notification, channel: NotificationChannel) -> bool:
        """Envoie une notification via un canal spécifique."""
        try:
            if channel == NotificationChannel.PUSH:
                return self.send_push_notification(notification)
            elif channel == NotificationChannel.EMAIL:
                return self.send_email_notification(notification)
            elif channel == NotificationChannel.SMS:
                return self.send_sms_notification(notification)
            elif channel == NotificationChannel.WEB:
                return self.send_web_notification(notification)
            else:
                logger.warning(f"Canal non supporté: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi via {channel}: {str(e)}")
            return False
    
    def send_push_notification(self, notification: Notification) -> bool:
        """Envoie une notification push."""
        try:
            # TODO: Implémenter avec Firebase Cloud Messaging
            logger.info(f"Envoi notification push: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi push: {str(e)}")
            return False
    
    def send_email_notification(self, notification: Notification) -> bool:
        """Envoie une notification email."""
        try:
            # TODO: Implémenter avec service email
            logger.info(f"Envoi notification email: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {str(e)}")
            return False
    
    def send_sms_notification(self, notification: Notification) -> bool:
        """Envoie une notification SMS."""
        try:
            # TODO: Implémenter avec service SMS
            logger.info(f"Envoi notification SMS: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi SMS: {str(e)}")
            return False
    
    def send_web_notification(self, notification: Notification) -> bool:
        """Envoie une notification web (stockée en base)."""
        try:
            # Les notifications web sont déjà stockées en base
            logger.info(f"Notification web créée: {notification.title}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur notification web: {str(e)}")
            return False


class SpamPrevention:
    """Service de prévention du spam de notifications."""
    
    def __init__(self):
        self.max_notifications_per_hour = 3
        self.max_notifications_per_day = 15
        self.type_limits = {
            NotificationType.WATERING: 5,
            NotificationType.HARVEST: 3,
            NotificationType.PLANTING: 2,
            NotificationType.MAINTENANCE: 3,
            NotificationType.WEATHER_ALERT: 2,
            NotificationType.PLANT_CARE_GUIDE: 2
        }
    
    def can_send_notification(self, user_id: str, notification_type: NotificationType) -> bool:
        """Vérifie si une notification peut être envoyée selon les limites anti-spam."""
        try:
            # Vérifier les limites horaires
            hourly_count = self.get_hourly_count(user_id)
            if hourly_count >= self.max_notifications_per_hour:
                return False
            
            # Vérifier les limites quotidiennes
            daily_count = self.get_daily_count(user_id)
            if daily_count >= self.max_notifications_per_day:
                return False
            
            # Vérifier les limites par type
            type_count = self.get_type_count(user_id, notification_type)
            type_limit = self.type_limits.get(notification_type, 2)
            if type_count >= type_limit:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification anti-spam: {str(e)}")
            return True  # En cas d'erreur, permettre l'envoi
    
    def get_hourly_count(self, user_id: str) -> int:
        """Récupère le nombre de notifications envoyées dans la dernière heure."""
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        return Notification.query.filter(
            Notification.user_id == user_id,
            Notification.sent_at >= one_hour_ago,
            Notification.status == NotificationStatus.SENT
        ).count()
    
    def get_daily_count(self, user_id: str) -> int:
        """Récupère le nombre de notifications envoyées dans les dernières 24h."""
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        return Notification.query.filter(
            Notification.user_id == user_id,
            Notification.sent_at >= one_day_ago,
            Notification.status == NotificationStatus.SENT
        ).count()
    
    def get_type_count(self, user_id: str, notification_type: NotificationType) -> int:
        """Récupère le nombre de notifications d'un type envoyées dans les dernières 24h."""
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        return Notification.query.filter(
            Notification.user_id == user_id,
            Notification.type == notification_type,
            Notification.sent_at >= one_day_ago,
            Notification.status == NotificationStatus.SENT
        ).count()
    
    def record_notification_sent(self, user_id: str, notification_type: NotificationType):
        """Enregistre qu'une notification a été envoyée."""
        # Cette méthode est principalement pour la cohérence avec le PRD
        # L'enregistrement se fait déjà via le model Notification
        pass
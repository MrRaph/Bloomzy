"""
Tests pour le service de notifications.
"""
import pytest
from datetime import datetime, timedelta, time
from unittest.mock import Mock, patch
from services.notification_service import NotificationService, SpamPrevention
from models.notification import (
    Notification, NotificationPreferences, NotificationType, 
    NotificationStatus, NotificationChannel
)
from models.user_plant import UserPlant
from models.indoor_plant import IndoorPlant


class TestNotificationService:
    """Tests du service de notifications."""
    
    def test_create_default_preferences(self, app, db_session, test_user):
        """Test de création des préférences par défaut."""
        with app.app_context():
            service = NotificationService()
            
            # Vérifier qu'il n'y a pas de préférences existantes
            existing_prefs = NotificationPreferences.query.filter_by(user_id=test_user.id).all()
            assert len(existing_prefs) == 0
            
            # Créer les préférences par défaut
            preferences = service.create_default_preferences(test_user.id)
            
            # Vérifier que toutes les préférences ont été créées
            assert len(preferences) == 6  # 6 types de notifications
            
            # Vérifier les préférences d'arrosage
            watering_pref = next(p for p in preferences if p.notification_type == NotificationType.WATERING)
            assert watering_pref.enabled is True
            assert watering_pref.preferred_hour == 9
            assert 'push' in watering_pref.preferred_channels
            assert 'web' in watering_pref.preferred_channels
    
    def test_get_user_preferences(self, app, db_session, test_user):
        """Test de récupération des préférences utilisateur."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence personnalisée
            custom_pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=False,
                preferred_channels=['email'],
                preferred_hour=7,
                frequency='reduced'
            )
            db_session.add(custom_pref)
            db_session.commit()
            
            # Récupérer les préférences
            preferences = service.get_user_preferences(test_user.id)
            
            # Vérifier que les préférences par défaut sont créées pour les autres types
            assert len(preferences) == 6
            
            # Vérifier la préférence personnalisée
            watering_pref = preferences[NotificationType.WATERING]
            assert watering_pref.enabled is False
            assert watering_pref.preferred_channels == ['email']
            assert watering_pref.preferred_hour == 7
            assert watering_pref.frequency == 'reduced'
    
    def test_can_send_notification(self, app, db_session, test_user):
        """Test de vérification des permissions d'envoi."""
        with app.app_context():
            service = NotificationService()
            
            # Créer des préférences avec notifications activées
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=True,
                preferred_channels=['push']
            )
            db_session.add(pref)
            db_session.commit()
            
            # Vérifier que l'envoi est autorisé
            can_send = service.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is True
            
            # Désactiver les notifications
            pref.enabled = False
            db_session.commit()
            
            # Vérifier que l'envoi est bloqué
            can_send = service.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is False
    
    def test_is_in_quiet_hours(self, app, db_session, test_user):
        """Test de vérification des heures de silence."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence avec heures de silence (22h - 8h)
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                quiet_hours_start=time(22, 0),
                quiet_hours_end=time(8, 0)
            )
            
            # Simuler différentes heures
            with patch('datetime.datetime') as mock_datetime:
                # 2h du matin (dans les heures de silence)
                mock_datetime.now.return_value.time.return_value = time(2, 0)
                assert service.is_in_quiet_hours(pref) is True
                
                # 10h du matin (hors heures de silence)
                mock_datetime.now.return_value.time.return_value = time(10, 0)
                assert service.is_in_quiet_hours(pref) is False
                
                # 23h (dans les heures de silence)
                mock_datetime.now.return_value.time.return_value = time(23, 0)
                assert service.is_in_quiet_hours(pref) is True
    
    def test_calculate_optimal_time(self, app, db_session, test_user):
        """Test de calcul de l'heure optimale."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence avec heure préférée
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                preferred_hour=9
            )
            db_session.add(pref)
            db_session.commit()
            
            # Calculer l'heure optimale pour aujourd'hui
            optimal_time = service.calculate_optimal_time(test_user.id, NotificationType.WATERING)
            
            # Vérifier que l'heure est correcte
            assert optimal_time.hour == 9
            assert optimal_time.date() == datetime.now().date()
    
    def test_calculate_optimal_time_watering_adjustment(self, app, db_session, test_user):
        """Test d'ajustement d'heure pour les notifications d'arrosage."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence avec heure tardive
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                preferred_hour=15  # 15h
            )
            db_session.add(pref)
            db_session.commit()
            
            # Calculer l'heure optimale pour arrosage
            optimal_time = service.calculate_optimal_time(test_user.id, NotificationType.WATERING)
            
            # Vérifier que l'heure est ajustée (max 10h pour arrosage)
            assert optimal_time.hour == 10
    
    def test_get_preferred_channels(self, app, db_session, test_user):
        """Test de récupération des canaux préférés."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence avec canaux spécifiques
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                preferred_channels=['push', 'email']
            )
            db_session.add(pref)
            db_session.commit()
            
            # Récupérer les canaux préférés
            channels = service.get_preferred_channels(test_user.id, NotificationType.WATERING)
            
            assert channels == ['push', 'email']
    
    def test_get_preferred_channels_default(self, app, db_session, test_user):
        """Test de récupération des canaux par défaut."""
        with app.app_context():
            service = NotificationService()
            
            # Récupérer les canaux pour un type sans préférence
            channels = service.get_preferred_channels(test_user.id, NotificationType.HARVEST)
            
            # Vérifier que les canaux par défaut sont retournés
            assert channels == service.default_channels
    
    @patch('services.notification_service.NotificationService.send_via_channel')
    def test_send_notification_success(self, mock_send_via_channel, app, db_session, test_user):
        """Test d'envoi réussi d'une notification."""
        with app.app_context():
            service = NotificationService()
            mock_send_via_channel.return_value = True
            
            # Créer une préférence
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=True,
                preferred_channels=['push']
            )
            db_session.add(pref)
            db_session.commit()
            
            # Créer une notification
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                channels=['push']
            )
            db_session.add(notification)
            db_session.commit()
            
            # Envoyer la notification
            success = service.send_notification(notification)
            
            assert success is True
            assert notification.status == NotificationStatus.SENT
            assert notification.sent_at is not None
    
    @patch('services.notification_service.NotificationService.send_via_channel')
    def test_send_notification_blocked_by_preferences(self, mock_send_via_channel, app, db_session, test_user):
        """Test de blocage d'envoi par les préférences."""
        with app.app_context():
            service = NotificationService()
            
            # Créer une préférence avec notifications désactivées
            pref = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=False
            )
            db_session.add(pref)
            db_session.commit()
            
            # Créer une notification
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                channels=['push']
            )
            db_session.add(notification)
            db_session.commit()
            
            # Envoyer la notification
            success = service.send_notification(notification)
            
            assert success is False
            assert notification.status == NotificationStatus.SCHEDULED  # Reste inchangé
            # Le mock ne devrait pas être appelé
            mock_send_via_channel.assert_not_called()


class TestSpamPrevention:
    """Tests du système de prévention du spam."""
    
    def test_can_send_notification_within_limits(self, app, db_session, test_user):
        """Test d'envoi autorisé dans les limites."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Vérifier que l'envoi est autorisé (pas de notifications existantes)
            can_send = spam_prevention.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is True
    
    def test_can_send_notification_hourly_limit(self, app, db_session, test_user):
        """Test de limite horaire."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Créer 3 notifications dans la dernière heure (limite atteinte)
            for i in range(3):
                notification = Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title=f"Test {i}",
                    content=f"Content {i}",
                    scheduled_for=datetime.utcnow(),
                    status=NotificationStatus.SENT,
                    sent_at=datetime.utcnow() - timedelta(minutes=30)
                )
                db_session.add(notification)
            
            db_session.commit()
            
            # Vérifier que la limite horaire est atteinte
            can_send = spam_prevention.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is False
    
    def test_can_send_notification_daily_limit(self, app, db_session, test_user):
        """Test de limite quotidienne."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Créer 15 notifications dans les dernières 24h (limite atteinte)
            for i in range(15):
                notification = Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title=f"Test {i}",
                    content=f"Content {i}",
                    scheduled_for=datetime.utcnow(),
                    status=NotificationStatus.SENT,
                    sent_at=datetime.utcnow() - timedelta(hours=i)
                )
                db_session.add(notification)
            
            db_session.commit()
            
            # Vérifier que la limite quotidienne est atteinte
            can_send = spam_prevention.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is False
    
    def test_can_send_notification_type_limit(self, app, db_session, test_user):
        """Test de limite par type."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Créer 5 notifications d'arrosage (limite pour ce type)
            for i in range(5):
                notification = Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title=f"Test {i}",
                    content=f"Content {i}",
                    scheduled_for=datetime.utcnow(),
                    status=NotificationStatus.SENT,
                    sent_at=datetime.utcnow() - timedelta(hours=i)
                )
                db_session.add(notification)
            
            db_session.commit()
            
            # Vérifier que la limite par type est atteinte
            can_send = spam_prevention.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is False
    
    def test_can_send_notification_old_notifications_ignored(self, app, db_session, test_user):
        """Test que les anciennes notifications sont ignorées."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Créer une notification vieille de 2 jours
            old_notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Old notification",
                content="Old content",
                scheduled_for=datetime.utcnow() - timedelta(days=2),
                status=NotificationStatus.SENT,
                sent_at=datetime.utcnow() - timedelta(days=2)
            )
            db_session.add(old_notification)
            db_session.commit()
            
            # Vérifier que l'envoi est autorisé (notification trop ancienne)
            can_send = spam_prevention.can_send_notification(test_user.id, NotificationType.WATERING)
            assert can_send is True
    
    def test_get_counts_methods(self, app, db_session, test_user):
        """Test des méthodes de comptage."""
        with app.app_context():
            spam_prevention = SpamPrevention()
            
            # Créer différentes notifications
            notifications_data = [
                (datetime.utcnow() - timedelta(minutes=30), NotificationType.WATERING),
                (datetime.utcnow() - timedelta(hours=2), NotificationType.WATERING),
                (datetime.utcnow() - timedelta(hours=12), NotificationType.HARVEST),
                (datetime.utcnow() - timedelta(days=2), NotificationType.WATERING),  # Trop ancienne
            ]
            
            for sent_at, notif_type in notifications_data:
                notification = Notification(
                    user_id=test_user.id,
                    type=notif_type,
                    title="Test",
                    content="Content",
                    scheduled_for=sent_at,
                    status=NotificationStatus.SENT,
                    sent_at=sent_at
                )
                db_session.add(notification)
            
            db_session.commit()
            
            # Tester les comptages
            hourly_count = spam_prevention.get_hourly_count(test_user.id)
            daily_count = spam_prevention.get_daily_count(test_user.id)
            watering_count = spam_prevention.get_type_count(test_user.id, NotificationType.WATERING)
            harvest_count = spam_prevention.get_type_count(test_user.id, NotificationType.HARVEST)
            
            assert hourly_count == 1  # Seule la notification de 30 min
            assert daily_count == 3   # 3 notifications dans les 24h
            assert watering_count == 2  # 2 notifications d'arrosage dans les 24h
            assert harvest_count == 1   # 1 notification de récolte dans les 24h
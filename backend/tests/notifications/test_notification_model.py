"""
Tests pour le modèle Notification.
"""
import pytest
from datetime import datetime, timedelta
from models.notification import (
    Notification, NotificationPreferences, NotificationTemplate,
    NotificationDeliveryLog, NotificationType, NotificationStatus,
    NotificationChannel
)
from models.user import User


class TestNotificationModel:
    """Tests du modèle Notification."""
    
    def test_create_notification(self, app, db_session, test_user):
        """Test de création d'une notification."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test de notification",
                content="Contenu de test",
                scheduled_for=datetime.utcnow() + timedelta(hours=1),
                priority=5,
                channels=['push', 'web'],
                metadata={'plant_id': 'test-plant-id'}
            )
            
            db_session.add(notification)
            db_session.commit()
            
            assert notification.id is not None
            assert notification.user_id == test_user.id
            assert notification.type == NotificationType.WATERING
            assert notification.title == "Test de notification"
            assert notification.content == "Contenu de test"
            assert notification.status == NotificationStatus.SCHEDULED
            assert notification.priority == 5
            assert notification.channels == ['push', 'web']
            assert notification.metadata['plant_id'] == 'test-plant-id'
    
    def test_notification_to_dict(self, app, db_session, test_user):
        """Test de conversion en dictionnaire."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.HARVEST,
                title="Test harvest",
                content="Harvest content",
                scheduled_for=datetime.utcnow() + timedelta(hours=2),
                priority=7,
                channels=['email'],
                metadata={'garden_id': 'test-garden-id'}
            )
            
            db_session.add(notification)
            db_session.commit()
            
            data = notification.to_dict()
            
            assert data['id'] == notification.id
            assert data['user_id'] == test_user.id
            assert data['type'] == 'harvest'
            assert data['title'] == "Test harvest"
            assert data['content'] == "Harvest content"
            assert data['status'] == 'scheduled'
            assert data['priority'] == 7
            assert data['channels'] == ['email']
            assert data['metadata']['garden_id'] == 'test-garden-id'
    
    def test_mark_as_sent(self, app, db_session, test_user):
        """Test de marquage comme envoyée."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            assert notification.status == NotificationStatus.SCHEDULED
            assert notification.sent_at is None
            
            notification.mark_as_sent()
            
            assert notification.status == NotificationStatus.SENT
            assert notification.sent_at is not None
    
    def test_mark_as_opened(self, app, db_session, test_user):
        """Test de marquage comme ouverte."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            assert notification.status == NotificationStatus.SCHEDULED
            assert notification.opened_at is None
            
            notification.mark_as_opened()
            
            assert notification.status == NotificationStatus.OPENED
            assert notification.opened_at is not None
    
    def test_mark_as_acted_upon(self, app, db_session, test_user):
        """Test de marquage avec action."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            assert notification.status == NotificationStatus.SCHEDULED
            assert notification.user_action is None
            assert notification.action_taken_at is None
            
            notification.mark_as_acted_upon("watered_plant")
            
            assert notification.status == NotificationStatus.ACTED_UPON
            assert notification.user_action == "watered_plant"
            assert notification.action_taken_at is not None
    
    def test_cancel_notification(self, app, db_session, test_user):
        """Test d'annulation d'une notification."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow() + timedelta(hours=1)
            )
            
            db_session.add(notification)
            db_session.commit()
            
            assert notification.status == NotificationStatus.SCHEDULED
            
            notification.cancel()
            
            assert notification.status == NotificationStatus.CANCELLED


class TestNotificationPreferencesModel:
    """Tests du modèle NotificationPreferences."""
    
    def test_create_preferences(self, app, db_session, test_user):
        """Test de création de préférences."""
        with app.app_context():
            preferences = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=True,
                preferred_channels=['push', 'email'],
                preferred_hour=9,
                frequency='normal'
            )
            
            db_session.add(preferences)
            db_session.commit()
            
            assert preferences.id is not None
            assert preferences.user_id == test_user.id
            assert preferences.notification_type == NotificationType.WATERING
            assert preferences.enabled is True
            assert preferences.preferred_channels == ['push', 'email']
            assert preferences.preferred_hour == 9
            assert preferences.frequency == 'normal'
    
    def test_preferences_to_dict(self, app, db_session, test_user):
        """Test de conversion des préférences en dictionnaire."""
        with app.app_context():
            preferences = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.HARVEST,
                enabled=False,
                preferred_channels=['sms'],
                preferred_hour=8,
                frequency='reduced'
            )
            
            db_session.add(preferences)
            db_session.commit()
            
            data = preferences.to_dict()
            
            assert data['id'] == preferences.id
            assert data['user_id'] == test_user.id
            assert data['notification_type'] == 'harvest'
            assert data['enabled'] is False
            assert data['preferred_channels'] == ['sms']
            assert data['preferred_hour'] == 8
            assert data['frequency'] == 'reduced'


class TestNotificationTemplateModel:
    """Tests du modèle NotificationTemplate."""
    
    def test_create_template(self, app, db_session):
        """Test de création d'un template."""
        with app.app_context():
            template = NotificationTemplate(
                type=NotificationType.WATERING,
                priority=5,
                title_template="Il est temps d'arroser {plant_name}",
                content_template="Votre {plant_species} a besoin d'eau. Dernière fois: {last_watering}",
                variables=['plant_name', 'plant_species', 'last_watering'],
                localization='fr'
            )
            
            db_session.add(template)
            db_session.commit()
            
            assert template.id is not None
            assert template.type == NotificationType.WATERING
            assert template.priority == 5
            assert 'plant_name' in template.title_template
            assert 'plant_species' in template.content_template
            assert template.variables == ['plant_name', 'plant_species', 'last_watering']
            assert template.localization == 'fr'
    
    def test_template_render(self, app, db_session):
        """Test de rendu d'un template."""
        with app.app_context():
            template = NotificationTemplate(
                type=NotificationType.WATERING,
                title_template="Arroser {plant_name}",
                content_template="Votre {plant_species} ({plant_name}) a besoin d'eau",
                variables=['plant_name', 'plant_species']
            )
            
            variables = {
                'plant_name': 'Monstera',
                'plant_species': 'Monstera deliciosa'
            }
            
            title, content = template.render(variables)
            
            assert title == "Arroser Monstera"
            assert content == "Votre Monstera deliciosa (Monstera) a besoin d'eau"
    
    def test_template_to_dict(self, app, db_session):
        """Test de conversion du template en dictionnaire."""
        with app.app_context():
            template = NotificationTemplate(
                type=NotificationType.PLANTING,
                priority=3,
                title_template="Temps de planter {crop_name}",
                content_template="C'est le moment idéal pour planter {crop_name}",
                variables=['crop_name'],
                localization='fr'
            )
            
            db_session.add(template)
            db_session.commit()
            
            data = template.to_dict()
            
            assert data['id'] == template.id
            assert data['type'] == 'planting'
            assert data['priority'] == 3
            assert data['title_template'] == "Temps de planter {crop_name}"
            assert data['content_template'] == "C'est le moment idéal pour planter {crop_name}"
            assert data['variables'] == ['crop_name']
            assert data['localization'] == 'fr'


class TestNotificationDeliveryLogModel:
    """Tests du modèle NotificationDeliveryLog."""
    
    def test_create_delivery_log(self, app, db_session, test_user):
        """Test de création d'un log de livraison."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            delivery_log = NotificationDeliveryLog(
                notification_id=notification.id,
                channel=NotificationChannel.PUSH,
                success=True,
                delivery_metadata={'message_id': 'test-123'}
            )
            
            db_session.add(delivery_log)
            db_session.commit()
            
            assert delivery_log.id is not None
            assert delivery_log.notification_id == notification.id
            assert delivery_log.channel == NotificationChannel.PUSH
            assert delivery_log.success is True
            assert delivery_log.error_message is None
            assert delivery_log.delivery_metadata['message_id'] == 'test-123'
    
    def test_delivery_log_failure(self, app, db_session, test_user):
        """Test de log d'échec de livraison."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            delivery_log = NotificationDeliveryLog(
                notification_id=notification.id,
                channel=NotificationChannel.EMAIL,
                success=False,
                error_message="Email address not found"
            )
            
            db_session.add(delivery_log)
            db_session.commit()
            
            assert delivery_log.id is not None
            assert delivery_log.notification_id == notification.id
            assert delivery_log.channel == NotificationChannel.EMAIL
            assert delivery_log.success is False
            assert delivery_log.error_message == "Email address not found"
    
    def test_delivery_log_to_dict(self, app, db_session, test_user):
        """Test de conversion du log en dictionnaire."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow()
            )
            
            db_session.add(notification)
            db_session.commit()
            
            delivery_log = NotificationDeliveryLog(
                notification_id=notification.id,
                channel=NotificationChannel.SMS,
                success=True,
                delivery_metadata={'sms_id': 'sms-456'}
            )
            
            db_session.add(delivery_log)
            db_session.commit()
            
            data = delivery_log.to_dict()
            
            assert data['id'] == delivery_log.id
            assert data['notification_id'] == notification.id
            assert data['channel'] == 'sms'
            assert data['success'] is True
            assert data['error_message'] is None
            assert data['delivery_metadata']['sms_id'] == 'sms-456'
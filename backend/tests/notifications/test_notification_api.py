"""
Tests d'intégration pour l'API des notifications.
"""
import pytest
import json
from datetime import datetime, timedelta
from models.notification import (
    Notification, NotificationPreferences, NotificationType, 
    NotificationStatus, NotificationChannel
)


class TestNotificationAPI:
    """Tests de l'API des notifications."""
    
    def test_get_user_notifications(self, app, client, auth_headers, test_user, db_session):
        """Test de récupération des notifications utilisateur."""
        with app.app_context():
            # Créer des notifications de test
            notifications = [
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title="Notification 1",
                    content="Content 1",
                    scheduled_for=datetime.utcnow() - timedelta(hours=1),
                    status=NotificationStatus.SENT
                ),
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.HARVEST,
                    title="Notification 2",
                    content="Content 2",
                    scheduled_for=datetime.utcnow() - timedelta(hours=2),
                    status=NotificationStatus.SCHEDULED
                )
            ]
            
            for notification in notifications:
                db_session.add(notification)
            db_session.commit()
            
            # Faire la requête
            response = client.get('/api/notifications', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'notifications' in data
            assert len(data['notifications']) == 2
            assert data['total'] == 2
            assert data['limit'] == 50
            assert data['offset'] == 0
            
            # Vérifier l'ordre (plus récent en premier)
            assert data['notifications'][0]['title'] == "Notification 1"
            assert data['notifications'][1]['title'] == "Notification 2"
    
    def test_get_user_notifications_filtered(self, app, client, auth_headers, test_user, db_session):
        """Test de filtrage des notifications."""
        with app.app_context():
            # Créer des notifications de différents types
            notifications = [
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title="Watering notification",
                    content="Content",
                    scheduled_for=datetime.utcnow(),
                    status=NotificationStatus.SENT
                ),
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.HARVEST,
                    title="Harvest notification",
                    content="Content",
                    scheduled_for=datetime.utcnow(),
                    status=NotificationStatus.SCHEDULED
                )
            ]
            
            for notification in notifications:
                db_session.add(notification)
            db_session.commit()
            
            # Filtrer par type
            response = client.get('/api/notifications?type=watering', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert len(data['notifications']) == 1
            assert data['notifications'][0]['type'] == 'watering'
    
    def test_get_user_notifications_pagination(self, app, client, auth_headers, test_user, db_session):
        """Test de pagination des notifications."""
        with app.app_context():
            # Créer 5 notifications
            for i in range(5):
                notification = Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title=f"Notification {i}",
                    content=f"Content {i}",
                    scheduled_for=datetime.utcnow() - timedelta(hours=i),
                    status=NotificationStatus.SENT
                )
                db_session.add(notification)
            db_session.commit()
            
            # Tester la pagination
            response = client.get('/api/notifications?limit=2&offset=1', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert len(data['notifications']) == 2
            assert data['total'] == 5
            assert data['limit'] == 2
            assert data['offset'] == 1
    
    def test_get_notification_by_id(self, app, client, auth_headers, test_user, db_session):
        """Test de récupération d'une notification par ID."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Récupérer la notification
            response = client.get(f'/api/notifications/{notification.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['id'] == notification.id
            assert data['title'] == "Test notification"
            assert data['content'] == "Test content"
            assert data['type'] == 'watering'
    
    def test_get_notification_not_found(self, app, client, auth_headers):
        """Test de récupération d'une notification inexistante."""
        response = client.get('/api/notifications/nonexistent-id', headers=auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_mark_notification_opened(self, app, client, auth_headers, test_user, db_session):
        """Test de marquage d'une notification comme ouverte."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Marquer comme ouverte
            response = client.post(f'/api/notifications/{notification.id}/mark-opened', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['notification']['status'] == 'opened'
            assert data['notification']['opened_at'] is not None
    
    def test_mark_notification_acted_upon(self, app, client, auth_headers, test_user, db_session):
        """Test de marquage d'une notification avec action."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Marquer avec action
            response = client.post(
                f'/api/notifications/{notification.id}/mark-acted',
                headers=auth_headers,
                json={'action': 'watered_plant'}
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['notification']['status'] == 'acted_upon'
            assert data['notification']['user_action'] == 'watered_plant'
            assert data['notification']['action_taken_at'] is not None
    
    def test_dismiss_notification(self, app, client, auth_headers, test_user, db_session):
        """Test d'ignorance d'une notification."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Ignorer la notification
            response = client.post(f'/api/notifications/{notification.id}/dismiss', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['notification']['status'] == 'dismissed'
    
    def test_cancel_notification(self, app, client, auth_headers, test_user, db_session):
        """Test d'annulation d'une notification."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow() + timedelta(hours=1),
                status=NotificationStatus.SCHEDULED
            )
            db_session.add(notification)
            db_session.commit()
            
            # Annuler la notification
            response = client.post(f'/api/notifications/{notification.id}/cancel', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['notification']['status'] == 'cancelled'
    
    def test_cancel_notification_invalid_status(self, app, client, auth_headers, test_user, db_session):
        """Test d'annulation d'une notification avec statut invalide."""
        with app.app_context():
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Tenter d'annuler une notification déjà envoyée
            response = client.post(f'/api/notifications/{notification.id}/cancel', headers=auth_headers)
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_get_notification_preferences(self, app, client, auth_headers, test_user, db_session):
        """Test de récupération des préférences."""
        with app.app_context():
            # Créer une préférence personnalisée
            preference = NotificationPreferences(
                user_id=test_user.id,
                notification_type=NotificationType.WATERING,
                enabled=True,
                preferred_channels=['push', 'email'],
                preferred_hour=8,
                frequency='normal'
            )
            db_session.add(preference)
            db_session.commit()
            
            # Récupérer les préférences
            response = client.get('/api/notifications/preferences', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'preferences' in data
            # Vérifier qu'il y a des préférences (par défaut créées + celle personnalisée)
            assert len(data['preferences']) >= 1
            
            # Trouver la préférence d'arrosage
            watering_pref = next(p for p in data['preferences'] if p['notification_type'] == 'watering')
            assert watering_pref['enabled'] is True
            assert watering_pref['preferred_channels'] == ['push', 'email']
            assert watering_pref['preferred_hour'] == 8
    
    def test_update_notification_preferences(self, app, client, auth_headers, test_user, db_session):
        """Test de mise à jour des préférences."""
        with app.app_context():
            # Données de mise à jour
            update_data = {
                'preferences': [
                    {
                        'notification_type': 'watering',
                        'enabled': False,
                        'preferred_channels': ['email'],
                        'preferred_hour': 7,
                        'frequency': 'reduced'
                    },
                    {
                        'notification_type': 'harvest',
                        'enabled': True,
                        'preferred_channels': ['push', 'web'],
                        'preferred_hour': 9,
                        'frequency': 'normal'
                    }
                ]
            }
            
            # Mettre à jour les préférences
            response = client.put(
                '/api/notifications/preferences',
                headers=auth_headers,
                json=update_data
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'preferences' in data
            assert len(data['preferences']) == 2
            
            # Vérifier les préférences mises à jour
            watering_pref = next(p for p in data['preferences'] if p['notification_type'] == 'watering')
            assert watering_pref['enabled'] is False
            assert watering_pref['preferred_channels'] == ['email']
            assert watering_pref['preferred_hour'] == 7
            assert watering_pref['frequency'] == 'reduced'
    
    def test_schedule_notification(self, app, client, auth_headers, test_user, db_session):
        """Test de programmation d'une notification."""
        with app.app_context():
            # Données de la notification
            notification_data = {
                'type': 'watering',
                'title': 'Test notification',
                'content': 'Test content',
                'scheduled_for': (datetime.utcnow() + timedelta(hours=1)).isoformat(),
                'priority': 7,
                'channels': ['push', 'web'],
                'metadata': {'test': True}
            }
            
            # Programmer la notification
            response = client.post(
                '/api/notifications/schedule',
                headers=auth_headers,
                json=notification_data
            )
            
            assert response.status_code == 201
            data = json.loads(response.data)
            
            assert 'notification' in data
            notification = data['notification']
            
            assert notification['type'] == 'watering'
            assert notification['title'] == 'Test notification'
            assert notification['content'] == 'Test content'
            assert notification['priority'] == 7
            assert notification['channels'] == ['push', 'web']
            assert notification['metadata']['test'] is True
    
    def test_schedule_notification_invalid_data(self, app, client, auth_headers):
        """Test de programmation avec données invalides."""
        # Données incomplètes
        notification_data = {
            'type': 'watering',
            'title': 'Test notification'
            # Manque 'content' et 'scheduled_for'
        }
        
        response = client.post(
            '/api/notifications/schedule',
            headers=auth_headers,
            json=notification_data
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_notification_analytics(self, app, client, auth_headers, test_user, db_session):
        """Test de récupération des analytics."""
        with app.app_context():
            # Créer des notifications avec différents statuts
            notifications = [
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title="Notification 1",
                    content="Content 1",
                    scheduled_for=datetime.utcnow() - timedelta(days=1),
                    status=NotificationStatus.SENT
                ),
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.WATERING,
                    title="Notification 2",
                    content="Content 2",
                    scheduled_for=datetime.utcnow() - timedelta(days=2),
                    status=NotificationStatus.OPENED
                ),
                Notification(
                    user_id=test_user.id,
                    type=NotificationType.HARVEST,
                    title="Notification 3",
                    content="Content 3",
                    scheduled_for=datetime.utcnow() - timedelta(days=3),
                    status=NotificationStatus.ACTED_UPON
                )
            ]
            
            for notification in notifications:
                db_session.add(notification)
            db_session.commit()
            
            # Récupérer les analytics
            response = client.get('/api/notifications/analytics', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'analytics' in data
            analytics = data['analytics']
            
            assert analytics['total_notifications'] == 3
            assert analytics['status_breakdown']['sent'] == 1
            assert analytics['status_breakdown']['opened'] == 1
            assert analytics['status_breakdown']['acted_upon'] == 1
            assert analytics['type_breakdown']['watering'] == 2
            assert analytics['type_breakdown']['harvest'] == 1
    
    def test_send_test_notification(self, app, client, auth_headers, test_user, db_session):
        """Test d'envoi d'une notification de test."""
        with app.app_context():
            # Données de test
            test_data = {
                'title': 'Test notification',
                'content': 'Test content',
                'channels': ['push']
            }
            
            # Envoyer la notification de test
            response = client.post(
                '/api/notifications/test',
                headers=auth_headers,
                json=test_data
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'notification' in data
            notification = data['notification']
            
            assert notification['title'] == 'Test notification'
            assert notification['content'] == 'Test content'
            assert notification['channels'] == ['push']
            assert notification['metadata']['test'] is True
    
    def test_get_delivery_logs(self, app, client, auth_headers, test_user, db_session):
        """Test de récupération des logs de livraison."""
        with app.app_context():
            # Créer une notification
            notification = Notification(
                user_id=test_user.id,
                type=NotificationType.WATERING,
                title="Test notification",
                content="Test content",
                scheduled_for=datetime.utcnow(),
                status=NotificationStatus.SENT
            )
            db_session.add(notification)
            db_session.commit()
            
            # Récupérer les logs (même s'ils sont vides pour ce test)
            response = client.get(f'/api/notifications/delivery-logs/{notification.id}', headers=auth_headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert 'notification_id' in data
            assert 'delivery_logs' in data
            assert data['notification_id'] == notification.id
            assert isinstance(data['delivery_logs'], list)
    
    def test_unauthorized_access(self, app, client):
        """Test d'accès non autorisé."""
        # Tenter d'accéder sans token
        response = client.get('/api/notifications')
        
        assert response.status_code == 401
    
    def test_access_other_user_notification(self, app, client, auth_headers, test_user, db_session):
        """Test d'accès à la notification d'un autre utilisateur."""
        with app.app_context():
            # Créer un autre utilisateur
            other_user = User(
                username='otheruser',
                email='other@example.com',
                password_hash='hashed_password'
            )
            db_session.add(other_user)
            db_session.commit()
            
            # Créer une notification pour l'autre utilisateur
            notification = Notification(
                user_id=other_user.id,
                type=NotificationType.WATERING,
                title="Other user notification",
                content="Content",
                scheduled_for=datetime.utcnow()
            )
            db_session.add(notification)
            db_session.commit()
            
            # Tenter d'accéder à la notification de l'autre utilisateur
            response = client.get(f'/api/notifications/{notification.id}', headers=auth_headers)
            
            assert response.status_code == 404  # Pas trouvé car pas le bon utilisateur
"""
Routes pour l'API des notifications.
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from models.user import db, User
from models.notification import (
    Notification, NotificationPreferences, NotificationTemplate,
    NotificationDeliveryLog, NotificationType, NotificationStatus,
    NotificationChannel
)
from routes.auth import jwt_required, get_current_user
from services.notification_service import NotificationService
from services.notification_scheduler import NotificationScheduler
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__)
notification_service = NotificationService()
notification_scheduler = NotificationScheduler()


@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required
def get_user_notifications():
    """
    Récupère les notifications de l'utilisateur connecté.
    
    Query parameters:
    - status: Filtrer par statut (scheduled, sent, delivered, opened, etc.)
    - type: Filtrer par type (watering, harvest, planting, etc.)
    - limit: Nombre maximum de notifications à retourner (défaut: 50)
    - offset: Nombre de notifications à ignorer (défaut: 0)
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Paramètres de requête
        status = request.args.get('status')
        notification_type = request.args.get('type')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Construction de la requête
        query = Notification.query.filter_by(user_id=user.id)
        
        if status:
            try:
                status_enum = NotificationStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Statut invalide'}), 400
        
        if notification_type:
            try:
                type_enum = NotificationType(notification_type)
                query = query.filter_by(type=type_enum)
            except ValueError:
                return jsonify({'error': 'Type de notification invalide'}), 400
        
        # Tri par date de création décroissante
        query = query.order_by(Notification.created_at.desc())
        
        # Pagination
        notifications = query.offset(offset).limit(limit).all()
        
        # Conversion en dictionnaire
        notifications_data = [notif.to_dict() for notif in notifications]
        
        return jsonify({
            'notifications': notifications_data,
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des notifications: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/<notification_id>', methods=['GET'])
@jwt_required
def get_notification(notification_id):
    """Récupère une notification spécifique."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        return jsonify(notification.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la notification: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/<notification_id>/mark-opened', methods=['POST'])
@jwt_required
def mark_notification_opened(notification_id):
    """Marque une notification comme ouverte."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.mark_as_opened()
        
        return jsonify({
            'message': 'Notification marquée comme ouverte',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors du marquage de la notification: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/<notification_id>/mark-acted', methods=['POST'])
@jwt_required
def mark_notification_acted_upon(notification_id):
    """Marque une notification comme ayant déclenché une action."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        if not data or 'action' not in data:
            return jsonify({'error': 'Action requise'}), 400
        
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.mark_as_acted_upon(data['action'])
        
        return jsonify({
            'message': 'Action enregistrée',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de l'action: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/<notification_id>/dismiss', methods=['POST'])
@jwt_required
def dismiss_notification(notification_id):
    """Marque une notification comme ignorée."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.status = NotificationStatus.DISMISSED
        notification.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Notification ignorée',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ignorance de la notification: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/<notification_id>/cancel', methods=['POST'])
@jwt_required
def cancel_notification(notification_id):
    """Annule une notification programmée."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        if notification.status not in [NotificationStatus.SCHEDULED]:
            return jsonify({'error': 'Notification ne peut pas être annulée'}), 400
        
        notification.cancel()
        
        return jsonify({
            'message': 'Notification annulée',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de l'annulation de la notification: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/preferences', methods=['GET'])
@jwt_required
def get_notification_preferences():
    """Récupère les préférences de notifications de l'utilisateur."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        preferences = NotificationPreferences.query.filter_by(
            user_id=user.id
        ).all()
        
        # Créer des préférences par défaut si elles n'existent pas
        if not preferences:
            preferences = notification_service.create_default_preferences(user.id)
        
        preferences_data = [pref.to_dict() for pref in preferences]
        
        return jsonify({
            'preferences': preferences_data
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des préférences: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/preferences', methods=['PUT'])
@jwt_required
def update_notification_preferences():
    """Met à jour les préférences de notifications de l'utilisateur."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        if not data or 'preferences' not in data:
            return jsonify({'error': 'Préférences requises'}), 400
        
        updated_preferences = []
        
        for pref_data in data['preferences']:
            # Validation des données
            if 'notification_type' not in pref_data:
                continue
            
            try:
                notification_type = NotificationType(pref_data['notification_type'])
            except ValueError:
                continue
            
            # Recherche ou création de la préférence
            preference = NotificationPreferences.query.filter_by(
                user_id=user.id,
                notification_type=notification_type
            ).first()
            
            if not preference:
                preference = NotificationPreferences(
                    user_id=user.id,
                    notification_type=notification_type
                )
                db.session.add(preference)
            
            # Mise à jour des champs
            preference.enabled = pref_data.get('enabled', preference.enabled)
            preference.preferred_channels = pref_data.get('preferred_channels', preference.preferred_channels)
            preference.preferred_hour = pref_data.get('preferred_hour', preference.preferred_hour)
            preference.frequency = pref_data.get('frequency', preference.frequency)
            
            if 'quiet_hours_start' in pref_data and pref_data['quiet_hours_start']:
                preference.quiet_hours_start = datetime.strptime(
                    pref_data['quiet_hours_start'], '%H:%M'
                ).time()
            
            if 'quiet_hours_end' in pref_data and pref_data['quiet_hours_end']:
                preference.quiet_hours_end = datetime.strptime(
                    pref_data['quiet_hours_end'], '%H:%M'
                ).time()
            
            preference.settings = pref_data.get('settings', preference.settings)
            preference.updated_at = datetime.utcnow()
            
            updated_preferences.append(preference)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Préférences mises à jour',
            'preferences': [pref.to_dict() for pref in updated_preferences]
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des préférences: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/schedule', methods=['POST'])
@jwt_required
def schedule_notification():
    """Programme une nouvelle notification."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['type', 'title', 'content', 'scheduled_for']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis: {field}'}), 400
        
        try:
            notification_type = NotificationType(data['type'])
        except ValueError:
            return jsonify({'error': 'Type de notification invalide'}), 400
        
        try:
            scheduled_for = datetime.fromisoformat(data['scheduled_for'])
        except ValueError:
            return jsonify({'error': 'Format de date invalide'}), 400
        
        # Création de la notification
        notification = Notification(
            user_id=user.id,
            type=notification_type,
            title=data['title'],
            content=data['content'],
            scheduled_for=scheduled_for,
            priority=data.get('priority', 5),
            channels=data.get('channels', ['push']),
            data=data.get('metadata', {})
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Programmation avec le scheduler
        notification_scheduler.schedule_notification(notification)
        
        return jsonify({
            'message': 'Notification programmée',
            'notification': notification.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Erreur lors de la programmation de la notification: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/analytics', methods=['GET'])
@jwt_required
def get_notification_analytics():
    """Récupère les analytics des notifications de l'utilisateur."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Période d'analyse (par défaut 30 jours)
        period_days = int(request.args.get('period_days', 30))
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Requête pour les notifications de la période
        notifications = Notification.query.filter(
            Notification.user_id == user.id,
            Notification.created_at >= start_date
        ).all()
        
        # Calcul des métriques
        total_notifications = len(notifications)
        
        if total_notifications == 0:
            return jsonify({
                'total_notifications': 0,
                'analytics': {}
            }), 200
        
        # Métriques par statut
        status_counts = {}
        for status in NotificationStatus:
            status_counts[status.value] = len([n for n in notifications if n.status == status])
        
        # Métriques par type
        type_counts = {}
        for type_enum in NotificationType:
            type_counts[type_enum.value] = len([n for n in notifications if n.type == type_enum])
        
        # Taux d'engagement
        opened_count = status_counts.get('opened', 0) + status_counts.get('acted_upon', 0)
        acted_upon_count = status_counts.get('acted_upon', 0)
        
        open_rate = (opened_count / total_notifications) * 100 if total_notifications > 0 else 0
        action_rate = (acted_upon_count / total_notifications) * 100 if total_notifications > 0 else 0
        
        # Répartition par canal
        channel_stats = {}
        for notification in notifications:
            for channel in notification.channels:
                if channel not in channel_stats:
                    channel_stats[channel] = 0
                channel_stats[channel] += 1
        
        analytics = {
            'total_notifications': total_notifications,
            'period_days': period_days,
            'status_breakdown': status_counts,
            'type_breakdown': type_counts,
            'engagement_metrics': {
                'open_rate': round(open_rate, 2),
                'action_rate': round(action_rate, 2)
            },
            'channel_distribution': channel_stats
        }
        
        return jsonify({'analytics': analytics}), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des analytics: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/test', methods=['POST'])
@jwt_required
def send_test_notification():
    """Envoie une notification de test."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        # Notification de test
        test_notification = Notification(
            user_id=user.id,
            type=NotificationType.PLANT_CARE_GUIDE,
            title=data.get('title', 'Test de notification'),
            content=data.get('content', 'Ceci est une notification de test.'),
            scheduled_for=datetime.utcnow(),
            priority=5,
            channels=data.get('channels', ['push']),
            data={'test': True}
        )
        
        db.session.add(test_notification)
        db.session.commit()
        
        # Envoi immédiat
        notification_service.send_notification(test_notification)
        
        return jsonify({
            'message': 'Notification de test envoyée',
            'notification': test_notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de la notification de test: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500


@notifications_bp.route('/notifications/delivery-logs/<notification_id>', methods=['GET'])
@jwt_required
def get_delivery_logs(notification_id):
    """Récupère les logs de livraison d'une notification."""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Vérifier que la notification appartient à l'utilisateur
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=user.id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        # Récupérer les logs de livraison
        delivery_logs = NotificationDeliveryLog.query.filter_by(
            notification_id=notification_id
        ).all()
        
        logs_data = [log.to_dict() for log in delivery_logs]
        
        return jsonify({
            'notification_id': notification_id,
            'delivery_logs': logs_data
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des logs: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500
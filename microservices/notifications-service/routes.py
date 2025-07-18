"""
Notifications Service Routes
"""
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import datetime
import logging
import requests
from models import (
    db, Notification, NotificationPreferences, NotificationTemplate,
    NotificationDeliveryLog, NotificationType, NotificationStatus,
    NotificationChannel
)
from services import NotificationService

logger = logging.getLogger(__name__)

notifications_bp = Blueprint('notifications', __name__)
notification_service = NotificationService()

def auth_required(f):
    """Decorator to verify JWT token with auth service"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        
        try:
            # Verify token with auth service
            auth_service_url = current_app.config.get('AUTH_SERVICE_URL')
            response = requests.post(
                f'{auth_service_url}/auth/verify',
                json={'token': token},
                timeout=5
            )
            
            if response.status_code != 200:
                return jsonify({'error': 'Token invalide'}), 401
            
            user_data = response.json()
            return f(user_data, *args, **kwargs)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Auth service unavailable: {e}")
            return jsonify({'error': 'Service d\'authentification indisponible'}), 503
        except Exception as e:
            logger.error(f"Auth verification error: {e}")
            return jsonify({'error': 'Erreur d\'authentification'}), 500
    
    return decorated

@notifications_bp.route('/notifications', methods=['GET'])
@auth_required
def get_user_notifications(user_data):
    """Get user's notifications"""
    try:
        user_id = user_data.get('user_id')
        
        # Query parameters
        status = request.args.get('status')
        notification_type = request.args.get('type')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Build query
        query = Notification.query.filter_by(user_id=user_id)
        
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
        
        # Sort and paginate
        query = query.order_by(Notification.created_at.desc())
        notifications = query.offset(offset).limit(limit).all()
        
        return jsonify({
            'notifications': [notif.to_dict() for notif in notifications],
            'total': query.count(),
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/<notification_id>', methods=['GET'])
@auth_required
def get_notification(user_data, notification_id):
    """Get a specific notification"""
    try:
        user_id = user_data.get('user_id')
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        return jsonify(notification.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting notification: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/<notification_id>/mark-opened', methods=['POST'])
@auth_required
def mark_notification_opened(user_data, notification_id):
    """Mark notification as opened"""
    try:
        user_id = user_data.get('user_id')
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.mark_as_opened()
        
        return jsonify({
            'message': 'Notification marquée comme ouverte',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error marking notification as opened: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/<notification_id>/mark-acted', methods=['POST'])
@auth_required
def mark_notification_acted_upon(user_data, notification_id):
    """Mark notification as acted upon"""
    try:
        user_id = user_data.get('user_id')
        data = request.get_json()
        
        if not data or 'action' not in data:
            return jsonify({'error': 'Action requise'}), 400
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.mark_as_acted_upon(data['action'])
        
        return jsonify({
            'message': 'Action enregistrée',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error marking notification as acted upon: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/<notification_id>/dismiss', methods=['POST'])
@auth_required
def dismiss_notification(user_data, notification_id):
    """Dismiss a notification"""
    try:
        user_id = user_data.get('user_id')
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        notification.status = NotificationStatus.DISMISSED
        notification.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Notification ignorée',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error dismissing notification: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/<notification_id>/cancel', methods=['POST'])
@auth_required
def cancel_notification(user_data, notification_id):
    """Cancel a scheduled notification"""
    try:
        user_id = user_data.get('user_id')
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
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
        logger.error(f"Error canceling notification: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/preferences', methods=['GET'])
@auth_required
def get_notification_preferences(user_data):
    """Get user's notification preferences"""
    try:
        user_id = user_data.get('user_id')
        
        preferences = NotificationPreferences.query.filter_by(user_id=user_id).all()
        
        # Create default preferences if none exist
        if not preferences:
            preferences = notification_service.create_default_preferences(user_id)
        
        return jsonify({
            'preferences': [pref.to_dict() for pref in preferences]
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting preferences: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/preferences', methods=['PUT'])
@auth_required
def update_notification_preferences(user_data):
    """Update user's notification preferences"""
    try:
        user_id = user_data.get('user_id')
        data = request.get_json()
        
        if not data or 'preferences' not in data:
            return jsonify({'error': 'Préférences requises'}), 400
        
        updated_preferences = []
        
        for pref_data in data['preferences']:
            if 'notification_type' not in pref_data:
                continue
            
            try:
                notification_type = NotificationType(pref_data['notification_type'])
            except ValueError:
                continue
            
            # Find or create preference
            preference = NotificationPreferences.query.filter_by(
                user_id=user_id,
                notification_type=notification_type
            ).first()
            
            if not preference:
                preference = NotificationPreferences(
                    user_id=user_id,
                    notification_type=notification_type
                )
                db.session.add(preference)
            
            # Update fields
            preference.enabled = pref_data.get('enabled', preference.enabled)
            preference.preferred_channels = pref_data.get('preferred_channels', preference.preferred_channels)
            preference.preferred_hour = pref_data.get('preferred_hour', preference.preferred_hour)
            preference.frequency = pref_data.get('frequency', preference.frequency)
            
            if 'quiet_hours_start' in pref_data and pref_data['quiet_hours_start']:
                preference.quiet_hours_start = datetime.datetime.strptime(
                    pref_data['quiet_hours_start'], '%H:%M'
                ).time()
            
            if 'quiet_hours_end' in pref_data and pref_data['quiet_hours_end']:
                preference.quiet_hours_end = datetime.datetime.strptime(
                    pref_data['quiet_hours_end'], '%H:%M'
                ).time()
            
            preference.settings = pref_data.get('settings', preference.settings)
            preference.updated_at = datetime.datetime.utcnow()
            
            updated_preferences.append(preference)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Préférences mises à jour',
            'preferences': [pref.to_dict() for pref in updated_preferences]
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/schedule', methods=['POST'])
@auth_required
def schedule_notification(user_data):
    """Schedule a new notification"""
    try:
        user_id = user_data.get('user_id')
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['type', 'title', 'content', 'scheduled_for']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis: {field}'}), 400
        
        try:
            notification_type = NotificationType(data['type'])
        except ValueError:
            return jsonify({'error': 'Type de notification invalide'}), 400
        
        try:
            scheduled_for = datetime.datetime.fromisoformat(data['scheduled_for'])
        except ValueError:
            return jsonify({'error': 'Format de date invalide'}), 400
        
        # Create notification
        notification = Notification(
            user_id=user_id,
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
        
        # Schedule with background task
        notification_service.schedule_notification(notification)
        
        return jsonify({
            'message': 'Notification programmée',
            'notification': notification.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error scheduling notification: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/test', methods=['POST'])
@auth_required
def send_test_notification(user_data):
    """Send a test notification"""
    try:
        user_id = user_data.get('user_id')
        data = request.get_json()
        
        # Create test notification
        test_notification = Notification(
            user_id=user_id,
            type=NotificationType.SYSTEM_NOTIFICATION,
            title=data.get('title', 'Test de notification'),
            content=data.get('content', 'Ceci est une notification de test.'),
            scheduled_for=datetime.datetime.utcnow(),
            priority=5,
            channels=data.get('channels', ['push']),
            data={'test': True}
        )
        
        db.session.add(test_notification)
        db.session.commit()
        
        # Send immediately
        notification_service.send_notification(test_notification)
        
        return jsonify({
            'message': 'Notification de test envoyée',
            'notification': test_notification.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/analytics', methods=['GET'])
@auth_required
def get_notification_analytics(user_data):
    """Get user's notification analytics"""
    try:
        user_id = user_data.get('user_id')
        
        # Analysis period (default 30 days)
        period_days = int(request.args.get('period_days', 30))
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=period_days)
        
        # Get notifications for period
        notifications = Notification.query.filter(
            Notification.user_id == user_id,
            Notification.created_at >= start_date
        ).all()
        
        # Calculate metrics
        total_notifications = len(notifications)
        
        if total_notifications == 0:
            return jsonify({
                'total_notifications': 0,
                'analytics': {}
            }), 200
        
        # Status counts
        status_counts = {}
        for status in NotificationStatus:
            status_counts[status.value] = len([n for n in notifications if n.status == status])
        
        # Type counts
        type_counts = {}
        for type_enum in NotificationType:
            type_counts[type_enum.value] = len([n for n in notifications if n.type == type_enum])
        
        # Engagement rates
        opened_count = status_counts.get('opened', 0) + status_counts.get('acted_upon', 0)
        acted_upon_count = status_counts.get('acted_upon', 0)
        
        open_rate = (opened_count / total_notifications) * 100 if total_notifications > 0 else 0
        action_rate = (acted_upon_count / total_notifications) * 100 if total_notifications > 0 else 0
        
        # Channel distribution
        channel_stats = {}
        for notification in notifications:
            for channel in notification.get_channels():
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
        logger.error(f"Error getting analytics: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@notifications_bp.route('/notifications/delivery-logs/<notification_id>', methods=['GET'])
@auth_required
def get_delivery_logs(user_data, notification_id):
    """Get delivery logs for a notification"""
    try:
        user_id = user_data.get('user_id')
        
        # Verify notification ownership
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification non trouvée'}), 404
        
        # Get delivery logs
        delivery_logs = NotificationDeliveryLog.query.filter_by(
            notification_id=notification_id
        ).all()
        
        return jsonify({
            'notification_id': notification_id,
            'delivery_logs': [log.to_dict() for log in delivery_logs]
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting delivery logs: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

# Internal API endpoints for other services
@notifications_bp.route('/internal/notifications/schedule-watering-reminder', methods=['POST'])
def schedule_watering_reminder():
    """Internal endpoint to schedule watering reminders"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'plant_name', 'scheduled_for']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis: {field}'}), 400
        
        try:
            scheduled_for = datetime.datetime.fromisoformat(data['scheduled_for'])
        except ValueError:
            return jsonify({'error': 'Format de date invalide'}), 400
        
        # Create watering reminder
        notification = Notification(
            user_id=data['user_id'],
            type=NotificationType.WATERING_REMINDER,
            title=f"Arrosage de {data['plant_name']}",
            content=f"Il est temps d'arroser votre {data['plant_name']}!",
            scheduled_for=scheduled_for,
            priority=7,
            channels=['push'],
            data={
                'plant_id': data.get('plant_id'),
                'plant_name': data['plant_name'],
                'user_plant_id': data.get('user_plant_id')
            }
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Schedule with background task
        notification_service.schedule_notification(notification)
        
        return jsonify({
            'message': 'Rappel d\'arrosage programmé',
            'notification': notification.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error scheduling watering reminder: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500
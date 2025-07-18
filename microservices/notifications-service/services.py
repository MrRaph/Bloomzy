"""
Notification Service Business Logic
"""
from datetime import datetime, timedelta
import logging
from models import (
    db, Notification, NotificationPreferences, NotificationTemplate,
    NotificationDeliveryLog, NotificationType, NotificationStatus,
    NotificationChannel
)
from celery import current_app as celery_app

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing notifications"""
    
    def create_default_preferences(self, user_id):
        """Create default notification preferences for a user"""
        default_preferences = []
        
        # Default preferences for each notification type
        default_settings = {
            NotificationType.WATERING_REMINDER: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 9,
                'frequency': 'daily'
            },
            NotificationType.FERTILIZING_REMINDER: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 10,
                'frequency': 'monthly'
            },
            NotificationType.REPOTTING_REMINDER: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 11,
                'frequency': 'yearly'
            },
            NotificationType.PLANT_CARE_GUIDE: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 12,
                'frequency': 'weekly'
            },
            NotificationType.HEALTH_CHECK: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 13,
                'frequency': 'weekly'
            },
            NotificationType.GROWTH_MILESTONE: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 14,
                'frequency': 'monthly'
            },
            NotificationType.WEATHER_ALERT: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 8,
                'frequency': 'daily'
            },
            NotificationType.SYSTEM_NOTIFICATION: {
                'enabled': True,
                'preferred_channels': ['push'],
                'preferred_hour': 15,
                'frequency': 'immediate'
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
            db.session.add(preference)
            default_preferences.append(preference)
        
        db.session.commit()
        return default_preferences
    
    def schedule_notification(self, notification):
        """Schedule a notification for delivery"""
        try:
            # Schedule with Celery
            from tasks import send_notification_task
            
            # Calculate delay until scheduled time
            delay = (notification.scheduled_for - datetime.utcnow()).total_seconds()
            
            if delay <= 0:
                # Send immediately if scheduled time has passed
                send_notification_task.delay(notification.id)
            else:
                # Schedule for later
                send_notification_task.apply_async(
                    args=[notification.id],
                    countdown=delay
                )
            
            logger.info(f"Notification scheduled: {notification.id}")
            
        except Exception as e:
            logger.error(f"Error scheduling notification: {e}")
            notification.status = NotificationStatus.FAILED
            db.session.commit()
    
    def send_notification(self, notification):
        """Send a notification through configured channels"""
        try:
            # Get user preferences
            preferences = NotificationPreferences.query.filter_by(
                user_id=notification.user_id,
                notification_type=notification.type
            ).first()
            
            # Determine channels to use
            channels = notification.get_channels()
            if preferences and preferences.enabled:
                # Use user's preferred channels if available
                preferred_channels = preferences.get_preferred_channels()
                if preferred_channels:
                    channels = preferred_channels
            
            # Send through each channel
            delivery_success = False
            for channel in channels:
                try:
                    success = self._send_through_channel(notification, channel)
                    if success:
                        delivery_success = True
                except Exception as e:
                    logger.error(f"Error sending through channel {channel}: {e}")
                    self._log_delivery_failure(notification, channel, str(e))
            
            # Update notification status
            if delivery_success:
                notification.mark_as_sent()
                logger.info(f"Notification sent successfully: {notification.id}")
            else:
                notification.status = NotificationStatus.FAILED
                db.session.commit()
                logger.error(f"Failed to send notification: {notification.id}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            notification.status = NotificationStatus.FAILED
            db.session.commit()
    
    def _send_through_channel(self, notification, channel):
        """Send notification through a specific channel"""
        try:
            if channel == 'push':
                return self._send_push_notification(notification)
            elif channel == 'email':
                return self._send_email_notification(notification)
            elif channel == 'sms':
                return self._send_sms_notification(notification)
            elif channel == 'in_app':
                return self._send_in_app_notification(notification)
            else:
                logger.warning(f"Unknown channel: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending through channel {channel}: {e}")
            return False
    
    def _send_push_notification(self, notification):
        """Send push notification (placeholder implementation)"""
        try:
            # This would integrate with Firebase Cloud Messaging, OneSignal, etc.
            # For now, we'll just log it
            logger.info(f"Push notification sent: {notification.title}")
            
            self._log_delivery_success(notification, 'push', 'mock_provider')
            return True
            
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
            self._log_delivery_failure(notification, 'push', str(e))
            return False
    
    def _send_email_notification(self, notification):
        """Send email notification (placeholder implementation)"""
        try:
            # This would integrate with SendGrid, Mailgun, etc.
            # For now, we'll just log it
            logger.info(f"Email notification sent: {notification.title}")
            
            self._log_delivery_success(notification, 'email', 'mock_provider')
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            self._log_delivery_failure(notification, 'email', str(e))
            return False
    
    def _send_sms_notification(self, notification):
        """Send SMS notification (placeholder implementation)"""
        try:
            # This would integrate with Twilio, Nexmo, etc.
            # For now, we'll just log it
            logger.info(f"SMS notification sent: {notification.title}")
            
            self._log_delivery_success(notification, 'sms', 'mock_provider')
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS notification: {e}")
            self._log_delivery_failure(notification, 'sms', str(e))
            return False
    
    def _send_in_app_notification(self, notification):
        """Send in-app notification (placeholder implementation)"""
        try:
            # This would use WebSocket connections to send real-time notifications
            # For now, we'll just log it
            logger.info(f"In-app notification sent: {notification.title}")
            
            self._log_delivery_success(notification, 'in_app', 'websocket')
            return True
            
        except Exception as e:
            logger.error(f"Error sending in-app notification: {e}")
            self._log_delivery_failure(notification, 'in_app', str(e))
            return False
    
    def _log_delivery_success(self, notification, channel, provider):
        """Log successful delivery"""
        try:
            log = NotificationDeliveryLog(
                notification_id=notification.id,
                channel=NotificationChannel(channel),
                status='success',
                provider=provider,
                metadata={'sent_at': datetime.utcnow().isoformat()}
            )
            db.session.add(log)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error logging delivery success: {e}")
    
    def _log_delivery_failure(self, notification, channel, error_message):
        """Log delivery failure"""
        try:
            log = NotificationDeliveryLog(
                notification_id=notification.id,
                channel=NotificationChannel(channel),
                status='failed',
                error_message=error_message,
                metadata={'failed_at': datetime.utcnow().isoformat()}
            )
            db.session.add(log)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error logging delivery failure: {e}")
    
    def get_due_notifications(self):
        """Get notifications that are due to be sent"""
        try:
            now = datetime.utcnow()
            due_notifications = Notification.query.filter(
                Notification.status == NotificationStatus.SCHEDULED,
                Notification.scheduled_for <= now
            ).all()
            
            return due_notifications
            
        except Exception as e:
            logger.error(f"Error getting due notifications: {e}")
            return []
    
    def process_due_notifications(self):
        """Process all due notifications"""
        try:
            due_notifications = self.get_due_notifications()
            
            for notification in due_notifications:
                self.send_notification(notification)
            
            logger.info(f"Processed {len(due_notifications)} due notifications")
            
        except Exception as e:
            logger.error(f"Error processing due notifications: {e}")
    
    def cleanup_old_notifications(self, days_old=30):
        """Clean up old notifications"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
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
            
            db.session.commit()
            
            logger.info(f"Cleaned up {len(old_notifications)} old notifications")
            
        except Exception as e:
            logger.error(f"Error cleaning up old notifications: {e}")
    
    def get_notification_stats(self):
        """Get notification statistics"""
        try:
            stats = {
                'total': Notification.query.count(),
                'scheduled': Notification.query.filter_by(status=NotificationStatus.SCHEDULED).count(),
                'sent': Notification.query.filter_by(status=NotificationStatus.SENT).count(),
                'delivered': Notification.query.filter_by(status=NotificationStatus.DELIVERED).count(),
                'opened': Notification.query.filter_by(status=NotificationStatus.OPENED).count(),
                'acted_upon': Notification.query.filter_by(status=NotificationStatus.ACTED_UPON).count(),
                'failed': Notification.query.filter_by(status=NotificationStatus.FAILED).count()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {e}")
            return {}
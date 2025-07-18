"""
Celery Tasks for Notifications Service
"""
from celery import Celery
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def make_celery():
    """Create Celery instance"""
    celery = Celery('notifications-service')
    celery.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        beat_schedule={
            'process-due-notifications': {
                'task': 'tasks.process_due_notifications',
                'schedule': 60.0,  # Every minute
            },
            'cleanup-old-notifications': {
                'task': 'tasks.cleanup_old_notifications',
                'schedule': timedelta(hours=24),  # Daily
            },
        },
    )
    return celery

celery = make_celery()

@celery.task
def send_notification_task(notification_id):
    """Send a notification"""
    try:
        from app import create_app
        from models import Notification
        from services import NotificationService
        
        app = create_app()
        
        with app.app_context():
            notification = Notification.query.get(notification_id)
            if not notification:
                logger.error(f"Notification not found: {notification_id}")
                return False
            
            service = NotificationService()
            service.send_notification(notification)
            
            return True
            
    except Exception as e:
        logger.error(f"Error in send_notification_task: {e}")
        return False

@celery.task
def process_due_notifications():
    """Process all due notifications"""
    try:
        from app import create_app
        from services import NotificationService
        
        app = create_app()
        
        with app.app_context():
            service = NotificationService()
            service.process_due_notifications()
            
        return True
        
    except Exception as e:
        logger.error(f"Error in process_due_notifications: {e}")
        return False

@celery.task
def cleanup_old_notifications():
    """Clean up old notifications"""
    try:
        from app import create_app
        from services import NotificationService
        
        app = create_app()
        
        with app.app_context():
            service = NotificationService()
            service.cleanup_old_notifications()
            
        return True
        
    except Exception as e:
        logger.error(f"Error in cleanup_old_notifications: {e}")
        return False

@celery.task
def schedule_watering_reminders():
    """Schedule watering reminders based on plant schedules"""
    try:
        from app import create_app
        from models import Notification, NotificationType
        import requests
        
        app = create_app()
        
        with app.app_context():
            # Get plants that need watering reminders
            plants_service_url = app.config.get('PLANTS_SERVICE_URL')
            
            # This would typically fetch from plants service
            # For now, it's a placeholder
            
            logger.info("Watering reminders scheduled")
            return True
            
    except Exception as e:
        logger.error(f"Error in schedule_watering_reminders: {e}")
        return False
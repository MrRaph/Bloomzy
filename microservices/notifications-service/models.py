"""
Notifications Service Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import uuid
import json

db = SQLAlchemy()

class NotificationStatus(Enum):
    SCHEDULED = "scheduled"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    ACTED_UPON = "acted_upon"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DISMISSED = "dismissed"

class NotificationType(Enum):
    WATERING_REMINDER = "watering_reminder"
    FERTILIZING_REMINDER = "fertilizing_reminder"
    REPOTTING_REMINDER = "repotting_reminder"
    PLANT_CARE_GUIDE = "plant_care_guide"
    HEALTH_CHECK = "health_check"
    GROWTH_MILESTONE = "growth_milestone"
    WEATHER_ALERT = "weather_alert"
    SYSTEM_NOTIFICATION = "system_notification"
    COMMUNITY_UPDATE = "community_update"
    SEASONAL_ADVICE = "seasonal_advice"

class NotificationChannel(Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    SLACK = "slack"
    DISCORD = "discord"

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)  # Reference to user in auth service
    type = db.Column(db.Enum(NotificationType), nullable=False)
    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.SCHEDULED)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    opened_at = db.Column(db.DateTime, nullable=True)
    acted_upon_at = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, default=5)  # 1-10 scale
    channels = db.Column(db.Text, nullable=True)  # JSON array of channels
    data = db.Column(db.Text, nullable=True)  # JSON metadata
    action_taken = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.channels and isinstance(self.channels, list):
            self.channels = json.dumps(self.channels)
        if self.data and isinstance(self.data, dict):
            self.data = json.dumps(self.data)
    
    def get_channels(self):
        """Get channels as a list"""
        if self.channels:
            return json.loads(self.channels)
        return []
    
    def get_data(self):
        """Get data as a dict"""
        if self.data:
            return json.loads(self.data)
        return {}
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_delivered(self):
        """Mark notification as delivered"""
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_opened(self):
        """Mark notification as opened"""
        if self.status in [NotificationStatus.SENT, NotificationStatus.DELIVERED]:
            self.status = NotificationStatus.OPENED
            self.opened_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def mark_as_acted_upon(self, action):
        """Mark notification as acted upon"""
        self.status = NotificationStatus.ACTED_UPON
        self.acted_upon_at = datetime.utcnow()
        self.action_taken = action
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel(self):
        """Cancel a scheduled notification"""
        if self.status == NotificationStatus.SCHEDULED:
            self.status = NotificationStatus.CANCELLED
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type.value,
            'status': self.status.value,
            'title': self.title,
            'content': self.content,
            'scheduled_for': self.scheduled_for.isoformat() if self.scheduled_for else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'acted_upon_at': self.acted_upon_at.isoformat() if self.acted_upon_at else None,
            'priority': self.priority,
            'channels': self.get_channels(),
            'data': self.get_data(),
            'action_taken': self.action_taken,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationPreferences(db.Model):
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)
    notification_type = db.Column(db.Enum(NotificationType), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    preferred_channels = db.Column(db.Text, nullable=True)  # JSON array
    preferred_hour = db.Column(db.Integer, default=9)  # Hour of day (0-23)
    frequency = db.Column(db.String(20), default='daily')  # daily, weekly, monthly
    quiet_hours_start = db.Column(db.Time, nullable=True)
    quiet_hours_end = db.Column(db.Time, nullable=True)
    settings = db.Column(db.Text, nullable=True)  # JSON for additional settings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.preferred_channels and isinstance(self.preferred_channels, list):
            self.preferred_channels = json.dumps(self.preferred_channels)
        if self.settings and isinstance(self.settings, dict):
            self.settings = json.dumps(self.settings)
    
    def get_preferred_channels(self):
        """Get preferred channels as a list"""
        if self.preferred_channels:
            return json.loads(self.preferred_channels)
        return ['push']
    
    def get_settings(self):
        """Get settings as a dict"""
        if self.settings:
            return json.loads(self.settings)
        return {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type.value,
            'enabled': self.enabled,
            'preferred_channels': self.get_preferred_channels(),
            'preferred_hour': self.preferred_hour,
            'frequency': self.frequency,
            'quiet_hours_start': self.quiet_hours_start.strftime('%H:%M') if self.quiet_hours_start else None,
            'quiet_hours_end': self.quiet_hours_end.strftime('%H:%M') if self.quiet_hours_end else None,
            'settings': self.get_settings(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationTemplate(db.Model):
    __tablename__ = 'notification_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    title_template = db.Column(db.String(255), nullable=False)
    content_template = db.Column(db.Text, nullable=False)
    channels = db.Column(db.Text, nullable=True)  # JSON array
    priority = db.Column(db.Integer, default=5)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.channels and isinstance(self.channels, list):
            self.channels = json.dumps(self.channels)
    
    def get_channels(self):
        """Get channels as a list"""
        if self.channels:
            return json.loads(self.channels)
        return ['push']
    
    def render(self, **kwargs):
        """Render template with provided data"""
        title = self.title_template.format(**kwargs)
        content = self.content_template.format(**kwargs)
        return title, content
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'title_template': self.title_template,
            'content_template': self.content_template,
            'channels': self.get_channels(),
            'priority': self.priority,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationDeliveryLog(db.Model):
    __tablename__ = 'notification_delivery_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id = db.Column(db.String(36), db.ForeignKey('notifications.id'), nullable=False)
    channel = db.Column(db.Enum(NotificationChannel), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, failed, pending
    provider = db.Column(db.String(50), nullable=True)  # Provider used (Firebase, SendGrid, etc.)
    external_id = db.Column(db.String(255), nullable=True)  # Provider's message ID
    error_message = db.Column(db.Text, nullable=True)
    metadata = db.Column(db.Text, nullable=True)  # JSON metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    notification = db.relationship('Notification', backref='delivery_logs')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.metadata and isinstance(self.metadata, dict):
            self.metadata = json.dumps(self.metadata)
    
    def get_metadata(self):
        """Get metadata as a dict"""
        if self.metadata:
            return json.loads(self.metadata)
        return {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'notification_id': self.notification_id,
            'channel': self.channel.value,
            'status': self.status,
            'provider': self.provider,
            'external_id': self.external_id,
            'error_message': self.error_message,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
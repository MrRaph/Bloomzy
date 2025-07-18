"""
Modèle de notification pour le système de notifications intelligent.
"""
from models.user import db
from datetime import datetime
from enum import Enum
import json


class NotificationType(Enum):
    WATERING = "watering"
    HARVEST = "harvest"
    PLANTING = "planting"
    MAINTENANCE = "maintenance"
    WEATHER_ALERT = "weather_alert"
    PLANT_CARE_GUIDE = "plant_care_guide"


class NotificationStatus(Enum):
    SCHEDULED = "scheduled"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    ACTED_UPON = "acted_upon"
    DISMISSED = "dismissed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationChannel(Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    WEB = "web"


class Notification(db.Model):
    """
    Modèle principal pour les notifications.
    
    Ce modèle stocke toutes les notifications du système avec leur statut,
    contenu et métadonnées associées.
    """
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Scheduling
    scheduled_for = db.Column(db.DateTime, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    opened_at = db.Column(db.DateTime, nullable=True)
    
    # Status et priorité
    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.SCHEDULED)
    priority = db.Column(db.Integer, default=5)  # 1-10, 10 étant le plus prioritaire
    
    # Canaux de livraison
    channels = db.Column(db.JSON, default=list)  # Liste des canaux (push, email, sms)
    
    # Métadonnées flexibles
    data = db.Column(db.JSON, default=dict)
    
    # Interaction utilisateur
    user_action = db.Column(db.String(50), nullable=True)
    action_taken_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f"<Notification {self.id}: {self.title}>"
    
    def to_dict(self):
        """Convertit la notification en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type.value,
            'title': self.title,
            'content': self.content,
            'scheduled_for': self.scheduled_for.isoformat() if self.scheduled_for else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'status': self.status.value,
            'priority': self.priority,
            'channels': self.channels,
            'metadata': self.data,
            'user_action': self.user_action,
            'action_taken_at': self.action_taken_at.isoformat() if self.action_taken_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def mark_as_sent(self):
        """Marque la notification comme envoyée."""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_delivered(self):
        """Marque la notification comme livrée."""
        self.status = NotificationStatus.DELIVERED
        self.delivered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_opened(self):
        """Marque la notification comme ouverte."""
        self.status = NotificationStatus.OPENED
        self.opened_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_acted_upon(self, action):
        """Marque la notification comme ayant déclenché une action."""
        self.status = NotificationStatus.ACTED_UPON
        self.user_action = action
        self.action_taken_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel(self):
        """Annule la notification."""
        self.status = NotificationStatus.CANCELLED
        self.updated_at = datetime.utcnow()
        db.session.commit()


class NotificationPreferences(db.Model):
    """
    Modèle pour les préférences de notifications utilisateur.
    
    Ce modèle stocke les préférences personnalisées de chaque utilisateur
    pour différents types de notifications.
    """
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_type = db.Column(db.Enum(NotificationType), nullable=False)
    
    # Activation
    enabled = db.Column(db.Boolean, default=True)
    
    # Canaux préférés
    preferred_channels = db.Column(db.JSON, default=list)
    
    # Timing
    preferred_hour = db.Column(db.Integer, default=9)  # Heure préférée (0-23)
    frequency = db.Column(db.String(20), default='normal')  # normal, reduced, minimal
    
    # Heures de silence
    quiet_hours_start = db.Column(db.Time, nullable=True)
    quiet_hours_end = db.Column(db.Time, nullable=True)
    
    # Métadonnées additionnelles
    settings = db.Column(db.JSON, default=dict)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='notification_preferences')
    
    def __repr__(self):
        return f"<NotificationPreferences {self.user_id}:{self.notification_type.value}>"
    
    def to_dict(self):
        """Convertit les préférences en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type.value,
            'enabled': self.enabled,
            'preferred_channels': self.preferred_channels,
            'preferred_hour': self.preferred_hour,
            'frequency': self.frequency,
            'quiet_hours_start': self.quiet_hours_start.isoformat() if self.quiet_hours_start else None,
            'quiet_hours_end': self.quiet_hours_end.isoformat() if self.quiet_hours_end else None,
            'settings': self.settings,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class NotificationTemplate(db.Model):
    """
    Modèle pour les templates de notifications.
    
    Ce modèle stocke les templates réutilisables pour différents types
    de notifications avec support de la localisation.
    """
    __tablename__ = 'notification_templates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.Enum(NotificationType), nullable=False)
    priority = db.Column(db.Integer, default=5)
    
    # Templates
    title_template = db.Column(db.Text, nullable=False)
    content_template = db.Column(db.Text, nullable=False)
    
    # Variables disponibles
    variables = db.Column(db.JSON, default=list)
    
    # Localisation
    localization = db.Column(db.String(10), default='fr')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<NotificationTemplate {self.type.value}:{self.localization}>"
    
    def to_dict(self):
        """Convertit le template en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'type': self.type.value,
            'priority': self.priority,
            'title_template': self.title_template,
            'content_template': self.content_template,
            'variables': self.variables,
            'localization': self.localization,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def render(self, variables_dict):
        """Rend le template avec les variables fournies."""
        title = self.title_template
        content = self.content_template
        
        for var_name, var_value in variables_dict.items():
            title = title.replace(f"{{{var_name}}}", str(var_value))
            content = content.replace(f"{{{var_name}}}", str(var_value))
        
        return title, content


class NotificationDeliveryLog(db.Model):
    """
    Modèle pour les logs de livraison de notifications.
    
    Ce modèle stocke les tentatives de livraison et leur statut
    pour le debugging et les métriques.
    """
    __tablename__ = 'notification_delivery_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id = db.Column(db.String(36), db.ForeignKey('notifications.id'), nullable=False)
    channel = db.Column(db.Enum(NotificationChannel), nullable=False)
    
    # Résultat de la livraison
    success = db.Column(db.Boolean, nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    
    # Métadonnées de livraison
    delivery_data = db.Column(db.JSON, default=dict)
    
    # Timestamps
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    notification = db.relationship('Notification', backref='delivery_logs')
    
    def __repr__(self):
        return f"<NotificationDeliveryLog {self.notification_id}:{self.channel.value}>"
    
    def to_dict(self):
        """Convertit le log en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'notification_id': self.notification_id,
            'channel': self.channel.value,
            'success': self.success,
            'error_message': self.error_message,
            'delivery_metadata': self.delivery_data,
            'attempted_at': self.attempted_at.isoformat()
        }


# Import nécessaire pour UUID
import uuid
"""
Plants Service Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import json

db = SQLAlchemy()

class IndoorPlant(db.Model):
    __tablename__ = 'indoor_plants'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scientific_name = db.Column(db.String(100), nullable=False, unique=True)
    common_names = db.Column(db.Text, nullable=True)
    family = db.Column(db.String(50), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    watering_frequency = db.Column(db.Integer, nullable=True)
    light = db.Column(db.String(50), nullable=True)
    humidity = db.Column(db.String(50), nullable=True)
    temperature = db.Column(db.String(50), nullable=True)
    soil_type = db.Column(db.String(50), nullable=True)
    adult_size = db.Column(db.String(50), nullable=True)
    growth_rate = db.Column(db.String(20), nullable=True)
    toxicity = db.Column(db.String(50), nullable=True)
    air_purification = db.Column(db.Boolean, default=False)
    flowering = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scientific_name': self.scientific_name,
            'common_names': self.common_names,
            'family': self.family,
            'origin': self.origin,
            'difficulty': self.difficulty,
            'watering_frequency': self.watering_frequency,
            'light': self.light,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'soil_type': self.soil_type,
            'adult_size': self.adult_size,
            'growth_rate': self.growth_rate,
            'toxicity': self.toxicity,
            'air_purification': self.air_purification,
            'flowering': self.flowering,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserPlant(db.Model):
    __tablename__ = 'user_plants'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)  # Reference to user in auth service
    plant_id = db.Column(db.Integer, db.ForeignKey('indoor_plants.id'), nullable=False)
    custom_name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    acquisition_date = db.Column(db.Date, nullable=True)
    last_watered = db.Column(db.Date, nullable=True)
    last_fertilized = db.Column(db.Date, nullable=True)
    last_repotted = db.Column(db.Date, nullable=True)
    health_status = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    watering_schedule = db.Column(db.Integer, nullable=True)  # Days between watering
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plant = db.relationship('IndoorPlant', backref='user_plants')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant': self.plant.to_dict() if self.plant else None,
            'custom_name': self.custom_name,
            'location': self.location,
            'acquisition_date': self.acquisition_date.isoformat() if self.acquisition_date else None,
            'last_watered': self.last_watered.isoformat() if self.last_watered else None,
            'last_fertilized': self.last_fertilized.isoformat() if self.last_fertilized else None,
            'last_repotted': self.last_repotted.isoformat() if self.last_repotted else None,
            'health_status': self.health_status,
            'notes': self.notes,
            'photo_url': self.photo_url,
            'watering_schedule': self.watering_schedule,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class GrowthEntry(db.Model):
    __tablename__ = 'growth_entries'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_plant_id = db.Column(db.String(36), db.ForeignKey('user_plants.id'), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    date = db.Column(db.Date, nullable=False)
    height = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    leaf_count = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_plant = db.relationship('UserPlant', backref='growth_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_plant_id': self.user_plant_id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'height': self.height,
            'width': self.width,
            'leaf_count': self.leaf_count,
            'photo_url': self.photo_url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WateringHistory(db.Model):
    __tablename__ = 'watering_history'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_plant_id = db.Column(db.String(36), db.ForeignKey('user_plants.id'), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    watered_at = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=True)  # Amount in ml
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_plant = db.relationship('UserPlant', backref='watering_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_plant_id': self.user_plant_id,
            'user_id': self.user_id,
            'watered_at': self.watered_at.isoformat() if self.watered_at else None,
            'amount': self.amount,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
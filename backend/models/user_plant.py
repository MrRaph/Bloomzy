from app import db
from datetime import datetime

class UserPlant(db.Model):
    __tablename__ = 'user_plants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey('indoor_plants.id'), nullable=False)
    
    # Informations personnalisées
    custom_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    pot_size = db.Column(db.String(20), nullable=True)
    soil_type = db.Column(db.String(100), nullable=True)
    acquired_date = db.Column(db.Date, nullable=True)
    
    # État actuel
    current_photo_url = db.Column(db.String(500), nullable=True)
    health_status = db.Column(db.String(20), default='healthy')  # healthy, sick, dying, dead
    notes = db.Column(db.Text, nullable=True)
    
    # Conditions actuelles
    light_exposure = db.Column(db.String(50), nullable=True)
    local_humidity = db.Column(db.Integer, nullable=True)
    ambient_temperature = db.Column(db.Integer, nullable=True)
    last_repotting = db.Column(db.Date, nullable=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='plants')
    species = db.relationship('IndoorPlant', backref='user_plants')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'species_id': self.species_id,
            'custom_name': self.custom_name,
            'location': self.location,
            'pot_size': self.pot_size,
            'soil_type': self.soil_type,
            'acquired_date': self.acquired_date.isoformat() if self.acquired_date else None,
            'current_photo_url': self.current_photo_url,
            'health_status': self.health_status,
            'notes': self.notes,
            'light_exposure': self.light_exposure,
            'local_humidity': self.local_humidity,
            'ambient_temperature': self.ambient_temperature,
            'last_repotting': self.last_repotting.isoformat() if self.last_repotting else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'species': self.species.to_dict() if self.species else None
        }
    
    def validate(self):
        """Validate user plant data"""
        errors = []
        
        if not self.custom_name or len(self.custom_name.strip()) < 1:
            errors.append("Custom name is required")
        
        if self.custom_name and len(self.custom_name) > 100:
            errors.append("Custom name must be less than 100 characters")
        
        if self.health_status and self.health_status not in ['healthy', 'sick', 'dying', 'dead']:
            errors.append("Health status must be one of: healthy, sick, dying, dead")
        
        if self.local_humidity is not None and (self.local_humidity < 0 or self.local_humidity > 100):
            errors.append("Local humidity must be between 0 and 100")
        
        if self.ambient_temperature is not None and (self.ambient_temperature < -20 or self.ambient_temperature > 50):
            errors.append("Ambient temperature must be between -20 and 50 degrees")
        
        return errors
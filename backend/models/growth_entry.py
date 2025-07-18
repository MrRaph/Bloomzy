from app import db
from datetime import datetime

class GrowthEntry(db.Model):
    __tablename__ = 'growth_entries'

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('user_plants.id'), nullable=False)
    
    # Métadonnées de l'entrée
    entry_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    entry_type = db.Column(db.String(20), nullable=False)  # photo, measurement, observation
    
    # Données photographiques
    photo_url = db.Column(db.String(500), nullable=True)
    photo_description = db.Column(db.String(200), nullable=True)
    
    # Métriques physiques
    height_cm = db.Column(db.Float, nullable=True)
    width_cm = db.Column(db.Float, nullable=True)
    leaf_count = db.Column(db.Integer, nullable=True)
    stem_count = db.Column(db.Integer, nullable=True)
    
    # Indicateurs de santé
    leaf_color = db.Column(db.String(50), nullable=True)  # green, yellow, brown, etc.
    stem_firmness = db.Column(db.String(20), nullable=True)  # firm, soft, brittle
    has_flowers = db.Column(db.Boolean, default=False)
    has_fruits = db.Column(db.Boolean, default=False)
    
    # Observations et notes
    health_notes = db.Column(db.Text, nullable=True)
    growth_notes = db.Column(db.Text, nullable=True)
    user_observations = db.Column(db.Text, nullable=True)
    
    # Analyse IA (pour future intégration)
    ai_health_score = db.Column(db.Float, nullable=True)  # 0-100 score
    ai_growth_analysis = db.Column(db.Text, nullable=True)
    ai_recommendations = db.Column(db.Text, nullable=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    plant = db.relationship('UserPlant', backref='growth_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'plant_id': self.plant_id,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'entry_type': self.entry_type,
            'photo_url': self.photo_url,
            'photo_description': self.photo_description,
            'height_cm': self.height_cm,
            'width_cm': self.width_cm,
            'leaf_count': self.leaf_count,
            'stem_count': self.stem_count,
            'leaf_color': self.leaf_color,
            'stem_firmness': self.stem_firmness,
            'has_flowers': self.has_flowers,
            'has_fruits': self.has_fruits,
            'health_notes': self.health_notes,
            'growth_notes': self.growth_notes,
            'user_observations': self.user_observations,
            'ai_health_score': self.ai_health_score,
            'ai_growth_analysis': self.ai_growth_analysis,
            'ai_recommendations': self.ai_recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def validate(self):
        """Validate growth entry data"""
        errors = []
        
        if not self.entry_type:
            errors.append("Entry type is required")
        
        if self.entry_type and self.entry_type not in ['photo', 'measurement', 'observation']:
            errors.append("Entry type must be one of: photo, measurement, observation")
        
        if self.height_cm is not None and (self.height_cm < 0 or self.height_cm > 1000):
            errors.append("Height must be between 0 and 1000 cm")
        
        if self.width_cm is not None and (self.width_cm < 0 or self.width_cm > 1000):
            errors.append("Width must be between 0 and 1000 cm")
        
        if self.leaf_count is not None and (self.leaf_count < 0 or self.leaf_count > 10000):
            errors.append("Leaf count must be between 0 and 10000")
        
        if self.stem_count is not None and (self.stem_count < 0 or self.stem_count > 1000):
            errors.append("Stem count must be between 0 and 1000")
        
        if self.leaf_color and self.leaf_color not in ['green', 'yellow', 'brown', 'red', 'purple', 'variegated']:
            errors.append("Leaf color must be one of: green, yellow, brown, red, purple, variegated")
        
        if self.stem_firmness and self.stem_firmness not in ['firm', 'soft', 'brittle']:
            errors.append("Stem firmness must be one of: firm, soft, brittle")
        
        if self.ai_health_score is not None and (self.ai_health_score < 0 or self.ai_health_score > 100):
            errors.append("AI health score must be between 0 and 100")
        
        if self.photo_description and len(self.photo_description) > 200:
            errors.append("Photo description must be less than 200 characters")
        
        return errors
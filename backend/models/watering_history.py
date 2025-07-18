from app import db
from datetime import datetime

class WateringHistory(db.Model):
    __tablename__ = 'watering_history'

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('user_plants.id'), nullable=False)
    
    # Informations d'arrosage
    watered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount_ml = db.Column(db.Integer, nullable=True)
    water_type = db.Column(db.String(50), nullable=True)  # tap, filtered, rainwater, etc.
    notes = db.Column(db.Text, nullable=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    plant = db.relationship('UserPlant', backref='watering_history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'plant_id': self.plant_id,
            'watered_at': self.watered_at.isoformat() if self.watered_at else None,
            'amount_ml': self.amount_ml,
            'water_type': self.water_type,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def validate(self):
        """Validate watering history data"""
        errors = []
        
        if not self.watered_at:
            errors.append("Watering date is required")
        
        if self.amount_ml is not None and (self.amount_ml < 0 or self.amount_ml > 10000):
            errors.append("Amount must be between 0 and 10000 ml")
        
        if self.water_type and self.water_type not in ['tap', 'filtered', 'rainwater', 'distilled', 'other']:
            errors.append("Water type must be one of: tap, filtered, rainwater, distilled, other")
        
        return errors
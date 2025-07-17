from app import db

class IndoorPlant(db.Model):
    __tablename__ = 'indoor_plants'

    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(128), nullable=False)
    common_names = db.Column(db.String(256))
    family = db.Column(db.String(128))
    origin = db.Column(db.String(128))
    difficulty = db.Column(db.String(64))
    watering_frequency = db.Column(db.String(64))
    light = db.Column(db.String(64))
    humidity = db.Column(db.String(64))
    temperature = db.Column(db.String(64))
    soil_type = db.Column(db.String(128))
    adult_size = db.Column(db.String(64))
    growth_rate = db.Column(db.String(64))
    toxicity = db.Column(db.String(128))
    air_purification = db.Column(db.Boolean, default=False)
    flowering = db.Column(db.String(128))

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
            'flowering': self.flowering
        }

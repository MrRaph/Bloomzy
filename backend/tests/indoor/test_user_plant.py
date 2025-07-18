import pytest
from datetime import datetime, date
from models.user import User, db
from models.indoor_plant import IndoorPlant
from models.user_plant import UserPlant
from models.watering_history import WateringHistory

class TestUserPlantModel:
    """Test suite for UserPlant model"""
    
    def test_user_plant_creation(self, app):
        """Test creating a new user plant"""
        with app.app_context():
            # Create test user
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            # Create test plant species
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            # Create user plant
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="My Beautiful Ficus",
                location="Living Room",
                pot_size="Medium",
                health_status="healthy"
            )
            db.session.add(user_plant)
            db.session.commit()
            
            # Verify creation
            assert user_plant.id is not None
            assert user_plant.user_id == user.id
            assert user_plant.species_id == species.id
            assert user_plant.custom_name == "My Beautiful Ficus"
            assert user_plant.location == "Living Room"
            assert user_plant.health_status == "healthy"
    
    def test_user_plant_to_dict(self, app):
        """Test UserPlant to_dict method"""
        with app.app_context():
            # Create test data
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="Test Plant",
                location="Bedroom",
                pot_size="Small",
                health_status="healthy",
                acquired_date=date(2023, 1, 15)
            )
            db.session.add(user_plant)
            db.session.commit()
            
            # Test to_dict
            plant_dict = user_plant.to_dict()
            assert plant_dict['id'] == user_plant.id
            assert plant_dict['user_id'] == user.id
            assert plant_dict['species_id'] == species.id
            assert plant_dict['custom_name'] == "Test Plant"
            assert plant_dict['location'] == "Bedroom"
            assert plant_dict['pot_size'] == "Small"
            assert plant_dict['health_status'] == "healthy"
            assert plant_dict['acquired_date'] == "2023-01-15"
            assert plant_dict['species'] is not None
            assert plant_dict['species']['scientific_name'] == "Ficus benjamina"
    
    def test_user_plant_validation_success(self, app):
        """Test successful validation of user plant data"""
        with app.app_context():
            user_plant = UserPlant(
                user_id=1,
                species_id=1,
                custom_name="Valid Plant",
                location="Living Room",
                health_status="healthy",
                local_humidity=65,
                ambient_temperature=22
            )
            
            errors = user_plant.validate()
            assert len(errors) == 0
    
    def test_user_plant_validation_errors(self, app):
        """Test validation errors for invalid user plant data"""
        with app.app_context():
            user_plant = UserPlant(
                user_id=1,
                species_id=1,
                custom_name="",  # Empty name
                health_status="invalid_status",  # Invalid health status
                local_humidity=150,  # Invalid humidity
                ambient_temperature=100  # Invalid temperature
            )
            
            errors = user_plant.validate()
            assert len(errors) == 4
            assert "Custom name is required" in errors
            assert "Health status must be one of: healthy, sick, dying, dead" in errors
            assert "Local humidity must be between 0 and 100" in errors
            assert "Ambient temperature must be between -20 and 50 degrees" in errors
    
    def test_user_plant_validation_name_length(self, app):
        """Test validation for name length"""
        with app.app_context():
            user_plant = UserPlant(
                user_id=1,
                species_id=1,
                custom_name="a" * 101,  # Too long
                health_status="healthy"
            )
            
            errors = user_plant.validate()
            assert len(errors) == 1
            assert "Custom name must be less than 100 characters" in errors
    
    def test_user_plant_relationships(self, app):
        """Test UserPlant relationships"""
        with app.app_context():
            # Create test data
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="Test Plant",
                health_status="healthy"
            )
            db.session.add(user_plant)
            db.session.commit()
            
            # Test relationships
            assert user_plant.user == user
            assert user_plant.species == species
            assert user_plant in user.plants
            assert user_plant in species.user_plants


class TestWateringHistoryModel:
    """Test suite for WateringHistory model"""
    
    def test_watering_history_creation(self, app):
        """Test creating a new watering history entry"""
        with app.app_context():
            # Create test data
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="Test Plant",
                health_status="healthy"
            )
            db.session.add(user_plant)
            db.session.commit()
            
            # Create watering history
            watering = WateringHistory(
                plant_id=user_plant.id,
                watered_at=datetime.now(),
                amount_ml=250,
                water_type="filtered",
                notes="Plant looked thirsty"
            )
            db.session.add(watering)
            db.session.commit()
            
            # Verify creation
            assert watering.id is not None
            assert watering.plant_id == user_plant.id
            assert watering.amount_ml == 250
            assert watering.water_type == "filtered"
            assert watering.notes == "Plant looked thirsty"
    
    def test_watering_history_to_dict(self, app):
        """Test WateringHistory to_dict method"""
        with app.app_context():
            # Create test data
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="Test Plant",
                health_status="healthy"
            )
            db.session.add(user_plant)
            db.session.commit()
            
            watering_time = datetime.now()
            watering = WateringHistory(
                plant_id=user_plant.id,
                watered_at=watering_time,
                amount_ml=300,
                water_type="tap",
                notes="Regular watering"
            )
            db.session.add(watering)
            db.session.commit()
            
            # Test to_dict
            watering_dict = watering.to_dict()
            assert watering_dict['id'] == watering.id
            assert watering_dict['plant_id'] == user_plant.id
            assert watering_dict['watered_at'] == watering_time.isoformat()
            assert watering_dict['amount_ml'] == 300
            assert watering_dict['water_type'] == "tap"
            assert watering_dict['notes'] == "Regular watering"
    
    def test_watering_history_validation_success(self, app):
        """Test successful validation of watering history data"""
        with app.app_context():
            watering = WateringHistory(
                plant_id=1,
                watered_at=datetime.now(),
                amount_ml=250,
                water_type="filtered",
                notes="Test watering"
            )
            
            errors = watering.validate()
            assert len(errors) == 0
    
    def test_watering_history_validation_errors(self, app):
        """Test validation errors for invalid watering history data"""
        with app.app_context():
            watering = WateringHistory(
                plant_id=1,
                watered_at=None,  # Missing date
                amount_ml=15000,  # Too much water
                water_type="invalid_type",  # Invalid water type
                notes="Test watering"
            )
            
            errors = watering.validate()
            assert len(errors) == 3
            assert "Watering date is required" in errors
            assert "Amount must be between 0 and 10000 ml" in errors
            assert "Water type must be one of: tap, filtered, rainwater, distilled, other" in errors
    
    def test_watering_history_relationship(self, app):
        """Test WateringHistory relationship with UserPlant"""
        with app.app_context():
            # Create test data
            user = User(email="test@example.com", password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            
            species = IndoorPlant(
                scientific_name="Ficus benjamina",
                common_names="Weeping Fig",
                family="Moraceae",
                difficulty="Easy"
            )
            db.session.add(species)
            db.session.commit()
            
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name="Test Plant",
                health_status="healthy"
            )
            db.session.add(user_plant)
            db.session.commit()
            
            watering = WateringHistory(
                plant_id=user_plant.id,
                watered_at=datetime.now(),
                amount_ml=250,
                water_type="filtered"
            )
            db.session.add(watering)
            db.session.commit()
            
            # Test relationship
            assert watering.plant == user_plant
            assert watering in user_plant.watering_history
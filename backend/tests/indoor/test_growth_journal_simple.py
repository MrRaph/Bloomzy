import pytest
import json
import jwt
from datetime import date, datetime, timedelta
from models.growth_entry import GrowthEntry
from models.user_plant import UserPlant
from models.indoor_plant import IndoorPlant
from models.user import User, db
from werkzeug.security import generate_password_hash

class TestGrowthJournalSimple:
    """Simple test suite for growth journal functionality"""
    
    def create_test_user(self, app):
        """Create a test user and return access token"""
        with app.app_context():
            user = User(
                email='test@example.com',
                password_hash=generate_password_hash('TestPassword123', method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()
            
            # Create JWT token using the same method as the auth routes
            payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            return user.id, access_token
    
    def test_growth_entry_creation(self, app, client):
        """Test creating a new growth entry"""
        user_id, token = self.create_test_user(app)
        
        with app.app_context():
            species = IndoorPlant(
                scientific_name="Monstera deliciosa",
                common_names="Monstera",
                difficulty="intermediate",
                watering_frequency=7
            )
            db.session.add(species)
            db.session.commit()
            
            plant = UserPlant(
                user_id=user_id,
                species_id=species.id,
                custom_name="My Monstera"
            )
            db.session.add(plant)
            db.session.commit()
            
            # Test data
            entry_data = {
                "entry_type": "measurement",
                "height_cm": 25.5,
                "width_cm": 30.0,
                "leaf_count": 8,
                "leaf_color": "green",
                "stem_firmness": "firm",
                "user_observations": "Plant is growing well"
            }
            
            headers = {'Authorization': f'Bearer {token}'}
            response = client.post(
                f'/api/plants/{plant.id}/growth-entries',
                json=entry_data,
                headers=headers
            )
            
            assert response.status_code == 201
            data = json.loads(response.data)
            
            assert data['entry_type'] == 'measurement'
            assert data['height_cm'] == 25.5
            assert data['width_cm'] == 30.0
            assert data['leaf_count'] == 8
            assert data['leaf_color'] == 'green'
            assert data['stem_firmness'] == 'firm'
            assert data['user_observations'] == 'Plant is growing well'
            assert data['plant_id'] == plant.id
    
    def test_growth_entry_validation(self, app, client):
        """Test growth entry validation"""
        user_id, token = self.create_test_user(app)
        
        with app.app_context():
            species = IndoorPlant(
                scientific_name="Monstera deliciosa",
                common_names="Monstera",
                difficulty="intermediate",
                watering_frequency=7
            )
            db.session.add(species)
            db.session.commit()
            
            plant = UserPlant(
                user_id=user_id,
                species_id=species.id,
                custom_name="My Monstera"
            )
            db.session.add(plant)
            db.session.commit()
            
            # Test invalid entry type
            invalid_data = {
                "entry_type": "invalid_type",
                "height_cm": 25.5
            }
            
            headers = {'Authorization': f'Bearer {token}'}
            response = client.post(
                f'/api/plants/{plant.id}/growth-entries',
                json=invalid_data,
                headers=headers
            )
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'Validation failed' in data['error']
            assert 'Entry type must be one of' in str(data['details'])
    
    def test_get_growth_entries(self, app, client):
        """Test retrieving growth entries for a plant"""
        user_id, token = self.create_test_user(app)
        
        with app.app_context():
            species = IndoorPlant(
                scientific_name="Monstera deliciosa",
                common_names="Monstera",
                difficulty="intermediate",
                watering_frequency=7
            )
            db.session.add(species)
            db.session.commit()
            
            plant = UserPlant(
                user_id=user_id,
                species_id=species.id,
                custom_name="My Monstera"
            )
            db.session.add(plant)
            db.session.commit()
            
            # Create test entries
            entry1 = GrowthEntry(
                plant_id=plant.id,
                entry_type="photo",
                photo_url="/test/photo1.jpg",
                entry_date=date(2024, 1, 1)
            )
            entry2 = GrowthEntry(
                plant_id=plant.id,
                entry_type="measurement",
                height_cm=20.0,
                entry_date=date(2024, 1, 15)
            )
            
            db.session.add_all([entry1, entry2])
            db.session.commit()
            
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get(
                f'/api/plants/{plant.id}/growth-entries',
                headers=headers
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            assert data['plant_id'] == plant.id
            assert data['total'] == 2
            assert len(data['entries']) == 2
            
            # Check entries are sorted by date descending
            assert data['entries'][0]['entry_date'] == '2024-01-15'
            assert data['entries'][1]['entry_date'] == '2024-01-01'
    
    def test_unauthorized_access(self, app, client):
        """Test that unauthenticated requests are rejected"""
        response = client.get('/api/plants/1/growth-entries')
        assert response.status_code == 401
        
        response = client.post('/api/plants/1/growth-entries')
        assert response.status_code == 401
        
        response = client.get('/api/plants/1/growth-analytics')
        assert response.status_code == 401
    
    def test_plant_not_found(self, app, client):
        """Test accessing growth entries for non-existent plant"""
        user_id, token = self.create_test_user(app)
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get(
            '/api/plants/999/growth-entries',
            headers=headers
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Plant not found' in data['error']
import pytest
import json
import jwt
from datetime import datetime, date, timedelta
from models.user import User, db
from models.indoor_plant import IndoorPlant
from models.user_plant import UserPlant
from models.watering_history import WateringHistory
from werkzeug.security import generate_password_hash

class TestUserPlantsAPISimple:
    """Simple test suite for User Plants API endpoints"""
    
    def setup_method(self):
        """Setup test data before each test"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123'
        }
        
        self.plant_species_data = {
            'scientific_name': 'Ficus benjamina',
            'common_names': 'Weeping Fig',
            'family': 'Moraceae',
            'difficulty': 'Easy',
            'watering_frequency': 'Weekly',
            'light': 'Bright indirect',
            'humidity': 'Medium',
            'temperature': '18-24°C'
        }
        
        self.user_plant_data = {
            'custom_name': 'My Beautiful Ficus',
            'location': 'Living Room',
            'pot_size': 'Medium',
            'soil_type': 'Potting mix',
            'acquired_date': '2023-01-15',
            'health_status': 'healthy',
            'notes': 'Bought from local nursery',
            'light_exposure': 'Bright indirect',
            'local_humidity': 65,
            'ambient_temperature': 22
        }
    
    def create_test_user(self, app):
        """Create a test user and return access token"""
        with app.app_context():
            user = User(
                email=self.user_data['email'],
                password_hash=generate_password_hash(self.user_data['password'], method='pbkdf2:sha256')
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
    
    def create_test_species(self, app):
        """Create a test plant species"""
        with app.app_context():
            species = IndoorPlant(**self.plant_species_data)
            db.session.add(species)
            db.session.commit()
            return species.id
    
    def test_get_my_plants_empty(self, app, client):
        """Test getting empty plants list"""
        user_id, token = self.create_test_user(app)
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/plants/my-plants', headers=headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['plants'] == []
        assert data['total'] == 0
    
    def test_create_my_plant_success(self, app, client):
        """Test creating a new user plant successfully"""
        user_id, token = self.create_test_user(app)
        species_id = self.create_test_species(app)
        
        plant_data = self.user_plant_data.copy()
        plant_data['species_id'] = species_id
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/api/plants/my-plants', 
                             json=plant_data, 
                             headers=headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['custom_name'] == plant_data['custom_name']
        assert data['location'] == plant_data['location']
        assert data['species_id'] == species_id
        assert data['user_id'] == user_id
        assert data['health_status'] == 'healthy'
    
    def test_create_my_plant_missing_fields(self, app, client):
        """Test creating a plant with missing required fields"""
        user_id, token = self.create_test_user(app)
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/api/plants/my-plants', 
                             json={}, 
                             headers=headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'species_id and custom_name are required' in data['error']
    
    def test_create_my_plant_invalid_species(self, app, client):
        """Test creating a plant with invalid species ID"""
        user_id, token = self.create_test_user(app)
        
        plant_data = {'species_id': 999, 'custom_name': 'Test Plant'}
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/api/plants/my-plants', 
                             json=plant_data, 
                             headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Plant species not found' in data['error']
    
    def test_create_my_plant_validation_error(self, app, client):
        """Test creating a plant with validation errors"""
        user_id, token = self.create_test_user(app)
        species_id = self.create_test_species(app)
        
        plant_data = {
            'species_id': species_id,
            'custom_name': 'Valid Name',  # Valid name
            'health_status': 'invalid_status',  # Invalid status
            'local_humidity': 150  # Invalid humidity
        }
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/api/plants/my-plants', 
                             json=plant_data, 
                             headers=headers)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']
        assert 'details' in data
    
    def test_unauthorized_access(self, app, client):
        """Test accessing endpoints without authentication"""
        response = client.get('/api/plants/my-plants')
        assert response.status_code == 401
        
        response = client.post('/api/plants/my-plants', json={})
        assert response.status_code == 401
        
        response = client.get('/api/plants/my-plants/1')
        assert response.status_code == 401
    
    def test_record_watering_success(self, app, client):
        """Test recording a watering event successfully"""
        user_id, token = self.create_test_user(app)
        species_id = self.create_test_species(app)
        
        # First create a plant
        plant_data = self.user_plant_data.copy()
        plant_data['species_id'] = species_id
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/api/plants/my-plants', 
                             json=plant_data, 
                             headers=headers)
        
        assert response.status_code == 201
        plant_id = json.loads(response.data)['id']
        
        # Now record watering
        watering_data = {
            'plant_id': plant_id,
            'amount_ml': 250,
            'water_type': 'filtered',
            'notes': 'Regular watering'
        }
        
        response = client.post('/api/plants/watering', 
                             json=watering_data, 
                             headers=headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['plant_id'] == plant_id
        assert data['amount_ml'] == 250
        assert data['water_type'] == 'filtered'
        assert data['notes'] == 'Regular watering'
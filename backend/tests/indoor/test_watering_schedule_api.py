import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import jwt
from models.user import User, db
from models.indoor_plant import IndoorPlant
from models.user_plant import UserPlant
from werkzeug.security import generate_password_hash

class TestWateringScheduleAPI:
    """Tests pour l'API de planning d'arrosage"""
    
    @pytest.fixture
    def mock_schedule_data(self):
        """Mock des données de planning d'arrosage"""
        return {
            'plant_id': 1,
            'adjusted_frequency_days': 7,
            'last_watering': '2023-06-10T12:00:00',
            'next_watering': '2023-06-17T12:00:00',
            'days_until_next': 4,
            'urgency': 'medium',
            'factors': {
                'base_frequency': 7.0,
                'season_factor': 0.8,
                'weather_factor': 1.0,
                'plant_factor': 1.1,
                'history_factor': 1.0
            },
            'weather_data': {
                'temperature': 22,
                'humidity': 65,
                'pressure': 1013
            },
            'calculated_at': '2023-06-13T12:00:00'
        }
    
    def create_test_user_and_plant(self, app):
        """Create test user and plant, return user_id, token, plant_id"""
        with app.app_context():
            # Create user
            user = User(
                email='test@example.com',
                password_hash=generate_password_hash('TestPassword123', method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()
            
            # Create species
            species = IndoorPlant(
                scientific_name='Ficus benjamina',
                common_names='Weeping Fig',
                watering_frequency=7
            )
            db.session.add(species)
            db.session.commit()
            
            # Create user plant
            user_plant = UserPlant(
                user_id=user.id,
                species_id=species.id,
                custom_name='Test Plant'
            )
            db.session.add(user_plant)
            db.session.commit()
            
            # Create token
            payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            return user.id, access_token, user_plant.id
    
    def test_get_watering_schedule_success(self, app, client, mock_schedule_data):
        """Test récupération réussie du planning d'arrosage"""
        user_id, token, plant_id = self.create_test_user_and_plant(app)
        headers = {'Authorization': f'Bearer {token}'}
        
        # Mock de l'algorithme
        with patch('routes.user_plants.WateringAlgorithm') as mock_algorithm_class:
            mock_algorithm = MagicMock()
            mock_schedule_data['plant_id'] = plant_id
            mock_algorithm.calculate_watering_schedule.return_value = mock_schedule_data
            mock_algorithm_class.return_value = mock_algorithm
            
            response = client.get(f'/api/plants/{plant_id}/watering-schedule', headers=headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['plant_id'] == plant_id
            assert data['adjusted_frequency_days'] == 7
            assert data['urgency'] == 'medium'
            assert 'factors' in data
            assert 'weather_data' in data
            
            # Vérification de l'appel à l'algorithme
            mock_algorithm.calculate_watering_schedule.assert_called_once_with(plant_id, user_id)
    
    def test_get_watering_schedule_unauthorized(self, client):
        """Test accès non autorisé au planning d'arrosage"""
        response = client.get('/api/plants/1/watering-schedule')
        assert response.status_code == 401
    
    def test_get_watering_schedule_plant_not_found(self, app, client):
        """Test planning d'arrosage pour plante inexistante"""
        user_id, token, plant_id = self.create_test_user_and_plant(app)
        headers = {'Authorization': f'Bearer {token}'}
        
        # Tenter d'accéder à une plante qui n'existe pas
        response = client.get('/api/plants/999/watering-schedule', headers=headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Plant not found'
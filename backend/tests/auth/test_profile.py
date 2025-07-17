import pytest
import json
from app import create_app
from models.user import db, User
from werkzeug.security import generate_password_hash


@pytest.fixture
def authenticated_user(app):
    """Crée un utilisateur authentifié avec token JWT"""
    with app.app_context():
        user = User(
            email='test@example.com',
            password_hash=generate_password_hash('password123', method='pbkdf2:sha256'),
            username='testuser'
        )
        db.session.add(user)
        db.session.commit()
        
        # Générer un token JWT
        import jwt
        import datetime
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return user, token


def test_get_profile_success(client, authenticated_user):
    """Test récupération du profil utilisateur"""
    user, token = authenticated_user
    
    response = client.get('/auth/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'
    assert data['username'] == 'testuser'
    assert 'id' in data
    assert 'created_at' in data


def test_get_profile_no_token(client):
    """Test récupération du profil sans token"""
    response = client.get('/auth/profile')
    assert response.status_code == 401


def test_get_profile_invalid_token(client):
    """Test récupération du profil avec token invalide"""
    response = client.get('/auth/profile', headers={
        'Authorization': 'Bearer invalid_token'
    })
    assert response.status_code == 401


def test_update_profile_success(client, authenticated_user):
    """Test mise à jour du profil utilisateur"""
    user, token = authenticated_user
    
    update_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'bio': 'Passionate about plants',
        'location': 'Paris, France',
        'timezone': 'Europe/Paris',
        'language': 'en'
    }
    
    response = client.put('/auth/profile', 
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['bio'] == 'Passionate about plants'
    assert data['location'] == 'Paris, France'
    assert data['timezone'] == 'Europe/Paris'
    assert data['language'] == 'en'


def test_update_profile_username_taken(client, authenticated_user, app):
    """Test mise à jour avec username déjà utilisé"""
    user, token = authenticated_user
    
    # Créer un autre utilisateur avec un username différent
    with app.app_context():
        other_user = User(
            email='other@example.com',
            password_hash=generate_password_hash('password123', method='pbkdf2:sha256'),
            username='otheruser'
        )
        db.session.add(other_user)
        db.session.commit()
    
    update_data = {'username': 'otheruser'}
    
    response = client.put('/auth/profile',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'Nom d\'utilisateur déjà utilisé' in data['error']


def test_update_profile_invalid_username(client, authenticated_user):
    """Test mise à jour avec username trop court"""
    user, token = authenticated_user
    
    update_data = {'username': 'ab'}  # Trop court
    
    response = client.put('/auth/profile',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'entre 3 et 80 caractères' in data['error']


def test_update_profile_bio_too_long(client, authenticated_user):
    """Test mise à jour avec bio trop longue"""
    user, token = authenticated_user
    
    update_data = {'bio': 'x' * 501}  # Trop long
    
    response = client.put('/auth/profile',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'limitée à 500 caractères' in data['error']


def test_update_profile_no_data(client, authenticated_user):
    """Test mise à jour sans données"""
    user, token = authenticated_user
    
    response = client.put('/auth/profile',
                         headers={'Authorization': f'Bearer {token}'},
                         json={})
    
    assert response.status_code == 200  # Empty dict should work fine
    data = json.loads(response.data)
    assert data['username'] == 'testuser'


def test_update_profile_preferences(client, authenticated_user):
    """Test mise à jour des préférences"""
    user, token = authenticated_user
    
    update_data = {
        'notifications_enabled': False,
        'email_notifications': False
    }
    
    response = client.put('/auth/profile',
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['notifications_enabled'] is False
    assert data['email_notifications'] is False
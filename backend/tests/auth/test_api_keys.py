import pytest
import json
from app import create_app
from models.user import db, User
from models.api_key import ApiKey
from werkzeug.security import generate_password_hash
import jwt
import datetime


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
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return user, token


def test_get_supported_services(client, authenticated_user):
    """Test récupération des services supportés"""
    user, token = authenticated_user
    
    response = client.get('/api/keys/services', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'services' in data
    assert 'openai' in data['services']
    assert 'claude' in data['services']


def test_create_api_key_success(client, authenticated_user):
    """Test création réussie d'une clé API"""
    user, token = authenticated_user
    
    api_key_data = {
        'service_name': 'openai',
        'api_key': 'sk-1234567890abcdef1234567890abcdef',
        'key_name': 'Ma clé OpenAI'
    }
    
    response = client.post('/api/keys/', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=api_key_data)
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['service_name'] == 'openai'
    assert data['key_name'] == 'Ma clé OpenAI'
    assert data['is_active'] is True
    assert 'api_key' not in data  # Clé chiffrée non exposée


def test_create_api_key_invalid_service(client, authenticated_user):
    """Test création avec service non supporté"""
    user, token = authenticated_user
    
    api_key_data = {
        'service_name': 'unknown_service',
        'api_key': 'sk-1234567890abcdef1234567890abcdef',
        'key_name': 'Ma clé'
    }
    
    response = client.post('/api/keys/', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=api_key_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Service non supporté' in data['error']


def test_create_api_key_invalid_format(client, authenticated_user):
    """Test création avec format de clé invalide"""
    user, token = authenticated_user
    
    api_key_data = {
        'service_name': 'openai',
        'api_key': 'invalid-key-format',
        'key_name': 'Ma clé OpenAI'
    }
    
    response = client.post('/api/keys/', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=api_key_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Format de clé API invalide' in data['error']


def test_create_api_key_missing_fields(client, authenticated_user):
    """Test création avec champs manquants"""
    user, token = authenticated_user
    
    api_key_data = {
        'service_name': 'openai',
        # api_key manquant
        'key_name': 'Ma clé OpenAI'
    }
    
    response = client.post('/api/keys/', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=api_key_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'requis' in data['error']


def test_list_api_keys(client, authenticated_user, app):
    """Test listage des clés API"""
    user, token = authenticated_user
    
    # Créer une clé API
    with app.app_context():
        api_key = ApiKey(
            user_id=user.id,
            service_name='openai',
            key_name='Ma clé test'
        )
        api_key.encrypt_key('sk-1234567890abcdef1234567890abcdef')
        db.session.add(api_key)
        db.session.commit()
    
    response = client.get('/api/keys/', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['service_name'] == 'openai'
    assert data[0]['key_name'] == 'Ma clé test'


def test_get_api_key_by_id(client, authenticated_user, app):
    """Test récupération d'une clé API par ID"""
    user, token = authenticated_user
    
    # Créer une clé API
    with app.app_context():
        api_key = ApiKey(
            user_id=user.id,
            service_name='claude',
            key_name='Ma clé Claude'
        )
        api_key.encrypt_key('sk-ant-1234567890abcdef1234567890abcdef')
        db.session.add(api_key)
        db.session.commit()
        key_id = api_key.id
    
    response = client.get(f'/api/keys/{key_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['service_name'] == 'claude'
    assert data['key_name'] == 'Ma clé Claude'


def test_get_api_key_not_found(client, authenticated_user):
    """Test récupération d'une clé API inexistante"""
    user, token = authenticated_user
    
    response = client.get('/api/keys/999', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'non trouvée' in data['error']


def test_update_api_key(client, authenticated_user, app):
    """Test mise à jour d'une clé API"""
    user, token = authenticated_user
    
    # Créer une clé API
    with app.app_context():
        api_key = ApiKey(
            user_id=user.id,
            service_name='openai',
            key_name='Ancienne clé'
        )
        api_key.encrypt_key('sk-1234567890abcdef1234567890abcdef')
        db.session.add(api_key)
        db.session.commit()
        key_id = api_key.id
    
    update_data = {
        'key_name': 'Nouvelle clé',
        'is_active': False
    }
    
    response = client.put(f'/api/keys/{key_id}', 
                         headers={'Authorization': f'Bearer {token}'},
                         json=update_data)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['key_name'] == 'Nouvelle clé'
    assert data['is_active'] is False


def test_delete_api_key(client, authenticated_user, app):
    """Test suppression d'une clé API"""
    user, token = authenticated_user
    
    # Créer une clé API
    with app.app_context():
        api_key = ApiKey(
            user_id=user.id,
            service_name='openai',
            key_name='Clé à supprimer'
        )
        api_key.encrypt_key('sk-1234567890abcdef1234567890abcdef')
        db.session.add(api_key)
        db.session.commit()
        key_id = api_key.id
    
    response = client.delete(f'/api/keys/{key_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'supprimée' in data['message']
    
    # Vérifier que la clé n'existe plus
    response = client.get(f'/api/keys/{key_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 404


def test_replace_active_key(client, authenticated_user, app):
    """Test remplacement d'une clé active par une nouvelle"""
    user, token = authenticated_user
    
    # Créer une première clé API
    with app.app_context():
        api_key1 = ApiKey(
            user_id=user.id,
            service_name='openai',
            key_name='Première clé'
        )
        api_key1.encrypt_key('sk-1234567890abcdef1234567890abcdef')
        db.session.add(api_key1)
        db.session.commit()
    
    # Créer une seconde clé pour le même service
    api_key_data = {
        'service_name': 'openai',
        'api_key': 'sk-abcdef1234567890abcdef1234567890',
        'key_name': 'Seconde clé'
    }
    
    response = client.post('/api/keys/', 
                          headers={'Authorization': f'Bearer {token}'},
                          json=api_key_data)
    
    assert response.status_code == 201
    
    # Vérifier que seule la nouvelle clé est active
    response = client.get('/api/keys/', headers={
        'Authorization': f'Bearer {token}'
    })
    
    data = json.loads(response.data)
    active_keys = [key for key in data if key['is_active']]
    assert len(active_keys) == 1
    assert active_keys[0]['key_name'] == 'Seconde clé'


def test_unauthorized_access(client):
    """Test accès sans authentification"""
    response = client.get('/api/keys/')
    assert response.status_code == 401
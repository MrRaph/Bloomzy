import pytest
from models.user import User
from werkzeug.security import generate_password_hash
import jwt
import datetime

def test_login_returns_jwt(client):
    email = 'jwtuser@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        user_email = user.email
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'token' in data
    secret = client.application.config.get('SECRET_KEY', 'dev-secret-key')
    payload = jwt.decode(data['token'], secret, algorithms=['HS256'])
    assert payload['user_id'] == user_id
    assert payload['email'] == user_email

def test_refresh_token(client):
    email = 'refreshuser@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        user_email = user.email
    # Connexion pour obtenir le token
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    token = response.get_json()['token']
    # Appel au refresh
    refresh_response = client.post('/auth/refresh', json={'token': token})
    refresh_data = refresh_response.get_json()
    assert refresh_response.status_code == 200
    assert 'token' in refresh_data
    # Le nouveau token doit être décodable
    secret = client.application.config.get('SECRET_KEY', 'dev-secret-key')
    new_payload = jwt.decode(refresh_data['token'], secret, algorithms=['HS256'])
    assert new_payload['user_id'] == user_id
    assert new_payload['email'] == user_email

def test_refresh_token_expired(client):
    # Génère un token expiré
    secret = client.application.config.get('SECRET_KEY', 'dev-secret-key')
    expired_payload = {
        'user_id': 1,
        'email': 'expired@example.com',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    }
    expired_token = jwt.encode(expired_payload, secret, algorithm='HS256')
    response = client.post('/auth/refresh', json={'token': expired_token})
    assert response.status_code == 401
    assert 'error' in response.get_json()

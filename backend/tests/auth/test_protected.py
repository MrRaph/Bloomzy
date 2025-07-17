import pytest
from models.user import User
from werkzeug.security import generate_password_hash
import jwt
import datetime

def test_protected_route_requires_token(client):
    response = client.get('/auth/protected')
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Token manquant'

def test_protected_route_with_valid_token(client):
    email = 'protected@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    # Connexion pour obtenir le token
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    token = response.get_json()['token']
    # Accès à la route protégée
    protected_response = client.get('/auth/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    assert protected_response.status_code == 200
    assert protected_response.get_json()['message'] == 'Accès autorisé'

def test_protected_route_with_revoked_token(client):
    email = 'revoked@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    token = response.get_json()['token']
    # Déconnexion (blacklist)
    client.post('/auth/logout', json={'token': token})
    # Accès à la route protégée avec token révoqué
    revoked_response = client.get('/auth/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    assert revoked_response.status_code == 401
    assert revoked_response.get_json()['error'] == 'Token révoqué'

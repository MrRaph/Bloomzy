import pytest
from models.user import User
from werkzeug.security import generate_password_hash
import jwt
import datetime

def test_logout_blacklists_token(client):
    email = 'logoutuser@example.com'
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
    # Déconnexion (blacklist)
    logout_response = client.post('/auth/logout', json={'token': token})
    assert logout_response.status_code == 200
    # Le token ne doit plus être utilisable pour refresh
    refresh_response = client.post('/auth/refresh', json={'token': token})
    assert refresh_response.status_code == 401
    assert refresh_response.get_json()['error'] == 'Token révoqué'

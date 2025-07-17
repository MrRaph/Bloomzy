import pytest
from flask import url_for
from models.user import User
from werkzeug.security import generate_password_hash

def test_login_success(client):
    # Préparation : création d'un utilisateur
    email = 'test@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    # Requête login
    response = client.post('/auth/login', json={
        'email': email,
        'password': password
    })
    assert response.status_code == 200
    assert 'user_id' in response.get_json()


def test_login_invalid_password(client):
    email = 'test2@example.com'
    password = 'Password123!'
    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    from models.user import db
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', json={
        'email': email,
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert 'error' in response.get_json()


def test_login_missing_fields(client):
    response = client.post('/auth/login', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

import pytest
from flask import Flask
from flask.testing import FlaskClient

# TODO: importer le module d'authentification

def test_signup_success(client: FlaskClient):
    """Test d'inscription réussie avec email et mot de passe valides."""
    response = client.post('/auth/signup', json={
        'email': 'user@example.com',
        'password': 'MotDePasseFort123!',
        'recaptcha_token': 'dummy-token'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['email'] == 'user@example.com'

def test_signup_weak_password(client: FlaskClient):
    """Test d'inscription avec un mot de passe trop faible."""
    response = client.post('/auth/signup', json={
        'email': 'user2@example.com',
        'password': '123',
        'recaptcha_token': 'dummy-token'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'mot de passe' in response.json['error'].lower()

def test_signup_invalid_email(client: FlaskClient):
    """Test d'inscription avec un email invalide."""
    response = client.post('/auth/signup', json={
        'email': 'not-an-email',
        'password': 'MotDePasseFort123!',
        'recaptcha_token': 'dummy-token'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'email' in response.json['error'].lower()

def test_signup_missing_fields(client: FlaskClient):
    """Test d'inscription avec des champs manquants."""
    response = client.post('/auth/signup', json={
        'email': 'user3@example.com',
        'recaptcha_token': 'dummy-token'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'champ' in response.json['error'].lower()

def test_signup_existing_email(client: FlaskClient):
    """Test d'inscription avec un email déjà utilisé."""
    # Première inscription
    client.post('/auth/signup', json={
        'email': 'user4@example.com',
        'password': 'MotDePasseFort123!',
        'recaptcha_token': 'dummy-token'
    })
    # Deuxième inscription avec le même email
    response = client.post('/auth/signup', json={
        'email': 'user4@example.com',
        'password': 'MotDePasseFort123!',
        'recaptcha_token': 'dummy-token'
    })
    assert response.status_code == 409
    assert 'error' in response.json
    assert 'existe' in response.json['error'].lower()

def test_signup_bot_protection(client: FlaskClient):
    """Test d'inscription sans token reCAPTCHA (protection contre les bots)."""
    response = client.post('/auth/signup', json={
        'email': 'user5@example.com',
        'password': 'MotDePasseFort123!'
        # Pas de champ 'recaptcha_token'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'captcha' in response.json['error'].lower()

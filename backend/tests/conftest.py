import pytest
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import create_app
from models.user import db, User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_session(app):
    """Provide a database session for tests"""
    return db.session

@pytest.fixture
def test_user(app):
    """Create a test user and return the user object"""
    user = User(
        email='test@example.com',
        password_hash=generate_password_hash('TestPassword123', method='pbkdf2:sha256')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_headers(app, test_user):
    """Generate authentication headers for API requests"""
    payload = {
        'user_id': test_user.id,
        'email': test_user.email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return {'Authorization': f'Bearer {access_token}'}

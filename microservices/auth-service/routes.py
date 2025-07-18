"""
Auth Service Routes
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
import re
import logging
from models import db, User, APIKey

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# JWT blacklist (in production, use Redis)
jwt_blacklist = set()

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        
        secret = current_app.config.get('SECRET_KEY')
        if token in jwt_blacklist:
            return jsonify({'error': 'Token révoqué'}), 401
        
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error': 'Utilisateur non trouvé'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def get_current_user():
    """Récupère l'utilisateur courant à partir du token JWT"""
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return None
    
    secret = current_app.config.get('SECRET_KEY')
    if token in jwt_blacklist:
        return None
    
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        # Email validation
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return jsonify({'error': 'Email invalide'}), 400
        
        # Password validation
        if len(password) < 8 or password.isdigit() or password.isalpha():
            return jsonify({'error': 'Mot de passe trop faible'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email existe déjà'}), 409
        
        # Create new user
        user = User(
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"User created successfully: {user.email}")
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email et mot de passe requis'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Identifiants invalides'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Compte désactivé'}), 401
        
        # Update last login
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        secret = current_app.config.get('SECRET_KEY')
        token = jwt.encode(payload, secret, algorithm='HS256')
        
        logger.info(f"User logged in successfully: {user.email}")
        return jsonify({
            'message': 'Connexion réussie',
            'user': user.to_dict(),
            'access_token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required
def logout(current_user):
    """User logout endpoint"""
    try:
        data = request.get_json()
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if token:
            jwt_blacklist.add(token)
        
        logger.info(f"User logged out successfully: {current_user.email}")
        return jsonify({'message': 'Déconnexion réussie'}), 200
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh():
    """Token refresh endpoint"""
    try:
        data = request.get_json()
        token = data.get('access_token') or data.get('token')
        
        if not token:
            return jsonify({'error': 'Token requis'}), 400
        
        secret = current_app.config.get('SECRET_KEY')
        
        if token in jwt_blacklist:
            return jsonify({'error': 'Token révoqué'}), 401
        
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            
            # Verify user still exists
            user = User.query.get(payload['user_id'])
            if not user or not user.is_active:
                return jsonify({'error': 'Utilisateur non trouvé'}), 401
            
            # Generate new token
            new_payload = {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            new_token = jwt.encode(new_payload, secret, algorithm='HS256')
            
            return jsonify({'access_token': new_token}), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401
        
    except Exception as e:
        logger.error(f"Error during token refresh: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/profile', methods=['GET'])
@jwt_required
def get_profile(current_user):
    """Get user profile"""
    try:
        return jsonify(current_user.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/profile', methods=['PUT'])
@jwt_required
def update_profile(current_user):
    """Update user profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        # Updatable fields
        updatable_fields = ['username', 'first_name', 'last_name', 'bio', 'location', 
                           'timezone', 'language', 'notifications_enabled', 'email_notifications']
        
        # Validate username uniqueness
        if 'username' in data and data['username'] != current_user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return jsonify({'error': 'Nom d\'utilisateur déjà utilisé'}), 409
        
        # Validate fields
        if 'username' in data and data['username']:
            if len(data['username']) < 3 or len(data['username']) > 80:
                return jsonify({'error': 'Nom d\'utilisateur entre 3 et 80 caractères'}), 400
        
        if 'bio' in data and data['bio'] and len(data['bio']) > 500:
            return jsonify({'error': 'Bio limitée à 500 caractères'}), 400
        
        # Update fields
        for field in updatable_fields:
            if field in data:
                setattr(current_user, field, data[field])
        
        current_user.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Profile updated successfully: {current_user.email}")
        return jsonify(current_user.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/verify', methods=['POST'])
def verify_token():
    """Verify JWT token (for other services)"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token requis'}), 400
        
        secret = current_app.config.get('SECRET_KEY')
        
        if token in jwt_blacklist:
            return jsonify({'error': 'Token révoqué'}), 401
        
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            
            # Verify user still exists
            user = User.query.get(payload['user_id'])
            if not user or not user.is_active:
                return jsonify({'error': 'Utilisateur non trouvé'}), 401
            
            return jsonify({
                'valid': True,
                'user_id': user.id,
                'email': user.email,
                'is_admin': user.is_admin
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401
        
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@auth_bp.route('/auth/users/<user_id>', methods=['GET'])
@jwt_required
def get_user_by_id(current_user, user_id):
    """Get user by ID (for other services)"""
    try:
        # Only allow access to own profile or admin access
        if current_user.id != user_id and not current_user.is_admin:
            return jsonify({'error': 'Accès refusé'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500
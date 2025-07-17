
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime, re
from models.user import db, User

# Blacklist JWT en mémoire (à remplacer par une solution persistante en prod)
jwt_blacklist = set()

bp = Blueprint('auth', __name__, url_prefix='/auth')

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
        secret = current_app.config.get('SECRET_KEY', 'dev-secret-key')
        if token in jwt_blacklist:
            return jsonify({'error': 'Token révoqué'}), 401
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expiré'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token invalide'}), 401
        return f(*args, **kwargs)
    return decorated

@bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'message': 'Accès autorisé'}), 200

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    recaptcha = data.get('recaptcha_token')

    if not email or not password:
        return jsonify({'error': 'Champs obligatoires manquants'}), 400

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return jsonify({'error': 'Email invalide'}), 400

    if len(password) < 8 or password.isdigit() or password.isalpha():
        return jsonify({'error': 'Mot de passe trop faible'}), 400

    if recaptcha is None:
        return jsonify({'error': 'Captcha requis'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email existe déjà'}), 409

    user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'email': user.email}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email et mot de passe requis.'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Identifiants invalides.'}), 401
    # Génération du token JWT
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    secret = current_app.config.get('SECRET_KEY', 'dev-secret-key')
    token = jwt.encode(payload, secret, algorithm='HS256')
    return jsonify({'message': 'Connexion réussie', 'user_id': user.id, 'token': token}), 200
@bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    token = data.get('token')
    secret = current_app.config.get('SECRET_KEY', 'dev-secret-key')
    try:
        if token in jwt_blacklist:
            return jsonify({'error': 'Token révoqué'}), 401
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        # Générer un nouveau token avec nouvelle expiration
        new_payload = {
            'user_id': payload['user_id'],
            'email': payload['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        new_token = jwt.encode(new_payload, secret, algorithm='HS256')
        return jsonify({'token': new_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token invalide'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data.get('token')
    if not token:
        return jsonify({'error': 'Token requis'}), 400
    jwt_blacklist.add(token)
    return jsonify({'message': 'Déconnexion réussie'}), 200

def get_current_user():
    """Récupère l'utilisateur courant à partir du token JWT"""
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return None
    
    secret = current_app.config.get('SECRET_KEY', 'dev-secret-key')
    if token in jwt_blacklist:
        return None
    
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    return jsonify(user.to_dict()), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Données requises'}), 400
    
    # Champs modifiables
    updatable_fields = ['username', 'first_name', 'last_name', 'bio', 'location', 
                       'timezone', 'language', 'notifications_enabled', 'email_notifications']
    
    # Validation username unique
    if 'username' in data and data['username'] != user.username:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'error': 'Nom d\'utilisateur déjà utilisé'}), 409
    
    # Validation des champs
    if 'username' in data and data['username']:
        if len(data['username']) < 3 or len(data['username']) > 80:
            return jsonify({'error': 'Nom d\'utilisateur entre 3 et 80 caractères'}), 400
    
    if 'bio' in data and data['bio'] and len(data['bio']) > 500:
        return jsonify({'error': 'Bio limitée à 500 caractères'}), 400
    
    # Mise à jour des champs
    for field in updatable_fields:
        if field in data:
            setattr(user, field, data[field])
    
    user.updated_at = datetime.datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour'}), 500

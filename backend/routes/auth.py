
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
from models.user import db, User

# Blacklist JWT en mémoire (à remplacer par une solution persistante en prod)
jwt_blacklist = set()

bp = Blueprint('auth', __name__, url_prefix='/auth')

def jwt_required(f):
    @wraps(f)


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

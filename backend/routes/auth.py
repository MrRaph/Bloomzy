from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime, re
from models.user import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

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
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Champs obligatoires manquants'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    secret = current_app.config.get('SECRET_KEY', 'dev-secret-key')
    token = jwt.encode(payload, secret, algorithm='HS256')
    return jsonify({'token': token}), 200

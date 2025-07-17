from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.api_key import ApiKey, db
from routes.auth import get_current_user, jwt_required
import re
from datetime import datetime

bp = Blueprint('api_keys', __name__, url_prefix='/api/keys')

SUPPORTED_SERVICES = ['openai', 'claude', 'gemini', 'huggingface']

def validate_service_name(service_name):
    """Valide le nom du service"""
    return service_name.lower() in SUPPORTED_SERVICES

def validate_api_key_format(service_name, api_key):
    """Valide le format de la clé API selon le service"""
    if service_name == 'openai':
        return api_key.startswith('sk-') and len(api_key) > 20
    elif service_name == 'claude':
        return api_key.startswith('sk-ant-') and len(api_key) > 20
    elif service_name == 'gemini':
        return len(api_key) > 20  # Format générique
    elif service_name == 'huggingface':
        return api_key.startswith('hf_') and len(api_key) > 20
    return False

@bp.route('/', methods=['GET'])
@jwt_required
def list_api_keys():
    """Liste les clés API de l'utilisateur"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    keys = ApiKey.query.filter_by(user_id=user.id).all()
    return jsonify([key.to_dict() for key in keys]), 200

@bp.route('/', methods=['POST'])
@jwt_required
def create_api_key():
    """Crée une nouvelle clé API"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données requises'}), 400
    
    service_name = data.get('service_name', '').lower()
    api_key = data.get('api_key', '')
    key_name = data.get('key_name', '')
    
    # Validations
    if not service_name or not api_key or not key_name:
        return jsonify({'error': 'service_name, api_key et key_name requis'}), 400
    
    if not validate_service_name(service_name):
        return jsonify({'error': f'Service non supporté. Services disponibles: {", ".join(SUPPORTED_SERVICES)}'}), 400
    
    if not validate_api_key_format(service_name, api_key):
        return jsonify({'error': 'Format de clé API invalide pour ce service'}), 400
    
    if len(key_name) < 3 or len(key_name) > 100:
        return jsonify({'error': 'Nom de clé entre 3 et 100 caractères'}), 400
    
    # Vérifier si une clé active existe déjà pour ce service
    existing_key = ApiKey.get_active_key_for_service(user.id, service_name)
    if existing_key:
        # Désactiver l'ancienne clé
        existing_key.is_active = False
    
    # Créer la nouvelle clé
    new_key = ApiKey(
        user_id=user.id,
        service_name=service_name,
        key_name=key_name
    )
    new_key.encrypt_key(api_key)
    
    try:
        db.session.add(new_key)
        db.session.commit()
        return jsonify(new_key.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la création'}), 500

@bp.route('/<int:key_id>', methods=['GET'])
@jwt_required
def get_api_key(key_id):
    """Récupère une clé API spécifique"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    api_key = ApiKey.query.filter_by(id=key_id, user_id=user.id).first()
    if not api_key:
        return jsonify({'error': 'Clé API non trouvée'}), 404
    
    return jsonify(api_key.to_dict()), 200

@bp.route('/<int:key_id>', methods=['PUT'])
@jwt_required
def update_api_key(key_id):
    """Met à jour une clé API"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    api_key = ApiKey.query.filter_by(id=key_id, user_id=user.id).first()
    if not api_key:
        return jsonify({'error': 'Clé API non trouvée'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données requises'}), 400
    
    # Seuls key_name et is_active peuvent être modifiés
    if 'key_name' in data:
        if len(data['key_name']) < 3 or len(data['key_name']) > 100:
            return jsonify({'error': 'Nom de clé entre 3 et 100 caractères'}), 400
        api_key.key_name = data['key_name']
    
    if 'is_active' in data:
        api_key.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify(api_key.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour'}), 500

@bp.route('/<int:key_id>', methods=['DELETE'])
@jwt_required
def delete_api_key(key_id):
    """Supprime une clé API"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    api_key = ApiKey.query.filter_by(id=key_id, user_id=user.id).first()
    if not api_key:
        return jsonify({'error': 'Clé API non trouvée'}), 404
    
    try:
        db.session.delete(api_key)
        db.session.commit()
        return jsonify({'message': 'Clé API supprimée'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la suppression'}), 500

@bp.route('/<int:key_id>/test', methods=['POST'])
@jwt_required
def test_api_key(key_id):
    """Teste une clé API"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    api_key = ApiKey.query.filter_by(id=key_id, user_id=user.id).first()
    if not api_key:
        return jsonify({'error': 'Clé API non trouvée'}), 404
    
    if not api_key.is_active:
        return jsonify({'error': 'Clé API désactivée'}), 400
    
    # Test de connexion (placeholder)
    try:
        success = api_key.test_connection()
        if success:
            api_key.last_used = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Clé API fonctionnelle', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Échec du test de connexion', 'status': 'error'}), 400
    except Exception as e:
        return jsonify({'error': 'Erreur lors du test'}), 500

@bp.route('/services', methods=['GET'])
@jwt_required
def get_supported_services():
    """Retourne la liste des services supportés"""
    return jsonify({'services': SUPPORTED_SERVICES}), 200
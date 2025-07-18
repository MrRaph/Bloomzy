"""
Plants Service Routes
"""
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import datetime
import logging
import requests
from models import db, IndoorPlant, UserPlant, GrowthEntry, WateringHistory

logger = logging.getLogger(__name__)

plants_bp = Blueprint('plants', __name__)

def auth_required(f):
    """Decorator to verify JWT token with auth service"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token manquant'}), 401
        
        try:
            # Verify token with auth service
            auth_service_url = current_app.config.get('AUTH_SERVICE_URL')
            response = requests.post(
                f'{auth_service_url}/auth/verify',
                json={'token': token},
                timeout=5
            )
            
            if response.status_code != 200:
                return jsonify({'error': 'Token invalide'}), 401
            
            user_data = response.json()
            return f(user_data, *args, **kwargs)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Auth service unavailable: {e}")
            return jsonify({'error': 'Service d\'authentification indisponible'}), 503
        except Exception as e:
            logger.error(f"Auth verification error: {e}")
            return jsonify({'error': 'Erreur d\'authentification'}), 500
    
    return decorated

# Indoor Plants endpoints
@plants_bp.route('/indoor-plants', methods=['GET'])
def list_indoor_plants():
    """List all indoor plants with optional filtering"""
    try:
        query = IndoorPlant.query
        
        # Search filter
        search = request.args.get('search')
        if search:
            query = query.filter(
                IndoorPlant.scientific_name.ilike(f'%{search}%') |
                IndoorPlant.common_names.ilike(f'%{search}%')
            )
        
        # Difficulty filter
        difficulty = request.args.get('difficulty')
        if difficulty:
            query = query.filter(IndoorPlant.difficulty == difficulty)
        
        # Family filter
        family = request.args.get('family')
        if family:
            query = query.filter(IndoorPlant.family == family)
        
        plants = query.all()
        return jsonify([plant.to_dict() for plant in plants]), 200
        
    except Exception as e:
        logger.error(f"Error listing plants: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/indoor-plants/<int:plant_id>', methods=['GET'])
def get_indoor_plant(plant_id):
    """Get a specific indoor plant by ID"""
    try:
        plant = IndoorPlant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting plant: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/indoor-plants', methods=['POST'])
@auth_required
def create_indoor_plant(user_data):
    """Create a new indoor plant (admin only)"""
    try:
        if not user_data.get('is_admin'):
            return jsonify({'error': 'Accès administrateur requis'}), 403
        
        data = request.get_json()
        
        if not data or not data.get('scientific_name'):
            return jsonify({'error': 'Nom scientifique requis'}), 400
        
        # Check if plant already exists
        existing_plant = IndoorPlant.query.filter_by(
            scientific_name=data.get('scientific_name')
        ).first()
        
        if existing_plant:
            return jsonify({'error': 'Plante existe déjà'}), 409
        
        # Handle common names
        common_names = data.get('common_names')
        if isinstance(common_names, list):
            common_names = ', '.join(common_names)
        
        plant = IndoorPlant(
            scientific_name=data.get('scientific_name'),
            common_names=common_names,
            family=data.get('family'),
            origin=data.get('origin'),
            difficulty=data.get('difficulty'),
            watering_frequency=data.get('watering_frequency'),
            light=data.get('light'),
            humidity=data.get('humidity'),
            temperature=data.get('temperature'),
            soil_type=data.get('soil_type'),
            adult_size=data.get('adult_size'),
            growth_rate=data.get('growth_rate'),
            toxicity=data.get('toxicity'),
            air_purification=data.get('air_purification', False),
            flowering=data.get('flowering')
        )
        
        db.session.add(plant)
        db.session.commit()
        
        logger.info(f"Plant created: {plant.scientific_name}")
        return jsonify(plant.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/indoor-plants/<int:plant_id>', methods=['PUT'])
@auth_required
def update_indoor_plant(user_data, plant_id):
    """Update an indoor plant (admin only)"""
    try:
        if not user_data.get('is_admin'):
            return jsonify({'error': 'Accès administrateur requis'}), 403
        
        plant = IndoorPlant.query.get_or_404(plant_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        # Update fields
        for key, value in data.items():
            if hasattr(plant, key):
                setattr(plant, key, value)
        
        plant.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Plant updated: {plant.scientific_name}")
        return jsonify(plant.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error updating plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/indoor-plants/<int:plant_id>', methods=['DELETE'])
@auth_required
def delete_indoor_plant(user_data, plant_id):
    """Delete an indoor plant (admin only)"""
    try:
        if not user_data.get('is_admin'):
            return jsonify({'error': 'Accès administrateur requis'}), 403
        
        plant = IndoorPlant.query.get_or_404(plant_id)
        
        # Check if plant is used by users
        user_plants = UserPlant.query.filter_by(plant_id=plant_id).count()
        if user_plants > 0:
            return jsonify({'error': 'Plante utilisée par des utilisateurs'}), 400
        
        db.session.delete(plant)
        db.session.commit()
        
        logger.info(f"Plant deleted: {plant.scientific_name}")
        return jsonify({'message': 'Plante supprimée avec succès'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

# User Plants endpoints
@plants_bp.route('/user-plants', methods=['GET'])
@auth_required
def list_user_plants(user_data):
    """List user's plants"""
    try:
        user_id = user_data.get('user_id')
        
        plants = UserPlant.query.filter_by(
            user_id=user_id,
            is_active=True
        ).all()
        
        return jsonify([plant.to_dict() for plant in plants]), 200
        
    except Exception as e:
        logger.error(f"Error listing user plants: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants', methods=['POST'])
@auth_required
def create_user_plant(user_data):
    """Add a plant to user's collection"""
    try:
        user_id = user_data.get('user_id')
        data = request.get_json()
        
        if not data or not data.get('plant_id'):
            return jsonify({'error': 'ID de plante requis'}), 400
        
        # Verify plant exists
        plant = IndoorPlant.query.get(data.get('plant_id'))
        if not plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        # Parse acquisition date
        acquisition_date = None
        if data.get('acquisition_date'):
            try:
                acquisition_date = datetime.datetime.strptime(
                    data.get('acquisition_date'), '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({'error': 'Format de date invalide'}), 400
        
        user_plant = UserPlant(
            user_id=user_id,
            plant_id=data.get('plant_id'),
            custom_name=data.get('custom_name'),
            location=data.get('location'),
            acquisition_date=acquisition_date,
            health_status=data.get('health_status', 'healthy'),
            notes=data.get('notes'),
            photo_url=data.get('photo_url'),
            watering_schedule=data.get('watering_schedule', plant.watering_frequency)
        )
        
        db.session.add(user_plant)
        db.session.commit()
        
        logger.info(f"User plant created: {user_plant.id}")
        return jsonify(user_plant.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating user plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants/<plant_id>', methods=['GET'])
@auth_required
def get_user_plant(user_data, plant_id):
    """Get a specific user plant"""
    try:
        user_id = user_data.get('user_id')
        
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        return jsonify(user_plant.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error getting user plant: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants/<plant_id>', methods=['PUT'])
@auth_required
def update_user_plant(user_data, plant_id):
    """Update a user plant"""
    try:
        user_id = user_data.get('user_id')
        
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        # Update fields
        updatable_fields = ['custom_name', 'location', 'health_status', 'notes', 
                           'photo_url', 'watering_schedule']
        
        for field in updatable_fields:
            if field in data:
                setattr(user_plant, field, data[field])
        
        # Handle date fields
        date_fields = ['last_watered', 'last_fertilized', 'last_repotted']
        for field in date_fields:
            if field in data and data[field]:
                try:
                    date_value = datetime.datetime.strptime(data[field], '%Y-%m-%d').date()
                    setattr(user_plant, field, date_value)
                except ValueError:
                    return jsonify({'error': f'Format de date invalide pour {field}'}), 400
        
        user_plant.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        logger.info(f"User plant updated: {user_plant.id}")
        return jsonify(user_plant.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error updating user plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants/<plant_id>', methods=['DELETE'])
@auth_required
def delete_user_plant(user_data, plant_id):
    """Delete a user plant (soft delete)"""
    try:
        user_id = user_data.get('user_id')
        
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        # Soft delete
        user_plant.is_active = False
        user_plant.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        
        logger.info(f"User plant deleted: {user_plant.id}")
        return jsonify({'message': 'Plante supprimée avec succès'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting user plant: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

# Growth Journal endpoints
@plants_bp.route('/user-plants/<plant_id>/growth', methods=['GET'])
@auth_required
def get_growth_entries(user_data, plant_id):
    """Get growth entries for a user plant"""
    try:
        user_id = user_data.get('user_id')
        
        # Verify plant ownership
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        entries = GrowthEntry.query.filter_by(
            user_plant_id=plant_id
        ).order_by(GrowthEntry.date.desc()).all()
        
        return jsonify([entry.to_dict() for entry in entries]), 200
        
    except Exception as e:
        logger.error(f"Error getting growth entries: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants/<plant_id>/growth', methods=['POST'])
@auth_required
def create_growth_entry(user_data, plant_id):
    """Create a new growth entry"""
    try:
        user_id = user_data.get('user_id')
        
        # Verify plant ownership
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        data = request.get_json()
        if not data or not data.get('date'):
            return jsonify({'error': 'Date requise'}), 400
        
        # Parse date
        try:
            entry_date = datetime.datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Format de date invalide'}), 400
        
        growth_entry = GrowthEntry(
            user_plant_id=plant_id,
            user_id=user_id,
            date=entry_date,
            height=data.get('height'),
            width=data.get('width'),
            leaf_count=data.get('leaf_count'),
            photo_url=data.get('photo_url'),
            notes=data.get('notes')
        )
        
        db.session.add(growth_entry)
        db.session.commit()
        
        logger.info(f"Growth entry created: {growth_entry.id}")
        return jsonify(growth_entry.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating growth entry: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500

# Watering endpoints
@plants_bp.route('/user-plants/<plant_id>/watering', methods=['GET'])
@auth_required
def get_watering_history(user_data, plant_id):
    """Get watering history for a user plant"""
    try:
        user_id = user_data.get('user_id')
        
        # Verify plant ownership
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        history = WateringHistory.query.filter_by(
            user_plant_id=plant_id
        ).order_by(WateringHistory.watered_at.desc()).all()
        
        return jsonify([entry.to_dict() for entry in history]), 200
        
    except Exception as e:
        logger.error(f"Error getting watering history: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500

@plants_bp.route('/user-plants/<plant_id>/watering', methods=['POST'])
@auth_required
def record_watering(user_data, plant_id):
    """Record a watering event"""
    try:
        user_id = user_data.get('user_id')
        
        # Verify plant ownership
        user_plant = UserPlant.query.filter_by(
            id=plant_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not user_plant:
            return jsonify({'error': 'Plante non trouvée'}), 404
        
        data = request.get_json()
        
        # Parse watering time
        watered_at = datetime.datetime.utcnow()
        if data and data.get('watered_at'):
            try:
                watered_at = datetime.datetime.fromisoformat(data.get('watered_at'))
            except ValueError:
                return jsonify({'error': 'Format de date/heure invalide'}), 400
        
        watering_record = WateringHistory(
            user_plant_id=plant_id,
            user_id=user_id,
            watered_at=watered_at,
            amount=data.get('amount') if data else None,
            notes=data.get('notes') if data else None
        )
        
        db.session.add(watering_record)
        
        # Update last watered date on user plant
        user_plant.last_watered = watered_at.date()
        user_plant.updated_at = datetime.datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Watering recorded: {watering_record.id}")
        return jsonify(watering_record.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error recording watering: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erreur serveur'}), 500
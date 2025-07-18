from flask import Blueprint, request, jsonify
from models.user import db, User
from models.indoor_plant import IndoorPlant
from models.user_plant import UserPlant
from models.watering_history import WateringHistory
from routes.auth import jwt_required, get_current_user
from services.watering_algorithm import WateringAlgorithm
from datetime import datetime, date
import os

user_plants_bp = Blueprint('user_plants', __name__, url_prefix='/api/plants')

@user_plants_bp.route('/my-plants', methods=['GET'])
@jwt_required
def get_my_plants():
    """Get all plants owned by the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        plants = UserPlant.query.filter_by(user_id=user.id).all()
        
        return jsonify({
            'plants': [plant.to_dict() for plant in plants],
            'total': len(plants)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/my-plants', methods=['POST'])
@jwt_required
def create_my_plant():
    """Create a new plant for the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('species_id') or not data.get('custom_name'):
            return jsonify({'error': 'species_id and custom_name are required'}), 400
        
        # Check if species exists
        species = IndoorPlant.query.get(data['species_id'])
        if not species:
            return jsonify({'error': 'Plant species not found'}), 404
        
        # Create new user plant
        user_plant = UserPlant(
            user_id=user.id,
            species_id=data['species_id'],
            custom_name=data['custom_name'],
            location=data.get('location'),
            pot_size=data.get('pot_size'),
            soil_type=data.get('soil_type'),
            acquired_date=datetime.strptime(data['acquired_date'], '%Y-%m-%d').date() if data.get('acquired_date') else None,
            current_photo_url=data.get('current_photo_url'),
            health_status=data.get('health_status', 'healthy'),
            notes=data.get('notes'),
            light_exposure=data.get('light_exposure'),
            local_humidity=data.get('local_humidity'),
            ambient_temperature=data.get('ambient_temperature'),
            last_repotting=datetime.strptime(data['last_repotting'], '%Y-%m-%d').date() if data.get('last_repotting') else None
        )
        
        # Validate the plant data
        validation_errors = user_plant.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        db.session.add(user_plant)
        db.session.commit()
        
        return jsonify(user_plant.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/my-plants/<int:plant_id>', methods=['GET'])
@jwt_required
def get_my_plant(plant_id):
    """Get a specific plant owned by the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        return jsonify(plant.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/my-plants/<int:plant_id>', methods=['PUT'])
@jwt_required
def update_my_plant(plant_id):
    """Update a specific plant owned by the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'custom_name' in data:
            plant.custom_name = data['custom_name']
        if 'location' in data:
            plant.location = data['location']
        if 'pot_size' in data:
            plant.pot_size = data['pot_size']
        if 'soil_type' in data:
            plant.soil_type = data['soil_type']
        if 'acquired_date' in data:
            plant.acquired_date = datetime.strptime(data['acquired_date'], '%Y-%m-%d').date() if data['acquired_date'] else None
        if 'current_photo_url' in data:
            plant.current_photo_url = data['current_photo_url']
        if 'health_status' in data:
            plant.health_status = data['health_status']
        if 'notes' in data:
            plant.notes = data['notes']
        if 'light_exposure' in data:
            plant.light_exposure = data['light_exposure']
        if 'local_humidity' in data:
            plant.local_humidity = data['local_humidity']
        if 'ambient_temperature' in data:
            plant.ambient_temperature = data['ambient_temperature']
        if 'last_repotting' in data:
            plant.last_repotting = datetime.strptime(data['last_repotting'], '%Y-%m-%d').date() if data['last_repotting'] else None
        
        # Validate the updated plant data
        validation_errors = plant.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        plant.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(plant.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/my-plants/<int:plant_id>', methods=['DELETE'])
@jwt_required
def delete_my_plant(plant_id):
    """Delete a specific plant owned by the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Delete associated watering history
        WateringHistory.query.filter_by(plant_id=plant_id).delete()
        
        # Delete the plant
        db.session.delete(plant)
        db.session.commit()
        
        return jsonify({'message': 'Plant deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/my-plants/<int:plant_id>/photo', methods=['POST'])
@jwt_required
def upload_plant_photo(plant_id):
    """Upload a photo for a specific plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Check if the post request has the file part
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo file provided'}), 400
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No photo file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'Invalid file type. Only JPG, JPEG, PNG, GIF are allowed'}), 400
        
        # For now, we'll just store the filename
        # In a real implementation, you would save the file to a storage service
        photo_url = f"/uploads/plants/{plant_id}_{file.filename}"
        plant.current_photo_url = photo_url
        plant.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo_url': photo_url
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Watering endpoints
@user_plants_bp.route('/watering', methods=['POST'])
@jwt_required
def record_watering():
    """Record a watering event for a plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        data = request.get_json()
        
        if not data or not data.get('plant_id'):
            return jsonify({'error': 'plant_id is required'}), 400
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=data['plant_id'], user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Create watering history entry
        watering = WateringHistory(
            plant_id=data['plant_id'],
            watered_at=datetime.strptime(data['watered_at'], '%Y-%m-%d %H:%M:%S') if data.get('watered_at') else datetime.utcnow(),
            amount_ml=data.get('amount_ml'),
            water_type=data.get('water_type'),
            notes=data.get('notes')
        )
        
        # Validate the watering data
        validation_errors = watering.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        db.session.add(watering)
        db.session.commit()
        
        return jsonify(watering.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DD HH:MM:SS'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/<int:plant_id>/watering-history', methods=['GET'])
@jwt_required
def get_watering_history(plant_id):
    """Get watering history for a specific plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get watering history
        watering_history = WateringHistory.query.filter_by(plant_id=plant_id).order_by(WateringHistory.watered_at.desc()).all()
        
        return jsonify({
            'plant_id': plant_id,
            'watering_history': [watering.to_dict() for watering in watering_history],
            'total': len(watering_history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/watering/<int:watering_id>', methods=['PUT'])
@jwt_required
def update_watering_record(watering_id):
    """Update a watering record"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get watering record and check ownership
        watering = WateringHistory.query.join(UserPlant).filter(
            WateringHistory.id == watering_id,
            UserPlant.user_id == user.id
        ).first()
        
        if not watering:
            return jsonify({'error': 'Watering record not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'watered_at' in data:
            watering.watered_at = datetime.strptime(data['watered_at'], '%Y-%m-%d %H:%M:%S')
        if 'amount_ml' in data:
            watering.amount_ml = data['amount_ml']
        if 'water_type' in data:
            watering.water_type = data['water_type']
        if 'notes' in data:
            watering.notes = data['notes']
        
        # Validate the updated watering data
        validation_errors = watering.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        db.session.commit()
        
        return jsonify(watering.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DD HH:MM:SS'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_plants_bp.route('/<int:plant_id>/watering-schedule', methods=['GET'])
@jwt_required
def get_watering_schedule(plant_id):
    """Get intelligent watering schedule for a specific plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Calculate watering schedule using algorithm
        algorithm = WateringAlgorithm()
        schedule = algorithm.calculate_watering_schedule(plant_id, user.id)
        
        if not schedule:
            return jsonify({'error': 'Unable to calculate watering schedule'}), 500
        
        return jsonify(schedule), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
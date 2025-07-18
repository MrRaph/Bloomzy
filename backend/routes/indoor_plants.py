from flask import Blueprint, request, jsonify
from models.indoor_plant import IndoorPlant
from app import db

indoor_plants_bp = Blueprint('indoor_plants', __name__, url_prefix='/indoor-plants')

@indoor_plants_bp.route('/', methods=['POST'])
def create_indoor_plant():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if not data.get('scientific_name'):
        return jsonify({'error': 'Scientific name is required'}), 400
    
    existing_plant = IndoorPlant.query.filter_by(
        scientific_name=data.get('scientific_name')
    ).first()
    if existing_plant:
        return jsonify({'error': 'Plant with this scientific name already exists'}), 409
    
    plant = IndoorPlant(
        scientific_name=data.get('scientific_name'),
        common_names=data.get('common_names'),
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
    
    try:
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create plant'}), 500

@indoor_plants_bp.route('/', methods=['GET'])
def list_indoor_plants():
    query = IndoorPlant.query
    search = request.args.get('search')
    if search:
        query = query.filter(
            IndoorPlant.scientific_name.ilike(f'%{search}%') |
            IndoorPlant.common_names.ilike(f'%{search}%')
        )
    
    difficulty = request.args.get('difficulty')
    if difficulty:
        query = query.filter(IndoorPlant.difficulty == difficulty)
    
    family = request.args.get('family')
    if family:
        query = query.filter(IndoorPlant.family == family)
    
    plants = query.all()
    return jsonify([p.to_dict() for p in plants]), 200

@indoor_plants_bp.route('/<int:plant_id>', methods=['GET'])
def get_indoor_plant(plant_id):
    plant = IndoorPlant.query.get_or_404(plant_id)
    return jsonify(plant.to_dict()), 200

@indoor_plants_bp.route('/<int:plant_id>', methods=['PUT'])
def update_indoor_plant(plant_id):
    plant = IndoorPlant.query.get_or_404(plant_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for key, value in data.items():
        if hasattr(plant, key):
            setattr(plant, key, value)
    
    db.session.commit()
    return jsonify(plant.to_dict()), 200

@indoor_plants_bp.route('/<int:plant_id>', methods=['DELETE'])
def delete_indoor_plant(plant_id):
    plant = IndoorPlant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted successfully'}), 200

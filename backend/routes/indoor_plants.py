from flask import Blueprint, request, jsonify
from models.indoor_plant import IndoorPlant
from app import db

indoor_plants_bp = Blueprint('indoor_plants', __name__, url_prefix='/indoor-plants')

@indoor_plants_bp.route('/', methods=['POST'])
def create_indoor_plant():
    data = request.get_json()
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
    db.session.add(plant)
    db.session.commit()
    return jsonify(plant.to_dict()), 201

@indoor_plants_bp.route('/', methods=['GET'])
def list_indoor_plants():
    query = IndoorPlant.query
    search = request.args.get('search')
    if search:
        query = query.filter(IndoorPlant.scientific_name.ilike(f'%{search}%'))
    plants = query.all()
    return jsonify([p.to_dict() for p in plants]), 200

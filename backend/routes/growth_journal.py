from flask import Blueprint, request, jsonify
from models.user import db, User
from models.user_plant import UserPlant
from models.growth_entry import GrowthEntry
from routes.auth import jwt_required, get_current_user
from datetime import datetime, date
from sqlalchemy import func

growth_journal_bp = Blueprint('growth_journal', __name__, url_prefix='/api/plants')

@growth_journal_bp.route('/<int:plant_id>/growth-entries', methods=['GET'])
@jwt_required
def get_growth_entries(plant_id):
    """Get all growth entries for a specific plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get query parameters for filtering
        entry_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', type=int)
        
        # Build query
        query = GrowthEntry.query.filter_by(plant_id=plant_id)
        
        if entry_type:
            query = query.filter(GrowthEntry.entry_type == entry_type)
        
        if start_date:
            query = query.filter(GrowthEntry.entry_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        
        if end_date:
            query = query.filter(GrowthEntry.entry_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        # Order by date descending
        query = query.order_by(GrowthEntry.entry_date.desc())
        
        if limit:
            query = query.limit(limit)
        
        entries = query.all()
        
        return jsonify({
            'plant_id': plant_id,
            'entries': [entry.to_dict() for entry in entries],
            'total': len(entries)
        }), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-entries', methods=['POST'])
@jwt_required
def create_growth_entry(plant_id):
    """Create a new growth entry for a plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if not data.get('entry_type'):
            return jsonify({'error': 'entry_type is required'}), 400
        
        # Create new growth entry
        entry = GrowthEntry(
            plant_id=plant_id,
            entry_date=datetime.strptime(data['entry_date'], '%Y-%m-%d').date() if data.get('entry_date') else date.today(),
            entry_type=data['entry_type'],
            photo_url=data.get('photo_url'),
            photo_description=data.get('photo_description'),
            height_cm=data.get('height_cm'),
            width_cm=data.get('width_cm'),
            leaf_count=data.get('leaf_count'),
            stem_count=data.get('stem_count'),
            leaf_color=data.get('leaf_color'),
            stem_firmness=data.get('stem_firmness'),
            has_flowers=data.get('has_flowers', False),
            has_fruits=data.get('has_fruits', False),
            health_notes=data.get('health_notes'),
            growth_notes=data.get('growth_notes'),
            user_observations=data.get('user_observations'),
            ai_health_score=data.get('ai_health_score'),
            ai_growth_analysis=data.get('ai_growth_analysis'),
            ai_recommendations=data.get('ai_recommendations')
        )
        
        # Validate the entry data
        validation_errors = entry.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify(entry.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-entries/<int:entry_id>', methods=['GET'])
@jwt_required
def get_growth_entry(plant_id, entry_id):
    """Get a specific growth entry"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get the specific entry
        entry = GrowthEntry.query.filter_by(id=entry_id, plant_id=plant_id).first()
        if not entry:
            return jsonify({'error': 'Growth entry not found'}), 404
        
        return jsonify(entry.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-entries/<int:entry_id>', methods=['PUT'])
@jwt_required
def update_growth_entry(plant_id, entry_id):
    """Update a specific growth entry"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get the specific entry
        entry = GrowthEntry.query.filter_by(id=entry_id, plant_id=plant_id).first()
        if not entry:
            return jsonify({'error': 'Growth entry not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'entry_date' in data:
            entry.entry_date = datetime.strptime(data['entry_date'], '%Y-%m-%d').date()
        if 'entry_type' in data:
            entry.entry_type = data['entry_type']
        if 'photo_url' in data:
            entry.photo_url = data['photo_url']
        if 'photo_description' in data:
            entry.photo_description = data['photo_description']
        if 'height_cm' in data:
            entry.height_cm = data['height_cm']
        if 'width_cm' in data:
            entry.width_cm = data['width_cm']
        if 'leaf_count' in data:
            entry.leaf_count = data['leaf_count']
        if 'stem_count' in data:
            entry.stem_count = data['stem_count']
        if 'leaf_color' in data:
            entry.leaf_color = data['leaf_color']
        if 'stem_firmness' in data:
            entry.stem_firmness = data['stem_firmness']
        if 'has_flowers' in data:
            entry.has_flowers = data['has_flowers']
        if 'has_fruits' in data:
            entry.has_fruits = data['has_fruits']
        if 'health_notes' in data:
            entry.health_notes = data['health_notes']
        if 'growth_notes' in data:
            entry.growth_notes = data['growth_notes']
        if 'user_observations' in data:
            entry.user_observations = data['user_observations']
        if 'ai_health_score' in data:
            entry.ai_health_score = data['ai_health_score']
        if 'ai_growth_analysis' in data:
            entry.ai_growth_analysis = data['ai_growth_analysis']
        if 'ai_recommendations' in data:
            entry.ai_recommendations = data['ai_recommendations']
        
        # Validate the updated entry data
        validation_errors = entry.validate()
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        entry.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(entry.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-entries/<int:entry_id>', methods=['DELETE'])
@jwt_required
def delete_growth_entry(plant_id, entry_id):
    """Delete a specific growth entry"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get the specific entry
        entry = GrowthEntry.query.filter_by(id=entry_id, plant_id=plant_id).first()
        if not entry:
            return jsonify({'error': 'Growth entry not found'}), 404
        
        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({'message': 'Growth entry deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-entries/photo', methods=['POST'])
@jwt_required
def upload_growth_photo(plant_id):
    """Upload a photo for a growth entry"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
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
        photo_url = f"/uploads/growth/{plant_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        # Create a new growth entry with the photo
        entry = GrowthEntry(
            plant_id=plant_id,
            entry_date=date.today(),
            entry_type='photo',
            photo_url=photo_url,
            photo_description=request.form.get('description', '')
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Growth photo uploaded successfully',
            'entry': entry.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-analytics', methods=['GET'])
@jwt_required
def get_growth_analytics(plant_id):
    """Get growth analytics and trends for a plant"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get all growth entries for analytics
        entries = GrowthEntry.query.filter_by(plant_id=plant_id).order_by(GrowthEntry.entry_date.asc()).all()
        
        if not entries:
            return jsonify({
                'plant_id': plant_id,
                'message': 'No growth data available',
                'analytics': {}
            }), 200
        
        # Calculate basic analytics
        analytics = {
            'total_entries': len(entries),
            'date_range': {
                'start': entries[0].entry_date.isoformat(),
                'end': entries[-1].entry_date.isoformat()
            },
            'entry_types': {},
            'growth_trends': {},
            'health_trends': {}
        }
        
        # Count entry types
        for entry in entries:
            entry_type = entry.entry_type
            analytics['entry_types'][entry_type] = analytics['entry_types'].get(entry_type, 0) + 1
        
        # Calculate growth trends
        height_data = [(entry.entry_date.isoformat(), entry.height_cm) for entry in entries if entry.height_cm is not None]
        width_data = [(entry.entry_date.isoformat(), entry.width_cm) for entry in entries if entry.width_cm is not None]
        leaf_data = [(entry.entry_date.isoformat(), entry.leaf_count) for entry in entries if entry.leaf_count is not None]
        
        analytics['growth_trends'] = {
            'height': height_data,
            'width': width_data,
            'leaf_count': leaf_data
        }
        
        # Calculate health trends
        health_scores = [(entry.entry_date.isoformat(), entry.ai_health_score) for entry in entries if entry.ai_health_score is not None]
        leaf_colors = [entry.leaf_color for entry in entries if entry.leaf_color is not None]
        
        analytics['health_trends'] = {
            'ai_health_scores': health_scores,
            'leaf_color_distribution': {color: leaf_colors.count(color) for color in set(leaf_colors)}
        }
        
        # Calculate growth rates if we have enough data
        if len(height_data) >= 2:
            first_height = height_data[0][1]
            last_height = height_data[-1][1]
            days_diff = (entries[-1].entry_date - entries[0].entry_date).days
            if days_diff > 0:
                analytics['growth_rates'] = {
                    'height_cm_per_day': (last_height - first_height) / days_diff,
                    'total_growth_cm': last_height - first_height,
                    'growth_period_days': days_diff
                }
        
        return jsonify({
            'plant_id': plant_id,
            'analytics': analytics
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@growth_journal_bp.route('/<int:plant_id>/growth-comparison', methods=['GET'])
@jwt_required
def get_growth_comparison(plant_id):
    """Get growth comparison between two time periods"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if plant exists and belongs to user
        plant = UserPlant.query.filter_by(id=plant_id, user_id=user.id).first()
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date are required'}), 400
        
        # Parse dates
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get entries for the specified period
        entries = GrowthEntry.query.filter(
            GrowthEntry.plant_id == plant_id,
            GrowthEntry.entry_date >= start_date_obj,
            GrowthEntry.entry_date <= end_date_obj
        ).order_by(GrowthEntry.entry_date.asc()).all()
        
        if len(entries) < 2:
            return jsonify({
                'plant_id': plant_id,
                'message': 'Not enough data for comparison',
                'comparison': {}
            }), 200
        
        # Compare first and last entries
        first_entry = entries[0]
        last_entry = entries[-1]
        
        comparison = {
            'period': {
                'start': first_entry.entry_date.isoformat(),
                'end': last_entry.entry_date.isoformat(),
                'days': (last_entry.entry_date - first_entry.entry_date).days
            },
            'changes': {}
        }
        
        # Calculate changes
        if first_entry.height_cm is not None and last_entry.height_cm is not None:
            comparison['changes']['height_cm'] = {
                'start': first_entry.height_cm,
                'end': last_entry.height_cm,
                'change': last_entry.height_cm - first_entry.height_cm
            }
        
        if first_entry.width_cm is not None and last_entry.width_cm is not None:
            comparison['changes']['width_cm'] = {
                'start': first_entry.width_cm,
                'end': last_entry.width_cm,
                'change': last_entry.width_cm - first_entry.width_cm
            }
        
        if first_entry.leaf_count is not None and last_entry.leaf_count is not None:
            comparison['changes']['leaf_count'] = {
                'start': first_entry.leaf_count,
                'end': last_entry.leaf_count,
                'change': last_entry.leaf_count - first_entry.leaf_count
            }
        
        # Health comparison
        if first_entry.ai_health_score is not None and last_entry.ai_health_score is not None:
            comparison['changes']['ai_health_score'] = {
                'start': first_entry.ai_health_score,
                'end': last_entry.ai_health_score,
                'change': last_entry.ai_health_score - first_entry.ai_health_score
            }
        
        # Photo comparison if available
        if first_entry.photo_url and last_entry.photo_url:
            comparison['photos'] = {
                'start': first_entry.photo_url,
                'end': last_entry.photo_url
            }
        
        return jsonify({
            'plant_id': plant_id,
            'comparison': comparison
        }), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
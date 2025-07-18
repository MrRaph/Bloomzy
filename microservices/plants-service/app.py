"""
Plants Service - Microservice for indoor plants management
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'plants-service-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///plants.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['AUTH_SERVICE_URL'] = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5001')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from routes import plants_bp
    app.register_blueprint(plants_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'plants-service',
            'version': '1.0.0',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/metrics')
    def metrics():
        """Prometheus metrics endpoint"""
        from models import IndoorPlant, UserPlant
        total_plants = IndoorPlant.query.count()
        total_user_plants = UserPlant.query.count()
        return jsonify({
            'total_plants': total_plants,
            'total_user_plants': total_user_plants
        }), 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=True)
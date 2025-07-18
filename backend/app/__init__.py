
from flask import Flask, jsonify
from flask_cors import CORS
from models.user import db
from routes.auth import bp as auth_bp
from routes.api_keys import bp as api_keys_bp
from routes.indoor_plants import indoor_plants_bp
from routes.user_plants import user_plants_bp
from routes.growth_journal import growth_journal_bp
import os

# Import models to ensure they are registered with SQLAlchemy
from models.user import User
from models.indoor_plant import IndoorPlant
from models.user_plant import UserPlant
from models.watering_history import WateringHistory
from models.growth_entry import GrowthEntry

def create_app():
    app = Flask(__name__)
    # Gestion dynamique de la chaîne de connexion DB (SQLite ou MySQL)
    db_url = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if not db_url:
        # Par défaut, SQLite fichier local
        db_url = 'sqlite:///../bloomzy.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Configuration CORS pour permettre les requêtes depuis le frontend
    CORS(app, origins=['http://localhost:8080'], supports_credentials=True)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_keys_bp)
    app.register_blueprint(indoor_plants_bp)
    app.register_blueprint(user_plants_bp)
    app.register_blueprint(growth_journal_bp)
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'bloomzy-backend',
            'database': 'connected'
        }), 200
      
    return app

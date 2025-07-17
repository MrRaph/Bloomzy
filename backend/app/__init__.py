
from flask import Flask, jsonify
from models.user import db
from routes.auth import bp as auth_bp
from routes.api_keys import bp as api_keys_bp
from routes.indoor_plants import indoor_plants_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_keys_bp)
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'bloomzy-backend',
            'database': 'connected'
        }), 200
    
    return app

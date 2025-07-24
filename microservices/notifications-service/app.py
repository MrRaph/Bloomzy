"""
Notifications Service - Microservice for notification management
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
import logging
import requests
from celery import Celery
import redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), 
                          port=int(os.environ.get('REDIS_PORT', 6379)), 
                          db=0)

def make_celery(app):
    """Create Celery app for background tasks"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'notifications-service-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///notifications.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['AUTH_SERVICE_URL'] = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5001')
    app.config['PLANTS_SERVICE_URL'] = os.environ.get('PLANTS_SERVICE_URL', 'http://plants-service:5002')
    
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create Celery app
    celery = make_celery(app)
    app.celery = celery
    
    # Register blueprints
    from routes import notifications_bp
    app.register_blueprint(notifications_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'notifications-service',
            'version': '1.0.0',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/metrics')
    def metrics():
        """Prometheus metrics endpoint"""
        from models import Notification, NotificationStatus
        
        total_notifications = Notification.query.count()
        scheduled_notifications = Notification.query.filter_by(
            status=NotificationStatus.SCHEDULED
        ).count()
        
        return jsonify({
            'total_notifications': total_notifications,
            'scheduled_notifications': scheduled_notifications,
            'redis_connected': redis_client.ping()
        }), 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003, debug=True)
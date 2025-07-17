from models.user import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_name = db.Column(db.String(50), nullable=False)  # openai, claude, etc.
    encrypted_key = db.Column(db.Text, nullable=False)
    key_name = db.Column(db.String(100), nullable=False)  # Nom donné par l'utilisateur
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Contrainte d'unicité : un utilisateur ne peut avoir qu'une clé active par service
    __table_args__ = (db.UniqueConstraint('user_id', 'service_name', 'is_active', name='unique_active_key_per_service'),)
    
    @staticmethod
    def get_encryption_key():
        """Récupère ou génère la clé de chiffrement"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # En développement, génère une clé temporaire
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = key.decode()
        return key if isinstance(key, bytes) else key.encode()
    
    def encrypt_key(self, api_key):
        """Chiffre une clé API"""
        fernet = Fernet(self.get_encryption_key())
        self.encrypted_key = fernet.encrypt(api_key.encode()).decode()
    
    def decrypt_key(self):
        """Déchiffre une clé API"""
        fernet = Fernet(self.get_encryption_key())
        return fernet.decrypt(self.encrypted_key.encode()).decode()
    
    def to_dict(self, include_key=False):
        """Convertit en dictionnaire, sans exposer la clé par défaut"""
        result = {
            'id': self.id,
            'service_name': self.service_name,
            'key_name': self.key_name,
            'is_active': self.is_active,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_key:
            result['api_key'] = self.decrypt_key()
        
        return result
    
    @classmethod
    def get_active_key_for_service(cls, user_id, service_name):
        """Récupère la clé active pour un service donné"""
        return cls.query.filter_by(
            user_id=user_id,
            service_name=service_name,
            is_active=True
        ).first()
    
    def test_connection(self):
        """Teste la connexion avec la clé API (à implémenter selon le service)"""
        # Placeholder - à implémenter selon le service
        return True
import requests
from typing import Dict, Optional
from datetime import datetime
from models.user import User
from models.api_key import ApiKey
from flask import current_app

class WeatherService:
    """Service pour récupérer les données météorologiques via API externe"""
    
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_data(self, user_id: int, latitude: float = None, longitude: float = None) -> Optional[Dict]:
        """
        Récupère les données météorologiques pour une localisation donnée
        
        Args:
            user_id: ID de l'utilisateur
            latitude: Latitude de la localisation (optionnel)
            longitude: Longitude de la localisation (optionnel)
            
        Returns:
            Dict avec les données météo ou None en cas d'erreur
        """
        try:
            # Récupération de la clé API de l'utilisateur
            api_key_record = ApiKey.query.filter_by(
                user_id=user_id, 
                service_name='openweathermap'
            ).first()
            
            if not api_key_record:
                current_app.logger.warning(f"Aucune clé API OpenWeatherMap trouvée pour l'utilisateur {user_id}")
                return None
                
            api_key = api_key_record.api_key
            
            # Utilisation de coordonnées par défaut si non fournies (Paris)
            if latitude is None or longitude is None:
                latitude, longitude = 48.8566, 2.3522
            
            # Appel à l'API OpenWeatherMap
            url = f"{self.base_url}/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Formatage des données pertinentes pour l'algorithme d'arrosage
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erreur lors de l'appel à l'API météo: {e}")
            return None
        except KeyError as e:
            current_app.logger.error(f"Erreur dans le format des données météo: {e}")
            return None
        except Exception as e:
            current_app.logger.error(f"Erreur inattendue dans le service météo: {e}")
            return None
    
    def calculate_weather_factor(self, weather_data: Dict) -> float:
        """
        Calcule un facteur météorologique pour ajuster la fréquence d'arrosage
        
        Args:
            weather_data: Données météorologiques
            
        Returns:
            Facteur entre 0.5 et 2.0 pour ajuster la fréquence d'arrosage
        """
        if not weather_data:
            return 1.0  # Facteur neutre si pas de données
            
        try:
            temperature = weather_data['temperature']
            humidity = weather_data['humidity']
            
            # Facteur basé sur la température (plus chaud = plus d'arrosage)
            # Température de référence: 20°C
            temp_factor = 1.0 + (temperature - 20) * 0.02
            temp_factor = max(0.5, min(2.0, temp_factor))
            
            # Facteur basé sur l'humidité (plus humide = moins d'arrosage)
            # Humidité de référence: 60%
            humidity_factor = 1.0 - (humidity - 60) * 0.01
            humidity_factor = max(0.5, min(2.0, humidity_factor))
            
            # Facteur combiné
            weather_factor = (temp_factor + humidity_factor) / 2
            
            return max(0.5, min(2.0, weather_factor))
            
        except (KeyError, TypeError, ValueError) as e:
            current_app.logger.error(f"Erreur dans le calcul du facteur météo: {e}")
            return 1.0
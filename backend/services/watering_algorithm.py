from typing import Dict, Optional
from datetime import datetime, timedelta
from models.user_plant import UserPlant
from models.watering_history import WateringHistory
from models.indoor_plant import IndoorPlant
from services.weather_service import WeatherService
from flask import current_app

class WateringAlgorithm:
    """Algorithme intelligent pour calculer la fréquence d'arrosage des plantes"""
    
    def __init__(self):
        self.weather_service = WeatherService()
    
    def calculate_watering_schedule(self, plant_id: int, user_id: int) -> Optional[Dict]:
        """
        Calcule le planning d'arrosage pour une plante donnée
        
        Args:
            plant_id: ID de la plante utilisateur
            user_id: ID de l'utilisateur
            
        Returns:
            Dict avec les recommandations d'arrosage ou None en cas d'erreur
        """
        try:
            # Récupération des données de la plante
            user_plant = UserPlant.query.filter_by(
                id=plant_id, 
                user_id=user_id
            ).first()
            
            if not user_plant:
                return None
                
            # Données météorologiques
            weather_data = self.weather_service.get_weather_data(
                user_id=user_id,
                latitude=user_plant.latitude,
                longitude=user_plant.longitude
            )
            
            # Calcul de la fréquence d'arrosage
            base_frequency = self._get_base_frequency(user_plant.species)
            season_factor = self._get_season_factor()
            weather_factor = self.weather_service.calculate_weather_factor(weather_data)
            plant_factor = self._calculate_plant_factor(user_plant)
            history_factor = self._calculate_history_factor(user_plant)
            
            # Calcul de la fréquence ajustée (en jours)
            adjusted_frequency = base_frequency * season_factor * weather_factor * plant_factor * history_factor
            adjusted_frequency = max(1, min(30, round(adjusted_frequency)))
            
            # Calcul des dates
            last_watering = self._get_last_watering_date(user_plant)
            if last_watering:
                next_watering = last_watering + timedelta(days=adjusted_frequency)
                days_until_next = (next_watering - datetime.utcnow()).days
            else:
                next_watering = datetime.utcnow()
                days_until_next = 0
            
            # Niveau d'urgence
            urgency = self._calculate_urgency(days_until_next)
            
            return {
                'plant_id': plant_id,
                'adjusted_frequency_days': adjusted_frequency,
                'last_watering': last_watering.isoformat() if last_watering else None,
                'next_watering': next_watering.isoformat(),
                'days_until_next': days_until_next,
                'urgency': urgency,
                'factors': {
                    'base_frequency': base_frequency,
                    'season_factor': season_factor,
                    'weather_factor': weather_factor,
                    'plant_factor': plant_factor,
                    'history_factor': history_factor
                },
                'weather_data': weather_data,
                'calculated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            current_app.logger.error(f"Erreur dans le calcul du planning d'arrosage: {e}")
            return None
    
    def _get_base_frequency(self, species: IndoorPlant) -> float:
        """Récupère la fréquence de base de l'espèce"""
        if species and species.watering_frequency:
            return float(species.watering_frequency)
        return 7.0  # Valeur par défaut : 7 jours
    
    def _get_season_factor(self) -> float:
        """Calcule le facteur saisonnier"""
        month = datetime.now().month
        
        # Printemps/Été (mars-août) : croissance active
        if 3 <= month <= 8:
            return 0.8  # Arrosage plus fréquent
        # Automne/Hiver (septembre-février) : croissance ralentie
        else:
            return 1.3  # Arrosage moins fréquent
    
    def _calculate_plant_factor(self, user_plant: UserPlant) -> float:
        """Calcule le facteur basé sur les caractéristiques de la plante"""
        factor = 1.0
        
        # Facteur taille du pot
        if user_plant.pot_size:
            pot_size = user_plant.pot_size.lower()
            if 'small' in pot_size or 'petit' in pot_size:
                factor *= 0.8  # Petit pot = arrosage plus fréquent
            elif 'large' in pot_size or 'grand' in pot_size:
                factor *= 1.2  # Grand pot = arrosage moins fréquent
        
        # Facteur type de substrat
        if user_plant.soil_type:
            soil = user_plant.soil_type.lower()
            if 'drainant' in soil or 'sable' in soil:
                factor *= 0.9  # Sol drainant = arrosage plus fréquent
            elif 'retenteur' in soil or 'terreau' in soil:
                factor *= 1.1  # Sol retenteur = arrosage moins fréquent
        
        # Facteur exposition lumineuse
        if user_plant.light_exposure:
            light = user_plant.light_exposure.lower()
            if 'direct' in light or 'fort' in light:
                factor *= 0.9  # Lumière forte = arrosage plus fréquent
            elif 'faible' in light or 'ombre' in light:
                factor *= 1.1  # Lumière faible = arrosage moins fréquent
        
        # Facteur température locale
        if user_plant.ambient_temperature:
            temp = user_plant.ambient_temperature
            if temp > 25:
                factor *= 0.9  # Température élevée = arrosage plus fréquent
            elif temp < 18:
                factor *= 1.1  # Température basse = arrosage moins fréquent
        
        return max(0.5, min(2.0, factor))
    
    def _calculate_history_factor(self, user_plant: UserPlant) -> float:
        """Calcule le facteur basé sur l'historique d'arrosage"""
        try:
            # Récupération des 10 derniers arrosages
            recent_waterings = WateringHistory.query.filter_by(
                user_plant_id=user_plant.id
            ).order_by(WateringHistory.watering_date.desc()).limit(10).all()
            
            if len(recent_waterings) < 2:
                return 1.0  # Pas assez d'historique
            
            # Calcul de la fréquence moyenne observée
            intervals = []
            for i in range(len(recent_waterings) - 1):
                interval = (recent_waterings[i].watering_date - recent_waterings[i+1].watering_date).days
                if interval > 0:
                    intervals.append(interval)
            
            if not intervals:
                return 1.0
                
            avg_interval = sum(intervals) / len(intervals)
            base_frequency = self._get_base_frequency(user_plant.species)
            
            # Ajustement basé sur l'écart entre fréquence théorique et observée
            if avg_interval > base_frequency * 1.2:
                return 1.1  # L'utilisateur arrose moins souvent
            elif avg_interval < base_frequency * 0.8:
                return 0.9  # L'utilisateur arrose plus souvent
            else:
                return 1.0  # Fréquence normale
                
        except Exception as e:
            current_app.logger.error(f"Erreur dans le calcul du facteur historique: {e}")
            return 1.0
    
    def _get_last_watering_date(self, user_plant: UserPlant) -> Optional[datetime]:
        """Récupère la date du dernier arrosage"""
        last_watering = WateringHistory.query.filter_by(
            user_plant_id=user_plant.id
        ).order_by(WateringHistory.watering_date.desc()).first()
        
        return last_watering.watering_date if last_watering else None
    
    def _calculate_urgency(self, days_until_next: int) -> str:
        """Calcule le niveau d'urgence"""
        if days_until_next <= 0:
            return "urgent"
        elif days_until_next <= 1:
            return "high"
        elif days_until_next <= 3:
            return "medium"
        else:
            return "low"
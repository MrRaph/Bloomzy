import pytest
from unittest.mock import patch, MagicMock
from services.weather_service import WeatherService

class TestWeatherServiceSimple:
    """Tests simplifiés pour le service météorologique"""
    
    @pytest.fixture
    def weather_service(self):
        return WeatherService()
    
    def test_calculate_weather_factor_no_data(self, weather_service):
        """Test calcul facteur météo sans données"""
        factor = weather_service.calculate_weather_factor(None)
        assert factor == 1.0
    
    def test_calculate_weather_factor_normal_conditions(self, weather_service):
        """Test calcul facteur météo conditions normales"""
        weather_data = {
            'temperature': 20,
            'humidity': 60
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert factor == 1.0
    
    def test_calculate_weather_factor_hot_dry(self, weather_service):
        """Test calcul facteur météo chaud et sec"""
        weather_data = {
            'temperature': 30,  # Chaud
            'humidity': 40      # Sec
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert factor > 1.0  # Plus d'arrosage nécessaire
    
    def test_calculate_weather_factor_cold_humid(self, weather_service):
        """Test calcul facteur météo froid et humide"""
        weather_data = {
            'temperature': 10,  # Froid
            'humidity': 80      # Humide
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert factor < 1.0  # Moins d'arrosage nécessaire
    
    def test_calculate_weather_factor_extreme_values(self, weather_service):
        """Test calcul facteur météo valeurs extrêmes"""
        weather_data = {
            'temperature': 50,  # Très chaud
            'humidity': 10      # Très sec
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert 0.5 <= factor <= 2.0  # Facteur borné
    
    def test_calculate_weather_factor_bounds(self, weather_service):
        """Test que le facteur météo reste dans les limites"""
        # Test limite inférieure
        weather_data = {
            'temperature': -20,  # Très froid
            'humidity': 100      # Très humide
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert factor >= 0.5
        
        # Test limite supérieure
        weather_data = {
            'temperature': 60,   # Très chaud
            'humidity': 0        # Très sec
        }
        
        factor = weather_service.calculate_weather_factor(weather_data)
        assert factor <= 2.0
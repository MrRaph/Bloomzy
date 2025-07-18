import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from services.watering_algorithm import WateringAlgorithm

class TestWateringAlgorithmSimple:
    """Tests simplifiés pour l'algorithme d'arrosage intelligent"""
    
    @pytest.fixture
    def algorithm(self):
        return WateringAlgorithm()
    
    def test_get_season_factor_spring_summer(self, algorithm):
        """Test facteur saisonnier printemps/été"""
        with patch('services.watering_algorithm.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 6, 15)  # Juin
            factor = algorithm._get_season_factor()
            assert factor == 0.8
    
    def test_get_season_factor_autumn_winter(self, algorithm):
        """Test facteur saisonnier automne/hiver"""
        with patch('services.watering_algorithm.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 12, 15)  # Décembre
            factor = algorithm._get_season_factor()
            assert factor == 1.3
    
    def test_calculate_urgency_urgent(self, algorithm):
        """Test calcul urgence - urgent"""
        urgency = algorithm._calculate_urgency(0)
        assert urgency == "urgent"
    
    def test_calculate_urgency_high(self, algorithm):
        """Test calcul urgence - élevée"""
        urgency = algorithm._calculate_urgency(1)
        assert urgency == "high"
    
    def test_calculate_urgency_medium(self, algorithm):
        """Test calcul urgence - moyenne"""
        urgency = algorithm._calculate_urgency(2)
        assert urgency == "medium"
    
    def test_calculate_urgency_low(self, algorithm):
        """Test calcul urgence - faible"""
        urgency = algorithm._calculate_urgency(5)
        assert urgency == "low"
    
    def test_get_base_frequency_with_species(self, algorithm):
        """Test récupération fréquence de base avec espèce"""
        mock_species = MagicMock()
        mock_species.watering_frequency = 7
        frequency = algorithm._get_base_frequency(mock_species)
        assert frequency == 7.0
    
    def test_get_base_frequency_without_species(self, algorithm):
        """Test récupération fréquence de base sans espèce"""
        frequency = algorithm._get_base_frequency(None)
        assert frequency == 7.0
    
    def test_calculate_plant_factor_default(self, algorithm):
        """Test calcul facteur plante avec valeurs par défaut"""
        mock_plant = MagicMock()
        mock_plant.pot_size = "medium"
        mock_plant.soil_type = "terreau"
        mock_plant.light_exposure = "indirect"
        mock_plant.ambient_temperature = 22
        
        factor = algorithm._calculate_plant_factor(mock_plant)
        assert 0.5 <= factor <= 2.0
    
    def test_calculate_plant_factor_small_pot(self, algorithm):
        """Test facteur plante avec petit pot"""
        mock_plant = MagicMock()
        mock_plant.pot_size = "small"
        mock_plant.soil_type = None
        mock_plant.light_exposure = None
        mock_plant.ambient_temperature = None
        
        factor = algorithm._calculate_plant_factor(mock_plant)
        assert factor < 1.0  # Petit pot = arrosage plus fréquent
    
    def test_calculate_plant_factor_large_pot(self, algorithm):
        """Test facteur plante avec grand pot"""
        mock_plant = MagicMock()
        mock_plant.pot_size = "large"
        mock_plant.soil_type = None
        mock_plant.light_exposure = None
        mock_plant.ambient_temperature = None
        
        factor = algorithm._calculate_plant_factor(mock_plant)
        assert factor > 1.0  # Grand pot = arrosage moins fréquent
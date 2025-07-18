import pytest
from models.indoor_plant import IndoorPlant
from app import db

def test_indoor_plant_creation(app):
    with app.app_context():
        plant = IndoorPlant(
            scientific_name="Monstera deliciosa",
            common_names="Monstera, Swiss Cheese Plant",
            family="Araceae",
            origin="Amérique centrale",
            difficulty="Facile",
            watering_frequency="Hebdomadaire",
            light="Lumineux, indirect",
            humidity="Moyenne à élevée",
            temperature="18-27°C",
            soil_type="Drainant",
            adult_size="2m",
            growth_rate="Rapide",
            toxicity="Toxique pour animaux",
            air_purification=True,
            flowering="Rare en intérieur"
        )
        db.session.add(plant)
        db.session.commit()
        assert plant.id is not None

def test_indoor_plant_serialization(app):
    with app.app_context():
        plant = IndoorPlant(
            scientific_name="Ficus lyrata",
            common_names="Figuier lyre",
            family="Moraceae",
            origin="Afrique de l'Ouest",
            difficulty="Moyen",
            watering_frequency="Bi-mensuel",
            light="Lumineux",
            humidity="Moyenne",
            temperature="20-25°C",
            soil_type="Riche et drainant",
            adult_size="3m",
            growth_rate="Moyen",
            toxicity="Non toxique",
            air_purification=False,
            flowering="Rare"
        )
        data = plant.to_dict()
        assert data["scientific_name"] == "Ficus lyrata"
        assert data["toxicity"] == "Non toxique"

def test_indoor_plant_db_add_and_query(app):
    with app.app_context():
        plant = IndoorPlant(scientific_name="Calathea orbifolia")
        db.session.add(plant)
        db.session.commit()
        found = IndoorPlant.query.filter_by(scientific_name="Calathea orbifolia").first()
        assert found is not None
        assert found.scientific_name == "Calathea orbifolia"

# Squelette pour les futurs tests d'API (endpoints CRUD et recherche)
def test_api_create_indoor_plant(app, client):
    with app.app_context():
        payload = {
            "scientific_name": "Sansevieria trifasciata",
            "common_names": "Snake Plant, Langue de belle-mère",
            "family": "Asparagaceae",
            "origin": "Afrique de l'Ouest",
            "difficulty": "Facile",
            "watering_frequency": "Mensuel",
            "light": "Peu lumineux à lumineux",
            "humidity": "Faible à moyenne",
            "temperature": "15-30°C",
            "soil_type": "Drainant",
            "adult_size": "1m",
            "growth_rate": "Lent",
            "toxicity": "Toxique pour animaux",
            "air_purification": True,
            "flowering": "Rare"
        }
        response = client.post("/indoor-plants/", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["scientific_name"] == "Sansevieria trifasciata"
        assert data["air_purification"] is True

def test_api_search_indoor_plant(app, client):
    with app.app_context():
        # Ajout d'une plante pour la recherche
        plant = {
            "scientific_name": "Chlorophytum comosum",
            "common_names": "Plante araignée",
            "family": "Asparagaceae"
        }
        client.post("/indoor-plants/", json=plant)
        # Recherche par nom scientifique
        response = client.get("/indoor-plants/?search=Chlorophytum")
        assert response.status_code == 200
        results = response.get_json()
        assert any(p["scientific_name"] == "Chlorophytum comosum" for p in results)

def test_api_get_indoor_plant_by_id(app, client):
    with app.app_context():
        # Créer une plante
        plant_data = {
            "scientific_name": "Pothos aureus",
            "common_names": "Pothos doré",
            "family": "Araceae"
        }
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 201
        plant_id = response.get_json()["id"]
        
        # Récupérer la plante par ID
        response = client.get(f"/indoor-plants/{plant_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["scientific_name"] == "Pothos aureus"

def test_api_get_nonexistent_plant(app, client):
    with app.app_context():
        response = client.get("/indoor-plants/999")
        assert response.status_code == 404

def test_api_update_indoor_plant(app, client):
    with app.app_context():
        # Créer une plante
        plant_data = {
            "scientific_name": "Ficus benjamina",
            "common_names": "Ficus",
            "difficulty": "Moyen"
        }
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 201
        plant_id = response.get_json()["id"]
        
        # Mettre à jour la plante
        update_data = {
            "difficulty": "Facile",
            "watering_frequency": "Hebdomadaire"
        }
        response = client.put(f"/indoor-plants/{plant_id}", json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data["difficulty"] == "Facile"
        assert data["watering_frequency"] == "Hebdomadaire"

def test_api_update_nonexistent_plant(app, client):
    with app.app_context():
        response = client.put("/indoor-plants/999", json={"difficulty": "Facile"})
        assert response.status_code == 404

def test_api_delete_indoor_plant(app, client):
    with app.app_context():
        # Créer une plante
        plant_data = {
            "scientific_name": "Aloe vera",
            "common_names": "Aloès"
        }
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 201
        plant_id = response.get_json()["id"]
        
        # Supprimer la plante
        response = client.delete(f"/indoor-plants/{plant_id}")
        assert response.status_code == 200
        
        # Vérifier que la plante n'existe plus
        response = client.get(f"/indoor-plants/{plant_id}")
        assert response.status_code == 404

def test_api_search_with_filters(app, client):
    with app.app_context():
        # Créer plusieurs plantes
        plants = [
            {
                "scientific_name": "Cactus opuntia",
                "family": "Cactaceae",
                "difficulty": "Facile"
            },
            {
                "scientific_name": "Orchidaceae vanda",
                "family": "Orchidaceae",
                "difficulty": "Difficile"
            }
        ]
        
        for plant in plants:
            client.post("/indoor-plants/", json=plant)
        
        # Recherche par famille
        response = client.get("/indoor-plants/?family=Cactaceae")
        assert response.status_code == 200
        results = response.get_json()
        assert len(results) == 1
        assert results[0]["family"] == "Cactaceae"
        
        # Recherche par difficulté
        response = client.get("/indoor-plants/?difficulty=Facile")
        assert response.status_code == 200
        results = response.get_json()
        assert len(results) >= 1
        assert all(p["difficulty"] == "Facile" for p in results)

def test_api_create_duplicate_plant(app, client):
    with app.app_context():
        plant_data = {
            "scientific_name": "Duplicata species",
            "common_names": "Plante test"
        }
        
        # Créer la première plante
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 201
        
        # Essayer de créer une plante avec le même nom scientifique
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 409
        data = response.get_json()
        assert "already exists" in data["error"]

def test_api_create_plant_without_scientific_name(app, client):
    with app.app_context():
        plant_data = {
            "common_names": "Plante sans nom scientifique"
        }
        
        response = client.post("/indoor-plants/", json=plant_data)
        assert response.status_code == 400
        data = response.get_json()
        assert "Scientific name is required" in data["error"]

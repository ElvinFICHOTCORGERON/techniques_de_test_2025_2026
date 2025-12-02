import pytest
from src.triangulator.api import create_app
from flask import Response

POINT_SET_ID = "123e4567-e89b-12d3-a456-426614174000"
INVALID_ID = "caillou"


@pytest.fixture
def client():
    """Crée un client Flask pour les tests d'API."""
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_api_invalid_uuid_400(client):
    """
    Test de validation: Vérifie qu'une requête avec un identifiant non UUID
    est correctement refusée par la couche d'API/routage.
    Statut attendu: 400 Bad Request.
    """
    response = client.get(f"/triangulation/{INVALID_ID}")

    assert response.status_code == 400
    assert response.is_json
    assert "code" in response.json
    assert response.content_type == 'application/json'


def test_api_endpoint_response_format(client):
    """
    Vérifie qu'une requête pour un ID valide retourne un type de contenu JSON
    en cas d'échec de service (avant tout mocking).
    """
    response = client.get(f"/triangulation/{POINT_SET_ID}")
    assert response.status_code in [404, 503, 500] 
    assert response.is_json
    assert response.content_type == 'application/json'
    assert isinstance(response, Response)
    
ef test_api_missing_id_404(client):
    """
    Test de validation: Vérifie qu'une requête sans PointSetID (endpoint tronqué)
    est gérée comme une ressource non trouvée par le routeur Flask.
    Statut attendu: 404 Not Found (Erreur de routage/ressource manquante).
    """
    response = client.get("/triangulation/") 

    assert response.status_code == 404 

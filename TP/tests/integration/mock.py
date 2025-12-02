import pytest
import struct
from flask import Response
from src.triangulator.api import create_app
from src.triangulator import client_psm 
from src.triangulator.client_psm import PointSetNotFound, PointSetManagerUnavailable
from src.triangulator.core import triangulate_points 


POINT_SET_ID = "123e4567-e89b-12d3-a456-426614174000"
NOT_FOUND_ID = "00000000-0000-0000-0000-000000000000"

MOCK_POINTSET_BIN = struct.pack('<I', 3) + b"\x00\x00\x00\x00" * 6 
MOCK_TRIANGLES_BIN = b'MOCKED_TRIANGLES_RESULT' 

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_integration_success_workflow(client, monkeypatch):
    """
    Teste le scénario nominal complet : PSM(OK) -> Triangulation(OK) -> Réponse 200 Binaire.
    """
    def mock_get_psm_success(_id):
        return MOCK_POINTSET_BIN
    
    def mock_triangulate_success(_data):
        return MOCK_TRIANGLES_BIN

    monkeypatch.setattr("src.triangulator.client_psm.get_pointset_bytes", mock_get_psm_success)
    monkeypatch.setattr("src.triangulator.core.triangulate_points", mock_triangulate_success)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 200
    assert response.mimetype == "application/octet-stream"
    assert response.data == MOCK_TRIANGLES_BIN


def test_integration_not_found_404(client, monkeypatch):
    """
    Teste la gestion d'une erreur 404 reçue du PointSetManager.
    Le Triangulator doit intercepter l'exception PointSetNotFound et répondre 404.
    """
    def mock_get_psm_404(_id):
        raise PointSetNotFound("PointSet ID non trouvé")

    monkeypatch.setattr("src.triangulator.client_psm.get_pointset_bytes", mock_get_psm_404)

    response = client.get(f"/triangulation/{NOT_FOUND_ID}")

    assert response.status_code == 404
    assert response.is_json
    assert response.json["code"] == "NOT_FOUND"


def test_integration_service_unavailable_503(client, monkeypatch):
    """
    Teste la gestion d'une indisponibilité du PointSetManager (erreur réseau ou 503).
    Le Triangulator doit intercepter l'exception PointSetManagerUnavailable et répondre 503.
    """
    def mock_get_psm_503(_id):
        raise PointSetManagerUnavailable("PSM inaccessible ou en panne")

    monkeypatch.setattr("src.triangulator.client_psm.get_pointset_bytes", mock_get_psm_503)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 503
    assert response.is_json
    assert response.json["code"] == "SERVICE_UNAVAILABLE"


def test_integration_internal_algorithm_failure_500(client, monkeypatch):
    """
    Teste le cas où l'algorithme de triangulation lève une erreur interne.
    Le Triangulator doit intercepter l'erreur et répondre 500.
    """
    def mock_get_psm_success(_id):
        return MOCK_POINTSET_BIN
    
    def mock_triangulate_failure(_data):
        raise ValueError("Erreur de calcul interne non gérée")

    monkeypatch.setattr("src.triangulator.client_psm.get_pointset_bytes", mock_get_psm_success)
    monkeypatch.setattr("src.triangulator.core.triangulate_points", mock_triangulate_failure)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 500
    assert response.is_json
    assert response.json["code"] == "INTERNAL_ERROR" 


def test_integration_psm_unexpected_error_500(client, monkeypatch):
    """
    Teste la gestion d'une erreur inattendue levée par le client PSM (ex: bug interne non classifié).
    Le Triangulator doit gérer cette exception non gérée et répondre 500.
    """
    def mock_get_psm_exception(_id):
        raise Exception("Erreur réseau ou parsing imprévue")

    monkeypatch.setattr("src.triangulator.client_psm.get_pointset_bytes", mock_get_psm_exception)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 500
    assert response.is_json
    assert response.json["code"] == "INTERNAL_ERROR"

import struct

import pytest
from src.triangulator.app import create_app
from src.triangulator.client_psm import PointSetManagerUnavailable, PointSetNotFound

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
    """Teste le scénario nominal complet.
    """
    def mock_get_psm_success(_id):
        return MOCK_POINTSET_BIN 
    
    def mock_triangulate_success(_data):
        return [(0, 1, 2)] 

    def mock_serialize_success(_points, _triangles):
        return MOCK_TRIANGLES_BIN

    monkeypatch.setattr("src.triangulator.service.get_pointset_bytes", 
                        mock_get_psm_success)
    monkeypatch.setattr("src.triangulator.service.triangulate_points", 
                        mock_triangulate_success)
    
    monkeypatch.setattr("src.triangulator.service.serialize_triangles", 
                        mock_serialize_success)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 200
    assert response.data == MOCK_TRIANGLES_BIN


def test_integration_not_found_404(client, monkeypatch):
    """Teste la gestion d'une erreur 404 reçue du PointSetManager.
    Le Triangulator doit intercepter l'exception PointSetNotFound et répondre 404.
    """
    def mock_get_psm_404(_id):
        raise PointSetNotFound("PointSet ID non trouvé")

    monkeypatch.setattr("src.triangulator.service.get_pointset_bytes", mock_get_psm_404)

    response = client.get(f"/triangulation/{NOT_FOUND_ID}")

    assert response.status_code == 404
    assert response.is_json
    assert response.json["code"] == "NOT_FOUND"


def test_integration_service_unavailable_503(client, monkeypatch):
    """Teste la gestion d'une indisponibilité du PointSetManager
    Le Triangulator doit intercepter l'exception PointSetManagerUnavailable 
    et répondre 503.
    """
    def mock_get_psm_503(_id):
        raise PointSetManagerUnavailable("PSM inaccessible ou en panne")

    monkeypatch.setattr("src.triangulator.service.get_pointset_bytes", mock_get_psm_503)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 503
    assert response.is_json
    assert response.json["code"] == "SERVICE_UNAVAILABLE"


def test_integration_internal_algorithm_failure_500(client, monkeypatch):
    """Teste le cas où l'algorithme de triangulation lève une erreur interne.
    Le Triangulator doit intercepter l'erreur et répondre 500.
    """
    def mock_get_psm_success(_id):
        return MOCK_POINTSET_BIN
    
    def mock_triangulate_failure(_data):
        raise ValueError("Erreur de calcul interne non gérée")

    monkeypatch.setattr("src.triangulator.service.get_pointset_bytes", 
                        mock_get_psm_success)
    monkeypatch.setattr("src.triangulator.service.triangulate_points", 
                        mock_triangulate_failure)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 500
    assert response.is_json
    assert response.json["code"] == "INTERNAL_ERROR" 


def test_integration_psm_unexpected_error_500(client, monkeypatch):
    """Teste la gestion d'une erreur inattendue levée par le client PSM .
    Le Triangulator doit gérer cette exception non gérée et répondre 500.
    """
    def mock_get_psm_exception(_id):
        raise Exception("Erreur réseau ou parsing imprévue")

    monkeypatch.setattr("src.triangulator.service.get_pointset_bytes", 
                        mock_get_psm_exception)

    response = client.get(f"/triangulation/{POINT_SET_ID}")

    assert response.status_code == 500
    assert response.is_json
    assert response.json["code"] == "INTERNAL_ERROR"



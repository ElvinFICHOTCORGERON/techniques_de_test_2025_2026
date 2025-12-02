# Fichier: src/triangulator/service.py
from .core import deserialize_pointset, triangulate_points, serialize_triangles
from .client_psm import get_pointset_bytes

def process_triangulation_request(pointset_id: str) -> bytes:
    """
    Exécute le workflow complet : récupération, calcul, et sérialisation.
    """
    pointset_bin = get_pointset_bytes(pointset_id)
    
    points = deserialize_pointset(pointset_bin)
    
    triangles = triangulate_points(points)
    
    triangles_bin = serialize_triangles(points, triangles)
    
    return triangles_bin
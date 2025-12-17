from .client_psm import get_pointset_bytes
from .core import deserialize_pointset, serialize_triangles, triangulate_points
from .execption import TriangulatorError


def process_triangulation_request(pointset_id: str) -> bytes:
    """Exécute le workflow complet : récupération, calcul, et sérialisation.
    """
    pointset_bin = get_pointset_bytes(pointset_id)
    
    try:
        points = deserialize_pointset(pointset_bin)
    except TriangulatorError as e:
        raise TriangulatorError(
            f"Échec de la désérialisation du PointSet: {e}"
        ) from e
    
    try:
        triangles = triangulate_points(points)
    except TriangulatorError as e:
        raise e 
    except Exception as e:
        raise TriangulatorError(
            f"Échec critique de l'algorithme de triangulation: {e}"
        ) from e
    
    triangles_bin = serialize_triangles(points, triangles)
    
    return triangles_bin
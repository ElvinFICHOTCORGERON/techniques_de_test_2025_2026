import struct
import math
from .exceptions import InvalidBinaryFormat, InsufficientPointsError

PSM_BASE_URL = "http://point-set-manager-service:8080" 

# Fonctions de sérialisation/désérialisation
def deserialize_pointset(data: bytes) -> list[tuple[float, float]]:
    """Convertit les données binaires PointSet en liste de tuples (X, Y)."""
    raise NotImplementedError()

def serialize_triangles(points: list, triangles: list) -> bytes:
    """Convertit la liste de points et d'indices de triangles en format binaire Triangles."""
    raise NotImplementedError()

def triangulate_points(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Calcule la triangulation (Delaunay ou autre) et retourne une liste de triplets d'indices."""
    if len(points) < 3:
        raise InsufficientPointsError("Moins de 3 points fournis pour la triangulation.")
        
    raise NotImplementedError()
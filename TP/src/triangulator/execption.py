class TriangulatorError(Exception):
    """Classe de base pour toutes les exceptions du Triangulator."""
    pass


class InvalidBinaryFormat(TriangulatorError, ValueError):
    """Levée si les données binaires PointSet ou Triangles sont mal formées ou incomplètes."""
    pass

class InsufficientPointsError(TriangulatorError, ValueError):
    """Levée si la triangulation est demandée avec moins de 3 points."""
    pass


class PointSetNotFound(TriangulatorError):
    """Levée lorsque le PointSetManager retourne une erreur 404 (ID non trouvé)."""
    pass

class PointSetManagerUnavailable(TriangulatorError):
    """Levée en cas d'erreur réseau ou si le PointSetManager retourne 503/5xx."""
    pass
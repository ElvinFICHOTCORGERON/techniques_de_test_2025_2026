import io
import struct

from .execption import InsufficientPointsError, InvalidBinaryFormat

PSM_BASE_URL = "http://point-set-manager-service:8080" 

def deserialize_pointset(data: bytes) -> list[tuple[float, float]]:
    """Convertit les données binaires PointSet en liste de tuples (X, Y)."""
    HEADER_SIZE = 4
    POINT_SIZE = 8 

    if len(data) < HEADER_SIZE:
        raise InvalidBinaryFormat(
            "Données PointSet trop courtes pour l'en-tête."
        )
    try:
        num_points = struct.unpack('<I', data[:HEADER_SIZE])[0]
    except struct.error:
        raise InvalidBinaryFormat(
            "Impossible de lire le nombre de points dans l'en-tête."
        ) from struct.error

    expected_data_size = num_points * POINT_SIZE
    
    if len(data) != HEADER_SIZE + expected_data_size:
        raise InvalidBinaryFormat(
            "Taille du binaire incohérente avec le nombre de points déclaré."
        )
    
    points = []
    
    for i in range(num_points):
        offset = HEADER_SIZE + i * POINT_SIZE
        x, y = struct.unpack('<ff', data[offset:offset + POINT_SIZE])
        points.append((x, y))
        
    return points

def serialize_triangles(points: list, triangles: list) -> bytes:
    """Convertit la liste de points et d'indices de triangles
    en format binaire Triangles.
    """
    buffer = io.BytesIO()
    
    num_points = len(points)
    buffer.write(struct.pack('<I', num_points))
    
    for x, y in points:
        buffer.write(struct.pack('<ff', x, y))
    
    num_triangles = len(triangles)
    buffer.write(struct.pack('<I', num_triangles))
    
    max_index = num_points - 1
    
    for i1, i2, i3 in triangles:
        if (
            i1 > max_index or i2 > max_index or i3 > max_index or 
            i1 < 0 or i2 < 0 or i3 < 0
        ):
            raise InvalidBinaryFormat(
                "Indice de sommet hors limite dans la sérialisation des triangles."
            )
            
        buffer.write(struct.pack('<III', i1, i2, i3))
        
    return buffer.getvalue()

def is_collinear(p1, p2, p3, epsilon=1e-9):
    """Vérifie si trois points sont colinéaires (standard library only)."""
    val = abs(p1[0] * (p2[1] - p3[1]) + 
              p2[0] * (p3[1] - p1[1]) + 
              p3[0] * (p1[1] - p2[1]))
    return val < epsilon

def get_circumcircle(p1, p2, p3):
    """Calcule le centre et le rayon au carré du cercle circonscrit à 3 points."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(D) < 1e-9:
        return None, float('inf')

    ux = (
    (x1**2 + y1**2) * (y2 - y3) + 
    (x2**2 + y2**2) * (y3 - y1) + 
    (x3**2 + y3**2) * (y1 - y2)
    ) / D
    uy = (
        (x1**2 + y1**2) * (x3 - x2) + 
        (x2**2 + y2**2) * (x1 - x3) + 
        (x3**2 + y3**2) * (x2 - x1)
    ) / D
    center = (ux, uy)
    radius_sq = (x1 - ux)**2 + (y1 - uy)**2
    return center, radius_sq

def triangulate_points(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Calcule la triangulation de Delaunay via l'algorithme de Bowyer-Watson."""
    n = len(points)
    if n < 3:
        raise InsufficientPointsError("Moins de 3 points fournis.")

    # 1. Créer un "Super-Triangle" qui contient tous les points
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    dx, dy = max_x - min_x, max_y - min_y
    delta = max(dx, dy)
    mid_x, mid_y = (min_x + max_x) / 2, (min_y + max_y) / 2

    # Points du super-triangle (indices fictifs n, n+1, n+2)
    st_points = [
        (mid_x - 20 * delta, mid_y - delta),
        (mid_x + 20 * delta, mid_y - delta),
        (mid_x, mid_y + 20 * delta)
    ]
    all_pts = points + st_points
    triangulation = [(n, n + 1, n + 2)]

    # 2. Insérer chaque point un par un
    for i, p in enumerate(points):
        bad_triangles = []
        for tri in triangulation:
            center, r_sq = get_circumcircle(
                all_pts[tri[0]], 
                all_pts[tri[1]], 
                all_pts[tri[2]])
            dist_sq = (p[0] - center[0])**2 + (p[1] - center[1])**2
            if dist_sq < r_sq:
                bad_triangles.append(tri)

        polygon = []
        for tri in bad_triangles:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            for edge in edges:
                is_shared = any(
                    all(e in other for e in edge) or 
                    all(e in other for e in edge[::-1])
                    for other in bad_triangles if other != tri
                )

                if not is_shared:
                    polygon.append(edge)

        for tri in bad_triangles:
            triangulation.remove(tri)

        for edge in polygon:
            triangulation.append((edge[0], edge[1], i))

    # 3. Nettoyage : retirer les triangles liés au super-triangle
    final_triangulation = []
    for tri in triangulation:
        if not any(idx >= n for idx in tri):
            final_triangulation.append(tri)

    return final_triangulation
Module src.triangulator.core
============================

Functions
---------

`deserialize_pointset(data: bytes) ‑> list[tuple[float, float]]`
:   Convertit les données binaires PointSet en liste de tuples (X, Y).

`get_circumcircle(p1, p2, p3)`
:   Calcule le centre et le rayon au carré du cercle circonscrit à 3 points.

`is_collinear(p1, p2, p3, epsilon=1e-09)`
:   Vérifie si trois points sont colinéaires (standard library only).

`serialize_triangles(points: list, triangles: list) ‑> bytes`
:   Convertit la liste de points et d'indices de triangles
    en format binaire Triangles.

`triangulate_points(points: list[tuple[float, float]]) ‑> list[tuple[int, int, int]]`
:   Calcule la triangulation de Delaunay via l'algorithme de Bowyer-Watson.
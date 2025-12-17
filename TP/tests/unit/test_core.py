import math
import struct

import pytest
from src.triangulator.core import (
    deserialize_pointset,
    serialize_triangles,
    triangulate_points,
)
from src.triangulator.execption import InsufficientPointsError, InvalidBinaryFormat


def test_deserialize_pointset_nominal_case():
    """Teste la désérialisation de 3 points valides avec vérification des flottants."""
    num_points_bin = struct.pack('<I', 3) 
    
    point_data_bin = struct.pack('<ff', 1.0, 2.0) + \
                     struct.pack('<ff', 3.5, 4.8) + \
                     struct.pack('<ff', -10.0, 0.0)
    
    binary_data = num_points_bin + point_data_bin
    
    expected_points = [(1.0, 2.0), (3.5, 4.8), (-10.0, 0.0)]
    
    actual_points = deserialize_pointset(binary_data) 

    for actual, expected in zip(actual_points, expected_points, strict=True):
        assert math.isclose(actual[0], expected[0], rel_tol=1e-5)
        assert math.isclose(actual[1], expected[1], rel_tol=1e-5)
    assert len(actual_points) == len(expected_points)


def test_deserialize_pointset_empty():
    """Teste la désérialisation d'un PointSet vide (N=0)."""
    binary_data = struct.pack('<I', 0) 
    
    actual_points = deserialize_pointset(binary_data) 
    
    assert actual_points == []


def test_deserialize_pointset_truncated_header():
    """Teste l'échec si le binaire est plus court que la taille de l'en-tête."""
    binary_data = b'\x01\x00\x00'
    
    with pytest.raises(InvalidBinaryFormat):
        deserialize_pointset(binary_data)


def test_deserialize_pointset_truncated_data():
    """Teste l'échec si la taille des données de points ne correspond pas au compte."""
    num_points_bin = struct.pack('<I', 3) 
    
    point1_bin = struct.pack('<ff', 1.0, 2.0)
    
    binary_data = num_points_bin + point1_bin 
    
    with pytest.raises(InvalidBinaryFormat):
        deserialize_pointset(binary_data)


def test_serialize_triangles_single_triangle():
    """Teste la sérialisation d'un PointSet de 3 points résultant en 1 triangle.
    Vérifie la conformité du format binaire Triangles.
    """
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    
    vertices_header = struct.pack('<I', 3)
    vertices_data = struct.pack('<ff', 0.0, 0.0) + \
                    struct.pack('<ff', 1.0, 0.0) + \
                    struct.pack('<ff', 0.0, 1.0)
    
    triangles_header = struct.pack('<I', 1)
    triangles_data = struct.pack('<III', 0, 1, 2)
    
    expected_binary = (
        vertices_header + vertices_data + 
        triangles_header + triangles_data
    )
    
    actual_binary = serialize_triangles(points, triangles)
    
    assert actual_binary == expected_binary


def test_serialize_triangles_empty_set():
    """Teste la sérialisation d'un PointSet vide (N=0) et sans triangles (T=0)."""
    points = []
    triangles = []
    
    expected_binary = struct.pack('<I', 0) + struct.pack('<I', 0)
    
    actual_binary = serialize_triangles(points, triangles)
    
    assert actual_binary == expected_binary


def test_serialize_triangles_invalid_index():
    """Teste l'échec de sérialisation si un indice de triangle est hors limites."""
    points = [(0.0, 0.0), (1.0, 0.0)] 
    triangles = [(0, 1, 5)] 
    
    with pytest.raises(InvalidBinaryFormat):
        serialize_triangles(points, triangles)


def test_triangulate_points_simple_triangle():
    """Teste le cas le plus simple : 3 points non colinéaires (résultat unique)."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    
    actual_triangles = triangulate_points(points) 
    expected_triangles = [(0, 1, 2)]
    
    assert sorted(actual_triangles[0]) == sorted(expected_triangles[0])
    assert len(actual_triangles) == 1


def test_triangulate_points_square_two_triangles():
    """Teste un cas simple de 4 points (carré) qui doit être décomposé en 2 triangles"""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)] 
    
    actual_triangles = triangulate_points(points) 
    
    assert len(actual_triangles) == 2
    
    indices_utilises = set(sum(actual_triangles, ()))
    assert indices_utilises == {0, 1, 2, 3}


def test_triangulate_points_collinear_failure():
    """Teste la gestion des points colinéaires (ne peuvent pas former de surface)."""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)] 
    
    actual_triangles = triangulate_points(points)
    assert actual_triangles == [] 


def test_triangulate_points_insufficient_points():
    """Teste l'échec si le nombre de points est inférieur à 3 (condition minimale)."""
    points_too_few = [(0.0, 0.0), (1.0, 1.0)]
    
    with pytest.raises(InsufficientPointsError):
        triangulate_points(points_too_few)


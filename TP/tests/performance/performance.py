Python

import pytest
import time
import struct
import math
import random
from src.triangulator.core import (
    deserialize_pointset, 
    triangulate_points, 
    serialize_triangles
)

N_SMALL = 100
N_LARGE = 10000 
ITERATIONS = 5


@pytest.fixture(scope="module")
def random_point_set(num_points):
    """Génère une liste de num_points tuples (X, Y)."""
    return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(num_points)]


@pytest.fixture(scope="function")
def timer():
    """Fournit une fonction pour mesurer le temps d'exécution d'une callback."""
    def measure_time(func, *args, **kwargs):
        times = []
        for _ in range(ITERATIONS):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        return sum(times) / ITERATIONS
    return measure_time


def generate_binary_pointset(points):
    """Crée un PointSet binaire à partir d'une liste de points."""
    num_points = len(points)
    header = struct.pack('<I', num_points)
    data = b''
    for x, y in points:
        data += struct.pack('<ff', x, y)
    return header + data

@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_deserialization(num_points, random_point_set, timer):
    """Mesure la performance de la conversion binaire vers la structure interne."""
    points = random_point_set(num_points)
    binary_data = generate_binary_pointset(points)
    
    def run_deserialization():
        deserialize_pointset(binary_data)
        
    avg_time = timer(run_deserialization)
    
    print(f"\n[DESERIALIZATION] N={num_points}: {avg_time:.6f} secondes (moyenne sur {ITERATIONS} itérations)")
    
    assert avg_time > 0 


@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_triangulation(num_points, random_point_set, timer):
    """
    Mesure la performance de l'algorithme de triangulation pure.
    C'est le test le plus critique pour la complexité.
    """
    points = random_point_set(num_points)
    
    def run_triangulation():
        triangulate_points(points)
        
    avg_time = timer(run_triangulation)
    
    print(f"\n[TRIANGULATION] N={num_points}: {avg_time:.6f} secondes (moyenne sur {ITERATIONS} itérations)")
    
    assert avg_time > 0


@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_serialization(num_points, random_point_set, timer):
    """
    Mesure la performance de la conversion de la structure interne (Points + Triangles) 
    vers le format binaire Triangles final.
    """
    points = random_point_set(num_points)
    
    triangles_mock = [(random.randint(0, num_points-1), 
                       random.randint(0, num_points-1), 
                       random.randint(0, num_points-1)) 
                      for _ in range(num_points * 2)]
    
    def run_serialization():
        serialize_triangles(points, triangles_mock)
        
    avg_time = timer(run_serialization)
    
    print(f"\n[SERIALIZATION] N={num_points}: {avg_time:.6f} secondes (moyenne sur {ITERATIONS} itérations)")
    
    assert avg_time > 0
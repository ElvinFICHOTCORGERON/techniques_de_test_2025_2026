import random
import struct
import time

import pytest
from src.triangulator.core import (
    deserialize_pointset,
    serialize_triangles,
    triangulate_points,
)

N_SMALL = 100
N_LARGE = 2000
ITERATIONS = 5

def get_random_point_set(num_points):
    """Génère une liste de num_points tuples (X, Y)."""
    return [
        (random.uniform(0, 1000), random.uniform(0, 1000)) 
        for _ in range(num_points)
    ]

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
    data = b''.join(struct.pack('<ff', x, y) for x, y in points)
    return header + data

@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_deserialization(num_points, timer):
    points = get_random_point_set(num_points)
    binary_data = generate_binary_pointset(points)
    
    avg_time = timer(lambda: deserialize_pointset(binary_data))
    
    print(f"\n[DESERIALIZATION] N={num_points}: {avg_time:.6f}s")
    assert avg_time > 0 

@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_triangulation(num_points, timer):
    points = get_random_point_set(num_points)
    
    avg_time = timer(lambda: triangulate_points(points))
    
    print(f"\n[TRIANGULATION] N={num_points}: {avg_time:.6f}s")
    assert avg_time >= 0 

@pytest.mark.performance
@pytest.mark.parametrize("num_points", [N_SMALL, N_LARGE])
def test_perf_serialization(num_points, timer):
    points = get_random_point_set(num_points)
    triangles_mock = [(random.randint(0, num_points-1), 
                       random.randint(0, num_points-1), 
                       random.randint(0, num_points-1)) 
                      for _ in range(num_points * 2)]
    
    avg_time = timer(lambda: serialize_triangles(points, triangles_mock))
    
    print(f"\n[SERIALIZATION] N={num_points}: {avg_time:.6f}s")
    assert avg_time > 0
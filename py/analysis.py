
from data_model import Particle, Step

from sklearn.neighbors import NearestNeighbors
import numpy as np

def calculate_degree_of_mixing(step: Step, k: int):
    if len(step.particles) < k:
        return 0
    positions = [(particle.x, particle.y) for particle in step.particles]
    types = [particle.type for particle in step.particles]

    nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(positions)
    distances, indices = nbrs.kneighbors(positions)

    similar_counts = 0
    total_counts = 0

    for i, neighbors in enumerate(indices):
        # Exclude the first neighbor since it's the point itself
        neighbor_types = [types[j] for j in neighbors[1:]]
        total_counts += k-1
        similar_counts += np.sum(np.array(neighbor_types) == types[i])

    ratio = similar_counts / total_counts
    degree_of_mixing = 1 - abs(ratio - 0.5) / 0.5
    return degree_of_mixing
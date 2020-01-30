"""Implements the Manna model."""

from SOC import common
import numpy as np
import numba
import random

class Manna(common.Simulation):
    """Implements the Manna model."""
    
    def __init__(self, critical_value: int = 1, abelian: bool = True, *args, **kwargs):
        """
        :param L: linear size of lattice, without boundary layers
        :type L: int
        :param critical_value: 1 by default - above this value, nodes start toppling
        :type critical_value: int
        :param abelian: True by default - abelian, False - nonabelian
        :type abelian: bool
        """
        super().__init__(*args, **kwargs)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        self.critical_value = critical_value
        self.abelian = abelian

    def drive(self, num_particles: int = 1):
        """
        Drive the simulation by adding particles from the outside.

        :param num_particles: How many particles to add per iteration (by default, 1)
        :type num_particles: int
        """
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary-1, size = (num_particles, 2))
        for x, y in location:
            self.values[x, y] += 1

    def topple_dissipate(self, i) -> bool:
        """
        Distribute material from overloaded sites to neighbors.

        Convenience wrapper for the numba.njitted `topple_dissipate` function defined in `manna.py`.

        :rtype: bool
        """
        return topple_dissipate(self.values, self.visited, self.critical_value, self.abelian, self.BOUNDARY_SIZE)

_DEBUG = True

@numba.njit
def topple_dissipate(values: np.ndarray, visited: np.ndarray, critical_value: int, abelian: bool, boundary_size: int) -> bool:

    """
    Distribute material from overloaded sites to neighbors.

    Returns True/False: should we continue checking if something needs toppling?

    :param values: data array of the simulation
    :type values: np.ndarray
    :param visited: boolean array, needs to be cleaned beforehand
    :type visited: np.ndarray
    :param critical_value: nodes topple above this value
    :type critical_value: int
    :param abelian: True by default - abelian, False - nonabelian
    :type abelian: bool
    :param boundary_size: size of boundary for the array
    :type boundary_size: int
    :rtype: bool
    """

    number_of_topple_iterations = 0
    # find a boolean array of active (overloaded) sites
    active_sites = common.clean_boundary_inplace(values > critical_value, boundary_size)   # TODO speedup?
    # odrzucam 

    while active_sites.any():   # TODO speedup?
        indices = np.vstack(np.where(active_sites)).T   # TODO speedup?
        # a Nx2 array of integer indices for overloaded sites
        N = indices.shape[0]

        for i in range(N):
            x, y = index = indices[i]

            if _DEBUG:
                width, height = values.shape
                assert boundary_size <= x < width
                assert boundary_size <= y < width
                assert values[x, y] >= 0

            if abelian:
                n_to_distribute = 2           # number of particles to distribute from the active site
                values[x, y] -= 2
            else:
                n_to_distribute = values[x, y]
                values[x, y] = 0
            
            # randomly and independently pick neighbors of the current site
            neighbors = index + np.random.choice(np.array((-1, 1)), # ugly but numba broke otherwise
                                                 size=(n_to_distribute, 2))   # TODO speedup?
            # to byśmy podmieniali gdybyśmy zmieniali model najbliższych sąsiadów

            for j in range(len(neighbors)):
                xn, yn = neighbors[j]
                values[xn, yn] += 1
                visited[xn, yn] = True
            
        number_of_topple_iterations += 1
        active_sites = common.clean_boundary_inplace(values > critical_value, boundary_size)
    # dissipate would be here, after the while loop
    # but it's not necessary so we skip it
    return number_of_topple_iterations


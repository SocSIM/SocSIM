"""Implements the Manna model."""

from SOC import common
import numpy as np
import numba
import random

class Manna(common.Simulation):
    """Implements the Manna model."""
    
    def __init__(self, L: int, critical_value: int = 1, model_variant: int = 0):
        """
        :param L: linear size of lattice, without boundary layers
        :type L: int
        :param critical_value: 1 by default - above this value, nodes start toppling
        :type critical_value: int
        :param model_variant: 0 by default - abelian, 1 - nonabelian
        :type model_variant: int
        """
        super().__init__(L)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        self.critical_value = critical_value
        self.model_variant = model_variant
    def drive(self, num_particles: int = 1):
        """
        Drive the simulation by adding particles from the outside.

        :param num_particles: How many particles to add per iteration (by default, 1)
        :type num_particles: int
        """
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary-1, size = (num_particles, 2))
        for x, y in location:
            self.values[x, y] += 1

    def topple(self) -> bool:
        """
        Distribute material from overloaded sites to neighbors.

        Convenience wrapper for the numba.njitted `topple` function defined in `manna.py`.

        :rtype: bool
        """
        return topple(self.values, self.visited, self.critical_value, self.model_variant, self.BOUNDARY_SIZE)

    def dissipate(self):
        """Does nothing, dissipation is handled by the added boundary strips"""
        pass

_DEBUG = True

# @numba.njit
def topple(values: np.ndarray, visited: np.ndarray, critical_value: int, model_variant: int, boundary_size: int) -> bool:
    """
    Distribute material from overloaded sites to neighbors.

    Returns True/False: should we continue checking if something needs toppling?

    :param values: data array of the simulation
    :type values: np.ndarray
    :param visited: boolean array, needs to be cleaned beforehand
    :type visited: np.ndarray
    :param critical_value: nodes topple above this value
    :type critical_value: int
    :param boundary_size: size of boundary for the array
    :type boundary_size: int
    :rtype: bool
    """

    # find a boolean array of active (overloaded) sites
    active_sites = common.clean_boundary_inplace(values > critical_value, boundary_size)

    print(active_sites)
    print(values)
    if active_sites.any():
        indices = np.vstack(np.where(active_sites)).T
        # a Nx2 array of integer indices for overloaded sites
        N = indices.shape[0]

        for i in range(N):
            x, y = index = indices[i]
            
            if _DEBUG:
                width, height = values.shape
                assert boundary_size <= x < width
                assert boundary_size <= y < width
                assert values[x, y] >= 0
            print(values[x, y])
            if(model_variant==0):
                n_to_distribute = 2           # number of particles to distribute from the active site
                values[x, y] -= 2
            elif(model_variant==1):
                n_to_distribute = values[x, y]
                values[x, y] = 0

            # randomly and independently pick neighbors of the current site
            neighbors = index + np.random.choice(np.array((-1, 1)), # ugly but numba broke otherwise
                                                 size=(n_to_distribute, 2))
            
            print(values[x, y], index, neighbors)
            for j in range(len(neighbors)):
                xn, yn = neighbors[j]
                values[xn, yn] += 1
                visited[xn, yn] = True
        return True
    else:
        return False # nothing happened, we can stop toppling


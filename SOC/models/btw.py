"""Contains the base class for the simulation of abelian sandpile model.""" 
from SOC import common
import numpy as np
from tqdm import auto as tqdm
import numba
import matplotlib.pyplot as plt


class BTW(common.Simulation):
    """Implements the BTW model."""
    def __init__(self, *args, **kwargs):
        """
        :param L: linear size of lattice, without boundary layers
        :type L: int
        """
        super().__init__(*args, **kwargs)
        self.d = 2 #lattice dimmension 
        self.q = 2*self.d #grains amount used at driving 
        self.z_c = self.q - 1 #critical slope
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)

    def adjacent_indexes(self, x, y):
        """
        Evaluates adjacent indexes to (x, y). Clockwise order,
        starting from left.
        """
        # TODO rise error if x,y are out of boundaries
        return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]


    def drive(self, num_particles: int = 1):
        """
        Drive the simulation by adding particles from the outside.

        :param num_particles: How many particles to add per iteration (by default, 1)
        :type num_particles: int
        """
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary - 1, size = (num_particles, 2))
        for x, y in location:
            self.values[x, y] += 1

    def topple_dissipate(self) -> int:
        """
        Distribute material from overloaded sites to neighbors.

        Convenience wrapper for the numba.njitted `topple` function defined in `manna.py`.

        :rtype: int
        """

        return topple(self.values, self.visited, self.releases, self.z_c, self.BOUNDARY_SIZE)    



@numba.njit
def topple(values: np.ndarray, visited: np.ndarray, releases: np.ndarray, critical_value: int, boundary_size: int) -> int:
    """
    Distribute material from overloaded sites to neighbors.

    Returns True/False: should we continue checking if something needs toppling?

    :param values: data array of the simulation
    :type values: np.ndarray
    :param visited: boolean array, needs to be cleaned beforehand
    :type visited: np.ndarray
    :param releases: boolean array, used to evalute number of sandpiles activations
    :type releases: np.ndarray
    :param critical_value: nodes topple above this value
    :type critical_value: int
    :param boundary_size: size of boundary for the array
    :type boundary_size: int
    :rtype: int
    """

    # find a boolean array of active (overloaded) sites
    number_of_iterations = 0
    active_sites = common.clean_boundary_inplace(values > critical_value, boundary_size)
    
    while active_sites.any():
        releases += active_sites
        
        indices = np.vstack(np.where(active_sites)).T
        # a Nx2 array of integer indices for overloaded sites

        N = indices.shape[0]
        for i in range(N):
            x, y = indices[i]
            values[x, y] -= critical_value + 1 # zależy od parametru?

            neighbors = np.array([(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)])
            for j in range(len(neighbors)):
                xn, yn = neighbors[j]
                values[xn, yn] += 1
                visited[xn, yn] = True
        
        number_of_iterations += 1

        active_sites = common.clean_boundary_inplace(values > critical_value, boundary_size)

    return number_of_iterations

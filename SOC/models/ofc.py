"""Implements the OFC model."""

from SOC import common
import numpy as np
import numba
import random

class OFC(common.Simulation):
    """Implements the OFC model."""
    
    def __init__(self, L: int, critical_value: float = 1., conservation_lvl: float = 0.25):
        """
        :param L: linear size of lattice, without boundary layers
        :type L: int
        :param critical_value: 1.0 by default - above this value, nodes start toppling
        :type critical_value: float
        :param conservation_lvl: 0.25 by default - fraction of the force from a toppling site going to its neighbour   # 0.25 -> full force distributed (if 4 neighbours)
        :type conservation_lvl: float
        """
        super().__init__(L)
        self.critical_value = critical_value
        self.values = np.random.rand(self.L_with_boundary, self.L_with_boundary) * self.critical_value
        self.conservation_lvl = conservation_lvl
        
    def drive(self):
        """
        Drive the simulation by adding force from the outside.

        """
        location_of_max = np.unravel_index(np.argmax(self.values, axis=None), self.values.shape)
        
        self.values += self.critical_value - self.values[location_of_max]
        
    def topple(self) -> bool:
        """
        Distribute material from overloaded sites to neighbors.

        Convenience wrapper for the numba.njitted `topple` function defined in `manna.py`.

        :rtype: bool
        """
        return topple(self.values, self.visited, self.critical_value, self.conservation_lvl, self.BOUNDARY_SIZE)

    def dissipate(self):
        """Does nothing, dissipation is handled by the added boundary strips"""
        pass

_DEBUG = True

# @numba.njit
def topple(values: np.ndarray, visited: np.ndarray, critical_value: float, conservation_lvl: float, boundary_size: int) -> bool:
    """
    Distribute material from overloaded sites to neighbors.

    Returns True/False: should we continue checking if something needs toppling?

    :param values: data array of the simulation
    :type values: np.ndarray
    :param visited: boolean array, needs to be cleaned beforehand
    :type visited: np.ndarray
    :param critical_value: nodes topple above this value
    :type critical_value: float
    :param conservation_lvl: 0.25 by default - fraction of the force from a toppling site going to its neighbour   # 0.25 -> full force distributed
    :type conservation_lvl: float
    :param boundary_size: size of boundary for the array
    :type boundary_size: int
    :rtype: bool
    """

    # find a boolean array of active (overloaded) sites
    active_sites = common.clean_boundary_inplace(values >= 1., boundary_size)         #najpewniej będzie warunek values>=critical_value

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


            neighbors = index + np.array([[0, 1], [-1, 0], [1, 0], [0,-1]])

            for j in range(len(neighbors)):
                xn, yn = neighbors[j]
                values[xn, yn] += conservation_lvl * values[x, y]
                visited[xn, yn] = True

            values[x, y] = 0.
            
        return True
    else:
        return False # nothing happened, we can stop toppling


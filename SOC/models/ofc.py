"""Implements the OFC model."""


# TODO Partial Stress Drop
# TODO Crack model

from SOC import common
import numpy as np
import numba
import random


class OFC(common.Simulation):
    """Implements the OFC model."""

    def __init__(self, critical_value: float = 1., conservation_lvl: float = 0.25, *args, **kwargs):
        """
        :param L: linear size of lattice, without boundary layers
        :type L: int
        :param critical_value: 1.0 by default - above this value, nodes start toppling
        :type critical_value: float
        # 0.25 -> full force distributed (if 4 neighbours)
        :param conservation_lvl: 0.25 by default - fraction of the force from a toppling site going to its neighbour
        :type conservation_lvl: float
        """
        super().__init__(*args, **kwargs)
        self.critical_value = critical_value
        self.values = np.random.rand(
            self.L_with_boundary, self.L_with_boundary) * self.critical_value
        self.conservation_lvl = conservation_lvl

        self.critical_value_current = self.critical_value

    def drive(self):
        """
        Drive the simulation by adding force from the outside.

        """

        # decreasing critical_value to the max_value
        max_value = np.max(self.values[self.BC:-self.BC, self.BC:-self.BC])
        self.critical_value_current = max_value

        # TODO MAYBE random loading vs obecnie zrobiony homogeneous loading?

        # TODO lista kandydatów do pękania?

    def topple_dissipate(self) -> int:
        """
        Distribute material from overloaded sites to neighbors.

        Convenience wrapper for the numba.njitted `topple` function defined in `ofc.py`.

        :rtype: int
        """
        return topple(self.values, self.visited, self.releases, self.critical_value_current, self.critical_value, self.conservation_lvl, self.BC)

    def _save_snapshot(self, i):
        self.saved_snapshots[i // self.save_every] = self.values - \
            self.critical_value_current


_DEBUG = True


@numba.njit
def topple(values: np.ndarray, visited: np.ndarray, releases: np.ndarray, critical_value_current: float, critical_value: float, conservation_lvl: float, boundary_size: int) -> int:
    """
    Distribute material from overloaded sites to neighbors.

    Returns True/False: should we continue checking if something needs toppling?

    :param values: data array of the simulation
    :type values: np.ndarray
    :param visited: boolean array, needs to be cleaned beforehand
    :type visited: np.ndarray
    :param critical_value: nodes topple above this value
    :type critical_value: float
    # 0.25 -> full force distributed
    :param conservation_lvl: 0.25 by default - fraction of the force from a toppling site going to its neighbour
    :type conservation_lvl: float
    :param boundary_size: size of boundary for the array
    :type boundary_size: int
    :rtype: int
    """

    # find a boolean array of active (overloaded) sites

    active_sites = common.clean_boundary_inplace(
        values >= critical_value_current, boundary_size)
    number_of_iterations = 0

    while active_sites.any():
        
        releases += active_sites
        indices = np.vstack(np.where(active_sites)).T
          # a Nx2 array of integer indices for overloaded sites
        N = indices.shape[0]
        for i in range(N):
            x, y = index = indices[i]
            if _DEBUG:
                width, height = values.shape
                assert boundary_size <= x < width
                assert boundary_size <= y < width
            neighbors = index + np.array([[0, 1], [-1, 0], [1, 0], [0,-1]])
              # TODO crack model nie wraca do sąsiadów, którzy już releasowali energię
            for j in range(len(neighbors)):
                xn, yn = neighbors[j]
                values[xn, yn] += conservation_lvl * (values[x, y] - critical_value_current + critical_value)   # Grassberger (1994), eqns (1)
                visited[xn, yn] = True

            values[x, y] = critical_value_current - critical_value  # Grassberger (1994), eqns (1)
            active_sites = common.clean_boundary_inplace(values >= critical_value_current, boundary_size)
        number_of_iterations += 1

    return number_of_iterations

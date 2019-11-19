"""Contains the base class for the simulation."""
import numpy as np
from tqdm import auto as tqdm
import numba
import matplotlib.pyplot as plt
import pandas
import seaborn

class Simulation:
    """Base class for SOC simulations."""
    values = NotImplemented
    BOUNDARY_SIZE = 1
    def __init__(self, L: int):
        """

        :param L: linear size of lattice, without boundary layers
        :type L: int
        """
        self.L = L
        self.L_with_boundary = L + 2 * self.BOUNDARY_SIZE
        self.size = L * L
        self.visited = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=bool)
        self.data_acquisition = []

    def drive(self):
        """
        Drive the simulation by adding particles from the outside.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the drive method!")

    def topple(self):
        """
        Distribute material from overloaded sites to neighbors.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the topple method!")

    def dissipate(self):
        """
        Handle losing material at boundaries.

        This may be removed in the future.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the dissipate method!")

    @classmethod
    def clean_boundary_inplace(cls, array: np.ndarray) -> np.ndarray:
        """
        Convenience wrapper to `clean_boundary_inplace` with the simulation's boundary size. 

        :param array:
        :type array: np.ndarray
        :rtype: np.ndarray
        """
        return clean_boundary_inplace(array, self.BOUNDARY_SIZE)

    def AvalancheLoop(self) -> dict:
        """
        Bring the current simulation's state to equilibrium by repeatedly
        toppling and dissipating.

        Returns a dictionary with the total size of the avalanche
        and the number of iterations the avalanche took.

        :rtype: dict
        """
        number_of_iterations = 0 # TODO rename number_of_topples/czas rozsypywania/duration
        self.visited[...] = False
        while self.topple():
            self.dissipate()
            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum()
        return dict(AvalancheSize=AvalancheSize, number_of_iterations=number_of_iterations)

    def run(self, N_iterations: int) -> dict:
        """
        Simulation loop. Drives the simulation, possibly starts avalanches, gathers data.

        :param N_iterations:
        :type N_iterations: int
        :rtype: dict
        """
        for i in tqdm.trange(N_iterations):
            self.drive()
            observables = self.AvalancheLoop()
            self.data_acquisition.append(observables)

    def plot_histograms(self, filename = None):
        df = pandas.DataFrame(self.data_acquisition)
        fig, axes = plt.subplots(len(df.columns))
        fig.suptitle(self.__class__.__name__)
        for i, column in enumerate(df.columns):
            ax = axes[i]
            seaborn.countplot(x=column, data=df, ax=ax)
            ax.set_yscale('log')
        if filename is not None:
            fig.savefig(filename)
        plt.show()

    def plot_state(self, with_boundaries = False):
        """
        Plots the current state of the simulation.
        """
        fig, ax = plt.subplots()
        if with_boundaries:
            values = self.values
        else:
            values = self.values[self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE, self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE]
        IM = ax.imshow(values, interpolation='nearest')
        plt.colorbar(IM)
        return fig
        
@numba.njit
def clean_boundary_inplace(array: np.ndarray, boundary_size: int, fill_value = False) -> np.ndarray:
    """
    Fill `array` at the boundary with `fill_value`.

    Useful to make sure sites on the borders do not become active and don't start toppling.

    Works inplace - will modify the existing array!

    :param array:
    :type array: np.ndarray
    :param boundary_size:
    :type boundary_size: int
    :param fill_value:
    :rtype: np.ndarray
    """
    array[:boundary_size, :] = fill_value
    array[-boundary_size:, :] = fill_value
    array[:, :boundary_size] = fill_value
    array[:, -boundary_size:] = fill_value
    return array


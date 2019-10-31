import numpy as np
from tqdm import auto as tqdm
import numba
import matplotlib.pyplot as plt

class Simulation:
    """Base class for SOC simulations."""

    values = NotImplemented
    BOUNDARY_SIZE = 1
    def __init__(self, L):
        self.L = L
        self.L_with_boundary = L + 2 * self.BOUNDARY_SIZE
        self.size = L * L
        self.visited = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=bool)

    def drive(self):
        raise NotImplementedError   # definiowane w subklasach 
    def topple(self):
        raise NotImplementedError
    def Dissipation(self):     # można zrobić po prostu pierścionek wokół tablicy (L+2, L+2) i wszystkie sumy robić po wewnętrznej 
        raise NotImplementedError
    
    @classmethod
    def force_boundary_not_active(cls, array):
        return force_boundary_not_active(array, self.BOUNDARY_SIZE)

    def AvalancheLoop(self):
        raise NotImplementedError

    def run(self, N_iterations: int):
        data_acquisition = {}
        for i in tqdm.trange(N_iterations):
            self.drive()
            observables = self.AvalancheLoop()
            data_acquisition[i] = observables
        return data_acquisition

    def plot_state(self):
        fig, ax = plt.subplots()
        IM = ax.imshow(self.values, interpolation='nearest', cmap='binary')
        plt.colorbar(IM)
        return fig
        
@numba.njit
def force_boundary_not_active_inplace(array, BOUNDARY_SIZE):
    array[:BOUNDARY_SIZE, :] = False
    array[-BOUNDARY_SIZE:, :] = False
    array[:, :BOUNDARY_SIZE] = False
    array[:, -BOUNDARY_SIZE:] = False
    return array


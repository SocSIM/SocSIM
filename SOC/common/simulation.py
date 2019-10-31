import numpy as np
from tqdm import auto as tqdm

class Simulation:
    """Base class for SOC simulations."""

    values = NotImplemented
    BOUNDARY_SIZE = 1
    def __init__(self, L):
        self.L = L
        self.L_with_boundary = L + 2 * self.BOUNDARY_SIZE
        self.visited = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=bool)

    def Initialization(self):
        raise NotImplementedError
    def Driving(self):
        raise NotImplementedError   # definiowane w subklasach 
    def Toppling(self):
        raise NotImplementedError
    def Dissipation(self):     # można zrobić po prostu pierścionek wokół tablicy (L+2, L+2) i wszystkie sumy robić po wewnętrznej 
        raise NotImplementedError
    
    def AvalancheLoop(self):
        raise NotImplementedError

    def run(self, N_iterations: int):
        data_acquisition = {}
        for i in tqdm.trange(N_iterations):
            self.Driving()
            observables = self.AvalancheLoop()
            data_acquisition[i] = observables
        return data_acquisition
        


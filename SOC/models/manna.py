from SOC import common
import numpy as np
import numba
import random

class Manna(common.Simulation):
    def __init__(self, L, critical_value: int = 1):
        super().__init__(L)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        self.critical_value = critical_value

    def Driving(self, num_particles = 1):
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary-1, size = (num_particles, 2))
        for x, y in location:
            self.values[x, y] += 1

    def Toppling(self):
        return Toppling(self.values, self.visited, self.critical_value, self.BOUNDARY_SIZE)

    def in_equilibrium(self):
        raise NotImplementedError

    def Dissipation(self):
        """Does nothing, dissipation is handled by the added boundary strips"""
        pass

    def AvalancheLoop(self):
        number_of_iterations = 0
        self.visited[...] = False
        while self.Toppling():
            self.Dissipation()
            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum()
        return dict(AvalancheSize=AvalancheSize, number_of_iterations=number_of_iterations)


# @numba.njit
def Toppling(values, visited, critical_value, BOUNDARY_SIZE):
    width, height = values.shape
    active_sites = common.force_boundary_not_active_inplace(values > critical_value, BOUNDARY_SIZE)
    if active_sites.any():
        indices = np.vstack(np.where(active_sites)).T
        for i in range(len(indices)):
            index = indices[i]
            x, y = index
            assert BOUNDARY_SIZE <= x < width
            assert BOUNDARY_SIZE <= y < width
            values[index] -= 2
            assert (values[index] >= 0).all()
            neighbors = np.random.choice(np.array((-1, 1)), size=(2, 2)) + index
            for neighbor in range(2):
                values[neighbors[neighbor]] += 1
                visited[neighbors[neighbor]] = True
        return True
    else:
        return False


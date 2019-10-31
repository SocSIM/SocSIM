from SOC import common
import numpy as np

class Manna(common.Simulation):
    def __init__(self, L):
        super().__init__(L)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)

    def Driving(self, num_particles = 1):
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary, size = (num_particles, 2))
        self.values[location] += 1

    def Toppling(self):
        # jak są dwie to rozrzucamy losowo
        raise NotImplementedError # TODO

    def in_equilibrium(self):
        raise NotImplementedError

    def AvalancheLoop(self):
        number_of_iterations = 0
        while not self.in_equilibrium():
            self.Toppling()
            self.Dissipation()

            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum() # dla Manna
        return dict(AvalancheSize=AvalancheSize, number_of_iterations=number_of_iterations)

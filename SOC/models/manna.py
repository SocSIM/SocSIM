from SOC import common
import numpy as np

class Manna(common.Simulation):
    def __init__(self, L, critical_value: int = 1):
        super().__init__(L)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        self.critical_value = critical_value

    def Driving(self, num_particles = 1):
        location = np.random.randint(self.BOUNDARY_SIZE, self.L_with_boundary, size = (num_particles, 2))
        self.values[location] += 1

    def Toppling(self):
        active_sites = self.force_boundary_not_active(self.values > self.critical_value)
        X, Y = np.where(active_sites)
        for x, y in np.where(active_sites):
            self.values[x, y] -= 2
            for neighbor in range(2):
                xn = x + np.random.choice([-1, 1])
                yn = y + np.random.choice([-1, 1])
                self.values[xn, yn] += 1
                self.visited[xn, yn] = True


        # jak są dwie to rozrzucamy losowo
        raise NotImplementedError # TODO

    def in_equilibrium(self):
        raise NotImplementedError

    def AvalancheLoop(self):
        number_of_iterations = 0
        self.visited[...] = False
        while not self.in_equilibrium():
            self.Toppling()
            self.Dissipation()

            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum() # dla Manna
        return dict(AvalancheSize=AvalancheSize, number_of_iterations=number_of_iterations)

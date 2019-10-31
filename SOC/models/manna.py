from SOC import common
import numpy as np

class Manna(common.Simulation):
    def __init__(self, L):
        super().__init__(L)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)

    def Toppling(self):
        # jak są dwie to rozrzucamy losowo
        raise NotImplementedError # TODO

    def AvalancheLoop(self):
        number_of_iterations = 0
        while False: #!układ_w_równowadze:
            self.Toppling()
            self.Dissipation()

            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum() # dla Manna
        return dict(AvalancheSize=AvalancheSize, number_of_iterations=number_of_iterations)

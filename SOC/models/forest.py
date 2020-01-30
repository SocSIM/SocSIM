"""Implements the Forest Fire model"""

from SOC import common
import numpy as np
import matplotlib.pyplot as plt
import numba

#Three possible states
_ash = 0
_tree = 1
_burning = 2

class Forest(common.Simulation):
    def __init__(self, p=0.05, f: float = 0, *args, **kwargs):
        """
        :param f: probability of thunder setting a tree on fire; set 0 to disable lighting
        """
       
        super().__init__(*args, **kwargs)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        # probabilities = np.random.random(size=(self.L, self.L))
        # trees_here = probabilities <= p
        # self.values[self.BC:self.L_with_boundary - self.BC,
        #             self.BC:self.L_with_boundary - self.BC,
        #             ][trees_here] = _tree
        self.values = common.clean_boundary_inplace(np.random.choice([_ash, _tree, _burning], self.values.shape, p=[0.99, 0.01, 0]), self.BC)
        self.new_values = np.zeros_like(self.values)
        self.p = p
        self.f = f

        # xi, yi = np.random.randint(self.BC, self.L_with_boundary - self.BC, 2)
        # self.values[self.BC:self.L_with_boundary - self.BC,
        #             self.BC:self.L_with_boundary - self.BC,
        #             ][xi, yi] = _burning

        
    def drive(self):
        """
        Does nothing in FF!
        """

    def topple_dissipate(self, i):
        """
        Forest burning and turning into ash. 
        
        :param p: probability of a new tree growh per empty cell, must be smaller than p
        :type p: float
        """
         
        #Displacement from a cell to its nearest neighbours

        # self.new_values[...] = self.values
        number_burning = (self.values[self.BC:-self.BC, self.BC:-self.BC] == _burning).sum()
        if i % 3 == 0:
            # A to T with small probability
            ash_here = self.values == _ash

            probabilities = np.random.random(size=(self.L_with_boundary, self.L_with_boundary))
            trees_grow_here = probabilities <= self.p

            self.new_values[common.clean_boundary_inplace(trees_grow_here & ash_here, self.BC)] = _tree
        elif i % 3 == 1:
            # Trees start burning: T -> B
            self.new_values[self.values == _tree] = _tree
            burn_trees(self.new_values, self.values, self.f, self.BC)
        elif i % 3 == 2:
            # B to A
            burning_here = self.values == _burning
            self.new_values[common.clean_boundary_inplace(burning_here, self.BC)] = _ash
        else:
            raise Exception("wtf?")

        self.values, self.new_values = self.new_values, self.values
        return number_burning

_neighbours = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
@numba.njit
def burn_trees(new_values, values, f, BC):
    for ix in range(BC, values.shape[0] - BC):
        for iy in range(BC, values.shape[1] - BC):
            if values[ix, iy] == _tree:
                if np.random.random() <= f:
                    new_values[ix,iy] = _burning
                else:
                    for dx, dy in _neighbours:
                        if values[ix+dx, iy+dy] == _burning:
                            new_values[ix,iy] = _burning
                            break

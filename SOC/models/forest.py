"""Implements the Forest Fire model"""

from SOC import common
import numpy as np
import matplotlib.pyplot as plt

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
        probabilities = np.random.random(size=(self.L, self.L))
        trees_here = probabilities <= p
        self.values[self.BC:self.L_with_boundary - self.BC,
                    self.BC:self.L_with_boundary - self.BC,
                    ][trees_here] = _tree
        self.p = p
        self.f = f
        
    def drive(self):
        """
        Does nothing in FF!
        """

    def topple(self):
        """
        Forest burning and turning into ash. 
        
        :param p: probability of a new tree growh per empty cell, must be smaller than p
        :type p: float
        """
         
        #Displacement from a cell to its nearest neighbours
        neighbours = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

        # A to T with small probability
        ash_here = self.values == _ash

        probabilities = np.random.random(size=(self.L_with_boundary, self.L_with_boundary))
        trees_grow_here = probabilities <= self.p

        self.values[common.clean_boundary_inplace(trees_grow_here & ash_here, self.BC)] = _tree

        # TODO move to numba
        # Trees start burning: T -> B
        for ix in range(self.BC, self.L_with_boundary - self.BC):
            for iy in range(self.BC, self.L_with_boundary - self.BC):
                if self.values[ix,iy] == _tree:
                    if np.random.random() <= self.f:
                        self.values[ix,iy] = _burning
                    else:
                        for dx, dy in neighbours:
                            if self.values[ix+dx, iy+dy] == _burning:
                                self.values[ix,iy] = _burning
                                break
               
        # B to A
        burning_here = self.values == _burning
        self.values[common.clean_boundary_inplace(burning_here, self.BC)] = _ash

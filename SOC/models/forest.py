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
    """
    Forest fire model

    :param f: probability of thunder setting a tree on fire; set 0 to disable lighting
    :param p: probability of a new tree growh per empty cell
    :type p: float
    """

    def __init__(self, p: float=0.05, f: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shape = (self.L_with_boundary, self.L_with_boundary)
        self.values = common.clean_boundary_inplace(np.random.choice([_ash, _tree, _burning], shape, p=[0.99, 0.01, 0]), self.BC)
        self.new_values = np.zeros_like(self.values)
        self.p = p
        self.f = f

    def drive(self):
        """
        Does nothing in FF!
        """

    def topple_dissipate(self)->int:
        """
        Forest burning and turning into ash. 
        """
         
        #Displacement from a cell to its nearest neighbours

        # self.new_values[...] = self.values
        # A to T with small probability
        ash_here = self.values == _ash

        probabilities = np.random.random(size=(self.L_with_boundary, self.L_with_boundary))
        trees_grow_here = probabilities <= self.p

        self.new_values[common.clean_boundary_inplace(trees_grow_here & ash_here, self.BC)] = _tree
        # Trees start burning: T -> B
        self.new_values[self.values == _tree] = _tree
        burn_trees(self.new_values, self.values, self.f, self.BC)
        # B to A
        burning_here = self.values == _burning
        self.new_values[common.clean_boundary_inplace(burning_here, self.BC)] = _ash

        self.values, self.new_values = self.new_values, self.values
        self.new_values[...] = 0
        number_burning = (self.inside(self.values) == _burning).sum()
        return number_burning

_neighbours = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
@numba.njit
def burn_trees(new_values: np.ndarray, values: np.ndarray, f: float, BC: int):
    """
    Tree-burning loop

    :param new_values: Temporary array of values in the next step.
    :param values: Array of current values.
    :param f: probability of thunder strike
    :param BC: size of boundary
    """
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

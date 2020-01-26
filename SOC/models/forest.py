"""Implements the Forest Fire model"""

from SOC import common
import numpy as np
import matplotlib.pyplot as plt

class Forest(common.Simulation)

    #Three possible states
    ash = 0
    tree = 1
    burning = 2
    
    #Displacement from a cell to its nearest neighbours
    neighbours = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))
    
    #The initial fraction of the forest occupied by trees
    fraction = 0.3
      
    def __init__(self, p: float = 0.05, f: float = 0.001, *args, **kwargs)
        """
        :param L: linear size of lattice without boundaries
        :type L: int
        :param p: probability of a new tree growh per empty cell
        :type p: float
        :param f: probability of a lightning strike
        :type f: float
        """
       
        super().__init__(*args, **kwargs)
        self.p = p
        self.f = f
        

    #Initializing the forest grid
    def create(self.L_with_boundary)
        forest_before = np.zeros(self.L_with_boundary, self.L_with_boundary)
        # I kinda assume here boundary = 1 anyway
        forest_before[1:self.L+1, 1:self.L+1] = np.random.randit(0, 2, size = (self.L, self.L))
        forest_before[1:self.L+1, 1:self.L+1] = np.random.random(size = (self.L, self.L)) < fraction
        
        return forest_before
     
    #Applying forest fire rules    
    def iterate(forest_before)
    
        forest_after = np.zeros((self.L_with_boundary, self.L_with_boundary))
        
        for ix in range(1,self.L+1):
            for iy in range(1,self.L+1):
                #ash
                if forest_before[ix,iy] == ash and np.random.random() <= self.p:
                    forest_after[ix,iy] = tree
                #tree
                if forest_before[ix,iy] == tree
                    forest_after[ix,iy] = tree
                    for dx, dy in neighbours:
                        if forest_before[ix+dx, iy+dy] == burning:
                            forest_after[ix,iy] = burning
                            break
                    else: np.random.random() <= self.f:
                            forest_after = burning
                #burning
                if forest_before[ix,iy] == burning:
                    forest_after[ix,iy] = ash
       
        return forest_after
   


                       
                            
            
            
            
            
            
            
            
            
            
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
      
    def __init__(self, *args, **kwargs)
        """
        """
       
        super().__init__(*args, **kwargs)
        self.values = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)
        
        # I kinda assume here boundary = 1 anyway
        #forest_before[1:self.L+1, 1:self.L+1] = np.random.randit(0, 2, size = (self.L, self.L))
        #forest_before[1:self.L+1, 1:self.L+1] = np.random.random(size = (self.L, self.L)) < fraction

    
     
    def drive(self, p: float = 0.05):
        """
        Drive the simulation by creating new trees.
        
        :param p: probability of a new tree growh per empty cell
        :type p: float

        """
        for ix in range(1,self.L+1):
            for iy in range(1,self.L+1):
                #ash
                if self.values[ix,iy] == ash and np.random.random() <= p:
                    self.values[ix,iy] = tree
 

    def topple_dissipate(self,  f: float = 0.001,):
        """
        Forest burning and turning into ash. 
        
        :param p: probability of a new tree growh per empty cell, must be smaller than p
        :type p: float
        """
         
        for ix in range(1,self.L+1):
            for iy in range(1,self.L+1):
                #tree
                if self.values[ix,iy] == tree
                    for dx, dy in neighbours:
                        if self.values[ix+dx, iy+dy] == burning:
                            self.values[ix,iy] = burning
                            break
                    else: np.random.random() <= self.f:
                        self.values[ix,iy] = burning
               
                #burning
                elif self.values[ix,iy] == burning:
                    self.values[ix,iy] = ash
       
   


                       
                            
            
            
            
            
            
            
            
            
            
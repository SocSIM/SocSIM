"""Avalanches"""

import numpy as np
from SOC.common import SaveImage
import tqdm.auto as tqdm
import numba

def GetMatrixBase(dim, val = 0):
    """Return matrix base, with a single sand grain in the middle"""
    m = np.ones(dim) * val
    SandFalling(m, 1)
    return m

def SandFalling(matrix, count = 1):
    """Drop a new grain on the matrix's center"""
    dim = matrix.shape
    matrix[int((dim[0] - 1) / 2), int((dim[0] - 1) / 2)] += count


@numba.njit
def OneTimeStepSimulation(matrixOrig, thresholdValue = 4):
    """OneTimeStepSimulation"""
    # avalancheCount = 0
    dim = matrixOrig.shape
    	
    for k in range(dim[0] * dim[1]):		
        # matrix that records differences
        matrix = np.zeros(dim)
        # this flag breakes cycle if there is no more avalanches
        shouldBreak = True
        for i in range(dim[0]):
            for j in range(dim[1]):

                if matrixOrig[i, j] >= thresholdValue:
                    matrix[i, j] -= 4
                    shouldBreak = False
                    if i == 0:
                        #avalancheCount += 1
                        matrix[i + 1, j] += 1
                    elif i == dim[0] - 1:
                        #avalancheCount += 1
                        matrix[i - 1, j] += 1

                    if j == 0:
                        #avalancheCount += 1
                        matrix[i, j + 1] += 1
                    elif j == dim[1] - 1:
                        #avalancheCount += 1
                        matrix[i, j - 1] += 1

                    if i > 0 and i < dim[0] - 1:
                        matrix[i + 1, j] += 1
                        matrix[i - 1, j] += 1
                    if j > 0 and j < dim[1] - 1:
                        matrix[i, j + 1] += 1
                        matrix[i, j - 1] += 1
        if shouldBreak:
            break

        #adds to origin matrix, difference matrix that recorded avalanches
        matrixOrig += matrix


def MainLoop(N: int, save_every: int = False, plot_histogram: bool  = False):
    """MainLoop

    Parameters
    ==========
    N: int
        Number of iterations
    save_every: int or False
        if not False, save a snapshot of the simulation every `save_every`
        iterations
    plot_histogram: bool
        toggles plotting a histogram at the end of the run
        
    """
    AvalancheCountArray = []

    #creating of overloaded sand base
    matrix = GetMatrixBase([101, 101], 4)

    #initialization of dune after several avalanches
    OneTimeStepSimulation(matrix)

    PrevMatrixTotalCount = np.sum(matrix)
    CurMatrixTotalCount = PrevMatrixTotalCount
    for i in tqdm.trange(N):
        OneTimeStepSimulation(matrix)
        
        CurMatrixTotalCount = np.sum(matrix)
        AvalancheCountArray.append(CurMatrixTotalCount - PrevMatrixTotalCount)
        PrevMatrixTotalCount = CurMatrixTotalCount

        SandFalling(matrix, 1)

        if save_every and (i % save_every == 0):
            SaveImage(matrix, f'soc{i:05d}.png')
    histData, minor = np.histogram(AvalancheCountArray)
    if plot_histogram:
        import matplotlib.pyplot as plt
        plt.hist(AvalancheCountArray)
        plt.show()

if __name__ == "__main__":
    MainLoop(10000)

import numpy as np
from SOC.common import SaveImage

#returns matrix base with one item in center
def GetMatrixBase(dim, val = 0):
    m = np.ones(dim) * val
    m[int((dim[0] - 1) / 2), int((dim[0] - 1) / 2)] += 1
    return m

#puts new sand item to center of matrix
def SandFalling(matrix, count = 1):
    dim = matrix.shape
    matrix[int((dim[0] - 1) / 2), int((dim[0] - 1) / 2)] += count


def OneTimeStepSimulation(matrixOrig):
    
    #avalancheCount = 0
    dim = matrixOrig.shape
    thresholdValue = 4
    	
    for k in range(dim[0] * dim[1]):		
        #matrix that records differences
        matrix = np.zeros(matrixOrig.shape)
        #this flag breakes cycle if there is no more avalanches
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


def MainLoop(N):
    AvalancheCountArray = []

    #creating of overloaded sand base
    matrix = GetMatrixBase([101, 101], 4)

    #initialization of dune after several avalanches
    OneTimeStepSimulation(matrix)

    PrevMatrixTotalCount = np.sum(matrix)
    CurMatrixTotalCount = PrevMatrixTotalCount
    for i in range(N):
        OneTimeStepSimulation(matrix)
        
        CurMatrixTotalCount = np.sum(matrix)
        AvalancheCountArray.append(CurMatrixTotalCount - PrevMatrixTotalCount)
        PrevMatrixTotalCount = CurMatrixTotalCount

        SandFalling(matrix, 1)

    SaveImage(matrix, 'soc'+ str(i) + '.png', 0)
    histData, minor = np.histogram(AvalancheCountArray)
    print(histData)
    print(AvalancheCountArray)
    plt.hist(AvalancheCountArray)
    plt.show()
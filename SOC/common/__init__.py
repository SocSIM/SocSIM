"""common"""
from .simulation import Simulation, clean_boundary_inplace
from matplotlib import pyplot as plt


def SaveImage(matrix, file_name = 'image.png'):  
    """SaveImage"""
    cax = plt.imshow(matrix, interpolation = 'nearest')
    cax.set_clim(vmin = 0, vmax = 4)
    plt.savefig(file_name, dpi = 100)
    plt.clf()

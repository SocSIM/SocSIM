"""Contains the base class for the simulation."""
import numpy as np
from tqdm import auto as tqdm
import numba
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas
import seaborn
from . import analysis
import zarr
import datetime

class Simulation:
    """Base class for SOC simulations."""
    values = NotImplemented
    saved_snapshots = NotImplemented

    BOUNDARY_SIZE = BC = 1
    def __init__(self, L: int, save_every: int = 100, wait_for_n_iters: int = 10):
        """__init__

        :param L: linear size of lattice, without boundary layers
        :type L: int
        :param save_every: number of iterations per snapshot save
        :type save_every: int or None
        """
        self.L = L
        self.visited = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=bool)
        self.data_acquisition = []
        self.save_every = save_every
        self.wait_for_n_iters = wait_for_n_iters
        # zliczanie relaksacji
        self.releases = np.zeros((self.L_with_boundary, self.L_with_boundary), dtype=int)

    @property
    def size(self):
        return self.L**2

    @property
    def L_with_boundary(self):
        return self.L + 2 * self.BOUNDARY_SIZE

    def drive(self):
        """
        Drive the simulation by adding particles from the outside.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the drive method!")

    def topple(self):
        """
        Distribute material from overloaded sites to neighbors.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the topple method!")

    def dissipate(self):
        """
        Handle losing material at boundaries.

        This may be removed in the future.

        Must be overriden in subclasses.
        """
        pass

    @classmethod
    def clean_boundary_inplace(cls, array: np.ndarray) -> np.ndarray:
        """
        Convenience wrapper to `clean_boundary_inplace` with the simulation's boundary size. 

        :param array:
        :type array: np.ndarray
        :rtype: np.ndarray
        """
        return clean_boundary_inplace(array, self.BOUNDARY_SIZE)

    def AvalancheLoop(self) -> dict:
        """
        Bring the current simulation's state to equilibrium by repeatedly
        toppling and dissipating.

        Returns a dictionary with the total size of the avalanche
        and the number of iterations the avalanche took.

        :rtype: dict
        """
        number_of_iterations = 0 # TODO rename number_of_topples/czas rozsypywania/duration
        self.visited[...] = False
        self.releases[...] = 0
        while self.topple():
            self.dissipate()
            number_of_iterations += 1
        
        AvalancheSize = self.visited.sum()
        NumberOfReleases = self.releases.sum()
        return dict(AvalancheSize=AvalancheSize, NumberOfReleases=NumberOfReleases, number_of_iterations=number_of_iterations)

    def run(self, N_iterations: int,
            filename: str  = None,
            wait_for_n_iters: int = 10,
            ) -> dict:

        """
        Simulation loop. Drives the simulation, possibly starts avalanches, gathers data.

        :param N_iterations: number of iterations (per grid node if `scale` is True)
        :type N_iterations: int
        :rtype: dict
        :param filename: filename for saving snapshots. if None, saves to memory; by default if False, makes something like array_Manna_2019-12-17T19:40:00.546426.zarr
        :type filename: str
        :param wait_for_n_iters: wait this many iterations before collecting data
                                 (lets model thermalize)
        :type wait_for_n_iters: int
        """
        if filename is False:
            filename = f"array_{self.__class__.__name__}_{datetime.datetime.now().isoformat()}.zarr"
        scaled_wait_for_n_iters = wait_for_n_iters
        scaled_n_iterations = N_iterations + scaled_wait_for_n_iters
        if scaled_n_iterations % self.save_every != 0:
            raise ValueError(f"Ensure save_every ({self.save_every}) is a divisor of the total number of iterations ({scaled_n_iterations})")
        print(f"Waiting for wait_for_n_iters={wait_for_n_iters} iterations before collecting data. This should let the system thermalize.")

        total_snapshots = max([scaled_n_iterations // self.save_every, 1])
        self.saved_snapshots = zarr.open(filename,
                                         shape=(
                                             total_snapshots,                            # czas
                                             self.L_with_boundary,                       # x
                                             self.L_with_boundary,                       # y
                                         ),
                                         chunks=(
                                             100,
                                             self.L_with_boundary,
                                             self.L_with_boundary,
                                         ),
                                         dtype=self.values.dtype,
                                         )
        self.saved_snapshots.attrs['save_every'] = self.save_every

        for i in tqdm.trange(scaled_n_iterations):
            self.drive()
            observables = self.AvalancheLoop()
            if i >= scaled_wait_for_n_iters:
                self.data_acquisition.append(observables)
            if self.save_every is not None and (i % self.save_every) == 0:
                self._save_snapshot(i)
        return filename

    def _save_snapshot(self, i):
        self.saved_snapshots[i // self.save_every] = self.values

    @property
    def data_df(self):
        return pandas.DataFrame(self.data_acquisition)

    def plot_histogram(self, column='AvalancheSize', num=50, filename = None, plot = True):
        return analysis.plot_histogram(self.data_df, column, num, filename, plot)

    def plot_state(self, with_boundaries = False):
        """
        Plots the current state of the simulation.
        """
        fig, ax = plt.subplots()

        if with_boundaries:
            values = self.values
        else:
            values = self.values[self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE, self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE]
        
        IM = ax.imshow(values, interpolation='nearest')
        
        plt.colorbar(IM)
        return fig

    def animate_states(self, notebook: bool = False, with_boundaries: bool = False):
        """
        Animates the collected states of the simulation.

        :param notebook: if True, displays via html5 video in a notebook;
                        otherwise returns MPL animation
        :type notebook: bool
        :param with_boundaries: include boundaries in the animation?
        :type with_boundaries: bool
        """
        fig, ax = plt.subplots()

        if with_boundaries:
            values = np.dstack(self.saved_snapshots)
        else:
            values = np.dstack(self.saved_snapshots)[self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE, self.BOUNDARY_SIZE:-self.BOUNDARY_SIZE, :]

        IM = ax.imshow(values[:, :, 0],
                       interpolation='nearest',
                       vmin = values.min(),
                       vmax = values.max()
                       )
        
        plt.colorbar(IM)
        iterations = values.shape[2]
        title = ax.set_title("Iteration {}/{}".format(0, iterations * self.save_every))

        def animate(i):
            IM.set_data(values[:,:,i])
            title.set_text("Iteration {}/{}".format(i * self.save_every, iterations * self.save_every))
            return IM, title

        anim = animation.FuncAnimation(fig,
                                       animate,
                                       frames=iterations,
                                       interval=30,
                                       )
        if notebook:
            from IPython.display import HTML, display
            plt.close(anim._fig)
            display(HTML(anim.to_html5_video()))
        else:
            return anim
    
    def get_exponent(self, *args, **kwargs):
        return analysis.get_exponent(self.data_df, *args, **kwargs)

    @classmethod
    def from_file(cls, filename):
        saved_snapshots = zarr.open(filename)
        save_every = saved_snapshots.attrs['save_every']
        L = saved_snapshots.shape[1] - 2 * cls.BOUNDARY_SIZE
        self = cls(L=L, save_every=save_every)
        self.values = saved_snapshots[-1]
        self.saved_snapshots = saved_snapshots
        return self
        
@numba.njit
def clean_boundary_inplace(array: np.ndarray, boundary_size: int, fill_value = False) -> np.ndarray:
    """
    Fill `array` at the boundary with `fill_value`.

    Useful to make sure sites on the borders do not become active and don't start toppling.

    Works inplace - will modify the existing array!

    :param array:
    :type array: np.ndarray
    :param boundary_size:
    :type boundary_size: int
    :param fill_value:
    :rtype: np.ndarray
    """
    array[:boundary_size, :] = fill_value
    array[-boundary_size:, :] = fill_value
    array[:, :boundary_size] = fill_value
    array[:, -boundary_size:] = fill_value
    return array


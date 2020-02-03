"""Contains the base class for the simulation."""
import numpy as np
from tqdm import auto as tqdm
import numba
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas
import seaborn
import zarr
import datetime

class Simulation:
    """Base class for SOC simulations."""
    values = NotImplemented
    saved_snapshots = NotImplemented

    BOUNDARY_SIZE = BC = 1
    def __init__(self, L: int, save_every: int = 1, wait_for_n_iters: int = 10):
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

    def topple_dissipate(self):
        """
        Distribute material from overloaded sites to neighbors.

        Must be overriden in subclasses.
        """
        raise NotImplementedError("Your model needs to override the topple method!")

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
        self.visited[...] = False
        self.releases[...] = 0
        number_of_iterations = self.topple_dissipate()
        
        AvalancheSize = self.visited[self.BC:-self.BC,
                                     self.BC:-self.BC].sum()
        NumberOfReleases = self.releases[self.BC:-self.BC,
                                         self.BC:-self.BC].sum()
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

    def animate_states(self, notebook: bool = False, with_boundaries: bool = False,
                       interval = 30,
                       ):
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
                                       interval=interval,
                                       )
        if notebook:
            from IPython.display import HTML, display
            plt.close(anim._fig)
            display(HTML(anim.to_html5_video()))
        else:
            return anim

    def save(self, file_name = 'sim'):
        """ serialization of object and saving it to file"""

        root = zarr.open_group('state/' + file_name + '.zarr', mode = 'w')
        values = root.create_dataset('values', shape = (self.L_with_boundary, self.L_with_boundary), chunks = (10, 10), dtype = 'i4')
        values = zarr.array(self.values)
        #data_acquisition = root.create_dataset('data_acquisition', shape = (len(self.data_acquisition)), chunks = (1000), dtype = 'i4')
        #data_acquisition = zarr.array(self.data_acquisition)
        root.attrs['L'] = self.L
        root.attrs['save_every'] = self.save_every

        return root

    def open(self, file_name = 'sim'):
        root = zarr.open_group('state/' + file_name + '.zarr', mode = 'r')
        self.values = np.array(root['values'][:])
        #self.data_acquisition = root['data_acquisition'][:]
        self.L = root.attrs['L']
        self.save_every = root.attrs['save_every']
    

    def get_exponent(self,
                     column='AvalancheSize',
                     low: int = 1,
                     high: int = 10,
                     plot = True, 
                     plot_filename=None):
        df = self.data_df
        filtered = df.loc[df.number_of_iterations != 0, column]
        sizes, counts = np.unique(filtered, return_counts=True)
        filtered = df.number_of_iterations[df.number_of_iterations != 0]
        sizes, counts = np.unique(filtered, return_counts=True)
        indices = (low < sizes) & (sizes < high)
        coef_a, coef_b = poly = np.polyfit(np.log10(sizes[indices]), np.log10(counts[indices]), 1)
        # assert smooth_width < hist_num
        #     second_deriv = grab_second_deriv(log_heights, smooth_width)
        #     ind_min, ind_max = find_largest_true_block(np.abs(second_deriv) <= d2_cutoff)
        # else:
        #     ind_min, ind_max = cutoffs

        if plot:
            fig, ax = plt.subplots()
            ax.loglog(sizes, counts, "o", label="Data")
            x_plot = np.array([low, high])
            ax.loglog(x_plot,
                      10**(np.polyval((poly), np.log10(x_plot))),
                      label=fr"$y = {10**coef_b:.3f} \exp({coef_a:.4f} x)$")
            ax.axvline(low, linestyle="--", label=f"Low cutoff: {low:.3f}")
            ax.axvline(high,  linestyle="--", label=f"High cutoff: {high:.3f}")
            ax.grid()
            ax.legend(loc='best')
            ax.set_xlabel(column)
            ax.set_ylabel(f"Count[{column}]")
            plt.tight_layout()
            if plot_filename is None:
                plt.show()
            else:
                fig.savefig(plot_filename)
                plt.close()
        print(f"y = {10**coef_b:.3f} exp({coef_a:.4f} x)")
        return dict(exponent=coef_a, intercept = coef_b)

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


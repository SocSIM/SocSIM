import numba
import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(df, column='AvalancheSize', num=50, filename = None, plot = True):
    min_range = np.log10(df[column].min()+1)
    bins = np.logspace(min_range,
                       np.log10(df[column].max()+1),
                       num = num)
    if plot == "pass":
        fig, ax = plt.subplots()
        heights, bins, _ = ax.hist(df[column], bins, label="Data (log-uniformly spaced bins)")
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlabel(column)
        ax.set_ylabel("count")
        if filename is not None:
            fig.savefig(filename)
        plt.tight_layout()
        if plot != "pass":
            plt.show()
    else:
        fig = None
        heights, bins = np.histogram(df[column], bins)
    return heights, bins, fig

@numba.njit
def find_largest_true_block(arr):
    """
    Given a boolean numpy array, finds the starting and ending indices
    for the largest continuous block of """
    start_index = -1
    max_start_index = -1
    max_length = -1
    length = -1
    i = 0
    is_in_block = False
    while i < len(arr):
        if arr[i] and not is_in_block:
            start_index = i
            length = 0
            is_in_block = True
        elif arr[i] and is_in_block:
            length += 1
        else:
            is_in_block = False
            if length > max_length:
                max_length = length
                max_start_index = start_index
        i += 1
    if length > max_length:
        max_length = length
        max_start_index = start_index
    return max_start_index, max_start_index + max_length

def grab_second_deriv(arr,smooth_width: int = 20):
    """
    Calculate second derivative of array via convolution with a smoothing second derivative filter
    
    as per https://stackoverflow.com/questions/13691775/python-pinpointing-the-linear-part-of-a-slope
    """
    smooth_width = 20
    x1 = np.linspace(-3, 3, smooth_width)
    norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0]) # ad hoc normalization
    y1 = (4*x1**2 - 2) * np.exp(-x1**2) / smooth_width *8#norm*(x1[1]-x1[0])
    y_conv = np.convolve(arr, y1, mode="same")
    return y_conv

def get_exponent(df, col='AvalancheSize', hist_num: int = 50, smooth_width: int = 20, d2_cutoff: float = 0.3, cutoffs = None, plot=False, sd_df = None):
    assert smooth_width < hist_num
    heights, bin_edges, fig = plot_histogram(df, column=col, num=hist_num, plot = "pass" if plot else False)
    bin_middles = (bin_edges[1:] + bin_edges[:-1])/2
    plt.semilogy(bin_middles)   # TODO bin edges ma offset względem bin middles; to trzeba poprawić - interpolacja zamiast średniej?
    finites = heights > 0   # inaczej logarytm umiera w boolach ;)
    
    if cutoffs is None:
        log_heights = np.log10(heights[finites])

        second_deriv = grab_second_deriv(log_heights, smooth_width)
        ind_min, ind_max = find_largest_true_block(np.abs(second_deriv) <= d2_cutoff)
    else:
        ind_min, ind_max = cutoffs
        

    if plot:
        ax = fig.gca()
        ax.loglog(bin_middles[finites], heights[finites], label="full data")
        ax.loglog(bin_middles[finites][ind_min:ind_max], heights[finites][ind_min:ind_max], label="largest block of small 2nd deriv")
        ax.legend()
    fit = np.polynomial.Polynomial.fit(np.log10(bin_middles[finites][ind_min:ind_max]),
                                       np.log10(heights[finites][ind_min:ind_max]),
                                       1
                                      )
    return dict(exponent=fit.coef[1], x_data = bin_middles[finites][ind_min:ind_max], y_data=heights[finites][ind_min:ind_max])

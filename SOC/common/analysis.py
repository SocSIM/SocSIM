import numba
import matplotlib.pyplot as plt
import numpy as np

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

def get_exponent(model, hist_num: int = 50, smooth_width: int = 20, d2_cutoff: float = 0.3, cutoffs = None, plot=False):
    assert smooth_width < hist_num
    heights, bin_edges = model.plot_histogram(num=hist_num, plot = plot)
    bin_middles = (bin_edges[1:] + bin_edges[:-1])/2
    if plot:
        plt.figure()
        plt.semilogy(bin_edges)
        plt.semilogy(bin_middles)   # to trzeba poprawić - interpolacja zamiast śre
        
    finites = heights > 0   # inaczej logarytm umiera w boolach ;)
    
    if cutoffs is None:
        log_heights = np.log10(heights[finites])

        second_deriv = grab_second_deriv(log_heights, smooth_width)
        ind_min, ind_max = find_largest_true_block(np.abs(second_deriv) <= d2_cutoff)
    else:
        ind_min, ind_max = cutoffs
        

    if plot:
        plt.figure()
        plt.loglog(bin_middles[finites], heights[finites], label="full data")
        plt.loglog(bin_middles[finites][ind_min:ind_max], heights[finites][ind_min:ind_max], label="largest block of small 2nd deriv")
        plt.legend()
    fit = np.polynomial.Polynomial.fit(np.log10(bin_middles[finites][ind_min:ind_max]),
                                       np.log10(heights[finites][ind_min:ind_max]),
                                       1
                                      )
    return dict(exponent=fit.coef[1], x_data = bin_middles[finites][ind_min:ind_max], y_data=heights[finites][ind_min:ind_max])

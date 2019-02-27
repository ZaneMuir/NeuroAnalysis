import numpy as np


def empirical_dist(arr):
    """
    **empirical distribution function**

    $$ \\hat{F}_n (t) = \\frac{1}{n} \\sum_{i=1}^n 1_{X_i \\le t}$$

    Arguments:
    - arr: 1d numeric array
    """

    _arr_idx = np.argsort(arr)
    _arr = arr[_arr_idx]

    _x = np.repeat(_arr, 2)
    _y = np.repeat(np.linspace(1, np.size(_arr), np.size(_arr)), 2)
    _y = np.pad(_y, (1,0), 'constant')[:-1] / np.size(_arr)

    return _x, _y, _arr_idx

from .SpikeUnit import SpikeUnit
import numpy as np


def gaussian_kernel(sigma):
    """
The gaussian kernel.

.. math ::
    w(\\tau) = \\frac{1}{\\sqrt{2 \\pi} \\sigma_w}
    \\exp(-\\frac{\\tau^2}{2 \\sigma^2_w})

example:

.. code-block:: python

    >>> kernel('guassian', {'sigma': 0.4})
    """
    return lambda t: 1/(np.sqrt(2*np.pi)*sigma) * np.exp(-t**2/(2*sigma**2))


def causal_kernel(alpha):
    """
The causal kernel.

.. math::
    w(\\tau) = [\\alpha^2 \\tau \\exp(- \\alpha \\tau)]_+

example:

.. code-block:: python

    >>> kernel('causal', {'alpha': 0.4})
    """
    def causal(t):
        v = alpha**2 * t * np.exp(-alpha*t)
        v[v<0] = 0
        return v
    return causal


def rectangular_kernel(delta):
    """
Moving rectangular kernel.

.. math::
    w(\\tau) = \\begin{cases}
    \\frac{1}{\Delta t} &,\\ -\\frac{\Delta t}{2} \\leq t \\leq \\frac{\\Delta t}{2} \\\\
    0 &,\\ otherwise
    \\end{cases}

example:

.. code-block:: python

    >>> kernel('square', {'delta': 0.4})

    """
    return lambda t: np.ones_like(t[(t>=-delta/2)&(t<=delta/2)]) / delta


def kernel(name, **args):
    """
Get the kernel function.

Kernels:
    - gaussian, args: [sigma]
    - causal, args: [alpha]
    - square, args: [delta]

Args:
    - name:   name of the kernel
    - \*\*args: arguments for each kernel.

Return:
    - kernel function in lambda.

Example:

.. code-block:: python

    >>> kernel('guassian', {'sigma':0.4})


    """
    if name == "gaussian":
        return gaussian_kernel(**args)
    elif name == "causal":
        return causal_kernel(**args)
    elif name=="square":
        return rectangular_kernel(**args)
    else:
        raise NameError("unkown kernel: "+str(name))


def _check_and_convert_to_ndarray(subject):
    if isinstance(subject,SpikeUnit):
        target = subject.spike_train
    elif isinstance(subject,list):
        target = np.array(subject)
    elif isinstance(subject, np.ndarray):
        target = subject
    else:
        raise ValueError("type of to is not supported: "+str(type(subject)))
    return target


def generate_linear_filter(to, k):
    """
Convert the discrete spike train array into a linear filter funciton.

Args:
    - to: data in numpy.ndarray or SpikeUnit class
    - k: kernel

Returns:
    - kernel lambda function

    """
    target = _check_and_convert_to_ndarray(to)
    return lambda t: np.sum(k(target - t))


def apply_linear_filter(to, k, x_range=None, nbins=1000, returnX=True):
    """
Map linear filter into a ndarray.

Args:
    - to: data in numpy.ndarray or SpikeUnit class
    - k: kernel
    - x_range: time range tuple (starttime, endtime), default as None
    - nbins: number of steps, default as 1000
    - returnX: return timespan ndarray

Returns:
    - [X_range,] discrete_linear_filter

    """
    target = _check_and_convert_to_ndarray(to)
    linear_filter = generate_linear_filter(to, k)

    if x_range is None:
        x_range = np.linspace(0, target[-1], nbins)
    elif isinstance(x_range, tuple) or isinstance(x_range, list):
        x_range = np.linspace(x_range[0], x_range[1], nbins)
    elif isinstance(x_range, np.ndarray):
        returnX = False
        pass
    else:
        raise ValueError("invalid x_range")

    if returnX:
        return x_range, np.array(list(map(linear_filter, x_range)))  # XXX
    else:
        return np.array(list(map(linear_filter, x_range)))


def apply_linear_filter_withroi(train, k, starts, roi=(0,0), nbins=1000, pbar=None):
    """
Map linear filter into a ndarray with a region of interest.

Args:
    - to: data in numpy.ndarray or SpikeUnit class
    - k: kernel
    - starts: start time points in list or 1-d ndarray
    - roi: region of interest, in time tuple (starttime, endtime)
    - nbins: number of steps, default as 1000
    - pbar: progress bar in tqdm

Returns:
    - _mean_response: 1-d ndarray
    """
    _mean_response = None

    for each_start in starts:
        a = apply_linear_filter(train, k,
                                x_range=(each_start+roi[0], each_start+roi[1]),
                                nbins=nbins, returnX=False)
        if _mean_response is None:
            _mean_response = a
        else:
            _mean_response = np.vstack((_mean_response, a))

        if pbar:
            pbar.update(1)

    return _mean_response

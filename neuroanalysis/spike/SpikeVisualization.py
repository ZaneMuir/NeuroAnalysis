# from . import SpikeUnit
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def _calc_error(mean_response, ci):
    _std = np.std(mean_response, axis=0)
    if ci == 'std':
        return _std
    elif isinstance(ci, float):
        return _std * stats.t.ppf(ci,np.shape(mean_response)[0])
    else:
        raise ValueError("invalid ci name: either float number between 0-1, or \"std\"")

def plot_curve_with_error_ribbon(mean_response, roi,
                                 ci='std', error_alpha=0.1, markers=None,
                                 label='', color=None, plotax=plt):
    _mean = np.mean(mean_response, axis=0)
    _ci = _calc_error(mean_response, ci=ci)


    x = np.linspace(roi[0],roi[1],len(_mean))
    plotax.plot(x, _mean, label=label,color=color)
    plotax.fill_between(x, _mean-_ci, _mean+_ci, alpha=error_alpha, color=color)
    if markers:
        markers()
    plt.xlim(roi)
    return

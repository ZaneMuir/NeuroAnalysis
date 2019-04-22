import numpy as np
import matplotlib.pyplot as plt
from .single_unit import PSTH


def crosscorrelogram(target, reference, shift=None, ROI=(-0.5,0.5), binsize=.01, skip_plot=False):
    """
    Cross Correlation between two unit, optionally corrected by shift predictor.
    
    arguments:
    - target: the target spike train as 1d numpy.array
    - reference: the reference spike train as 1d numpy.array
    
    keyword arguments:
    - shift: shift size, if None then skip the shift predictor correction [default: None]
    - ROI: region of interest as tuple [default: (-0.5, 0.5)]
    - binsize: the size of each bin [default: 0.01]
    - skip_plot: if True then skip auto plot crosscorrelogram [default: False]
    
    return:
    - crosscorrelogram: as in 1d numpy.array
    """

    _xcorr, _ = PSTH(target, reference, ROI, binsize, True)
    if not isinstance(shift, type(None)):
        _xcorr_shift, _ = PSTH(target, reference[reference > shift]-shift, ROI, binsize, True)
        _xcorr = _xcorr - _xcorr_shift

    if not skip_plot:
        plt.figure(figsize=(8,4))
        _tspec = np.linspace(ROI[0], ROI[1]-1/int((ROI[1]-ROI[0])/binsize), int((ROI[1]-ROI[0])/binsize))
        plt.bar(_tspec+binsize/2, _xcorr, width=binsize)
        plt.vlines([0], 0, np.max(_xcorr)*1.05, linestyle='--', alpha=0.5)
        plt.xlim((ROI[0], ROI[-1]))
        plt.show()

    return _xcorr
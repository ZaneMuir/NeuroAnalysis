import numpy as np
import matplotlib.pyplot as plt
from .single_unit import PSTH


def shiftappend(arr, shift, end=None, direction='left'):
    if isinstance(end, type(None)):
        end = arr[-1]
    
    if direction == 'left':
        return np.hstack((arr[arr > shift]-shift, arr[arr < shift]+end-shift))
    elif direction == 'right':
        return np.hstack((arr[arr < shift]-end+shift, arr[arr < shift]+shift))
    else:
        raise ValueError('unknown direction: %s'%direction)

def crosscorrelogram(target, reference, ROI=(-0.5,0.5), binsize=.01, shift=None, skip_plot=False):
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
    
    if isinstance(shift, int) or isinstance(shift, float):
        _shift_reference = shiftappend(reference, shift)
        _xcorr_shift, _ = PSTH(target, _shift_reference, ROI, binsize, True)
        _xcorr = _xcorr - _xcorr_shift
        
    elif isinstance(shift, list) or isinstance(shift, np.ndarray):
        _xcorr_shift = np.zeros_like(_xcorr)
        for item in shift:
            _shift_reference = shiftappend(reference, item)
            _xcorr_shift_item, _ = PSTH(target, _shift_reference, ROI, binsize, True)
            _xcorr_shift = _xcorr_shift + _xcorr_shift_item/np.size(shift)
        _xcorr = _xcorr - _xcorr_shift
    else:
        _xcorr_shift = None

    if not skip_plot:
        plt.figure(figsize=(16,4))
        plt.subplot(1,2,2)
        _tspec = np.linspace(ROI[0], ROI[1]-1/int((ROI[1]-ROI[0])/binsize), int((ROI[1]-ROI[0])/binsize))
        plt.bar(_tspec+binsize/2, _xcorr, width=binsize)
        plt.vlines([0], 0, np.max(_xcorr)*1.05, linestyle='--', alpha=0.5)
        plt.xlim((ROI[0], ROI[-1]))
        plt.title('crosscorrelogram')
        
        if not isinstance(_xcorr_shift, type(None)):
            plt.subplot(1,2,1)
            plt.bar(_tspec+binsize/2, _xcorr_shift, width=binsize)
            plt.vlines([0], 0, np.max(_xcorr)*1.05, linestyle='--', alpha=0.5)
            plt.xlim((ROI[0], ROI[-1]))
            plt.title('shift predictor')
        
        plt.show()

    return _xcorr
import numpy as np
import matplotlib.pyplot as plt


def PSTH(train, marker, ROI, binsize=.1, skip_plot=False):
    """
    PSTH - peri-stimulus time histogram or post-stimulus time histogram
    each bin is calcuated as $$\\frac{\\sum_i^N x_i}{N \\cdot \\text{binsize}}$$
    
    arguments:
    - train: the spike train as 1d numpy.array
    - marker: the marker of stimuli
    - ROI: the region of interest for each stimuli, 
           define the range the PSTH.
    
    keyword arguments:
    - binsize: the size of each bin [default: 0.1]
    
    return:
    (PSTH, _seg)
    - PSTH: the `spike/binsize` value of each PSTH bin
    - _seg: spike train for each segment, i.e. the data
            of the raster plot.
    """
    
    _seg = []
    _bins = int((ROI[-1]-ROI[0])/binsize)
    _psth = np.zeros(_bins, dtype='int')
    
    for _idx, _item in enumerate(marker):
        _seg_train = train[(_item+ROI[0]<train)&(train<_item+ROI[-1])]-_item
        _psth_item, _psth_x = np.histogram(_seg_train, range=ROI, bins=_bins)
        _psth = _psth + _psth_item
        _seg.append(_seg_train)

    _psth = _psth/np.size(marker)/binsize
    
    if not skip_plot:
        plt.figure(figsize=(8,8))
        plt.subplot(2,1,1)
        for _idx, _item in enumerate(_seg):
            plt.vlines(_item, _idx+0.5, _idx+1.5)
        plt.xlim(ROI)
        plt.xticks([])
        plt.ylabel('trial #')
        
        plt.subplot(2,1,2)
        plt.bar(_psth_x[:-1]+binsize/2, _psth, width=binsize)
        plt.xlim(ROI)
        plt.ylabel('spkies / binsize')

        plt.tight_layout()
        plt.show()
    
    return _psth, _seg
import numpy as np
from .filter import gaussianwind

## wavelet
def morlet(F, fs):
    """Morlet wavelet"""
    wtime = np.linspace(-1, 1, 2*fs)
    s = 6 / (2 * np.pi * F)
    wavelet = np.exp(2*1j*np.pi*wtime*F) * np.exp(-wtime**2/(2*s**2))
    return wavelet

## wavelet tranform
def dwt(data, fs, frange, wavelet=morlet, reflection=False):
    """wavelet tranform decomposition.

    Syntax: Dwt = dwt(data, fs, frange, wavelet, reflection)

    Keyword arguments:
    data       -- (numpy.ndarray) 1D or 2D array. for 2D array, columns as
                  observations, rows as raw data.
    fs         -- (int) sampling rate
    frange     -- (numpy.ndarray) target frequencies
    wavelet    -- (function) wavelet function [default: morlet]
    reflection -- (bool) perform data reflection, to compensate the edge effect
                  [default: False]

    Return:
    Dwt        -- (numpy.ndarray, dtype="complex") wavelet decomposition result

    """

    if np.ndim(data) == 1:
        data = np.reshape(data, (1, len(data)))

    if reflection:
        data_flip = np.fliplr(data)
        data_fft = np.hstack((data_flip, data, data_flip))
    else:
        data_fft = data

    nConv = np.size(data_fft, -1) + int(2*fs)
    fft_data = np.fft.fft(data_fft, nConv)

    Dwt = np.zeros((np.size(frange), np.size(data, 0), np.size(data, 1)), dtype="complex")

    for idx, F in enumerate(frange):
        fft_wavelet = np.fft.fft(wavelet(F, fs), nConv)
        conv_wave = np.fft.ifft(fft_wavelet * fft_data, nConv)
        conv_wave = conv_wave[:, fs:-fs]

        if reflection:
            Dwt[idx, :, :] = conv_wave[:, np.size(data, 1):-np.size(data, 1)]
        else:
            Dwt[idx, :, :] = conv_wave

    return Dwt


def dwt_power(dwtresult, fs,  zscore=False, baseline=None, gaussian_sigma=0):
    """calcuate the total power from the result of dwt

    Syntax: Pxx = dwt_power(dwtresult, zscore, dbcalibration)

    Keyword arguments:
    dwtresult -- (numpy.ndarray, dtype="complex") the 3D result from dwt function
    fs        -- (int) sampling rate
    zscore    -- (bool) normalize the db result by z-score normalization
                 [default: True]
    baseline  -- (tuple(float, float)) normalize the db result
                 by baseline normalization
                 [default: None]

    Return:
    Pxx       -- (numpy.ndarray) total power
    """

    # generate power and averaged across tirlas (axis 1)
    raw_pxx = np.mean(np.abs(dwtresult) ** 2.0, 1)
    
    if baseline != None:
        starter = int(baseline[0]*fs)
        gap = int((baseline[1] - baseline[0])*fs)
        _base = raw_pxx[:, starter:(starter+gap)]
    else:
        _base = raw_pxx

    if not zscore:
        _baseline = np.mean(_base, 1)
        _baseline = np.reshape(_baseline, (np.size(_baseline, 0), 1))
        Pxx = 10 * np.log10(raw_pxx / _baseline)
    elif zscore:
        mu = np.reshape(np.mean(_base, 1), (np.size(_base, 0), 1))
        sig = np.reshape(np.std(_base, 1), (np.size(_base, 0), 1))
        Pxx = (raw_pxx - mu) / sig
    else:
        Pxx = np.log10(raw_pxx)
        
    if gaussian_sigma > 0:
        _smooth = np.zeros_like(Pxx)
        for ridx in range(np.size(Pxx, 0)):
            _smooth[ridx, :] = gaussianwind(Pxx[ridx, :], fs, gaussian_sigma)
        Pxx = _smooth
        
    return Pxx

def dwt_itpc(dwtresult, itpcz=False, weights=None):
    """Calculate the inter-trial phase clustering from the dwt result

    Syntax: ITPC = dwt_itpc(dwtresult, zscore, weights)

    Keyword arguments:
    dwtresult -- (numpy.ndarray, dtype="complex") 3D complex array from dwt function
    itpcz     -- (bool) flag for ITPCz analysis [default: False]
    weights   -- (numpy.ndarray) weights for wITPCz analysis [default: None] #TODO

    Return:
    ITPC -- (numpy.ndarray) iter-trial pahse clustering result
    """
    unit = dwtresult / np.abs(dwtresult)
    ITPC = np.abs(np.sum(unit, 1) / np.size(dwtresult, 1))
    
    if itpcz == True:
        result = ITPC**2 * np.size(dwtresult, 1)
    else:
        result = ITPC
    
    return result


##### ARCHIVE #####

## Taper
def han(timepoints):
    """Han Taper function. i.e. shifted half cosine."""
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.linspace(0, 1, timepoints))


## stfft
def stfft(data, nwindow, noverlap, fs, taper=han, rho=2):
    """Perform short time fast fourier transformation

    Syntax: (Stfft, Tspec) = stfft(data, nwindow, noverlap, fs, taper, rho)

    Keyword arguments:
    data     -- (numpy.ndarray) 1D or 2D array. for 2D array, columns as
                observations, rows as raw data.
    nwindow  -- (int) fft window size, as number of data points.
    noverlap -- (int) overlap points between two windows
    fs       -- (int) sampling frequency
    taper    -- (function) taper function, take <int> as input. [default: han]
    rho      -- (int) density of fft readout frequency,
                relative to sampling frequency. [default: 2]

    Return:
    Stfft    -- (numpy.ndarray, dtype="complex") stfft result, in complex form.
    Tspec    -- (numpy.ndarray) time point of each stfft time bin.

    """

    step = nwindow - noverlap
    start = nwindow // 2
    nstep = (np.size(data, -1) - nwindow) // step

    Tspec = np.linspace(start, step * nstep, nstep) / fs
    Stfft = np.zeros((np.size(data, 0), rho * 500, nstep))

    taperl = taper(nwindow)
    for idx in range(nstep):
        temp = data[(slice(None), slice(idx*step, idx*step+nwindow))] * taperl
        entry = np.fft.fft(temp, n=rho*fs)
        Stfft[(slice(None), slice(None), idx)] = entry

    return Stfft, Tspec
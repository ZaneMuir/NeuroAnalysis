import scipy.signal as signal

def _butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def _bessel_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.bessel(order, normal_cutoff, btype='highpass')
    return b, a


def bessel_highpass_filter(data, cutoff, fs, order=5):
    b, a = _bessel_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

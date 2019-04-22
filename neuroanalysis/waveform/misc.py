import numpy as np

def create_epoch_bymarker(data, marker, roi, fs, mbias=0):
    gap = int(np.ceil((roi[1] - roi[0]) * fs))
    result = np.zeros((np.size(data, 0), gap, len(marker)), dtype=data.dtype)
    for midx, eachm in enumerate(marker):
        start = int(np.floor((eachm + roi[0] + mbias) * fs))
        result[:, :, midx] = data[:, start:start+gap]
    return result

def create_1d_epoch_bymarker(data, marker, roi, fs, mbias=0):
    gap = int(np.ceil((roi[1] - roi[0]) * fs))
    result = np.zeros((len(marker), gap), dtype=data.dtype)
    for midx, eachm in enumerate(marker):
        start = int(np.floor((eachm + roi[0] + mbias) * fs))
        result[midx, :] = data[start:start+gap]
    return result

def detect_cross_pnt(arr, thr, way='up', gap=1):
    """
    detect the data rise/down point, returns the index of the
    point right above the threshold.

    arguments:
    - arr: data array (1d)
    - thr: threshold (scale)

    key arguments:
    - way: either be "up" or "down", for data rise/ data down respectively.
    - gap: the least points between two valid markers.

    returns:
    - _marker_idx: index array (1d)
    """

    _idx, = np.where(arr > thr)
    _idx_diff, = np.where(np.diff(_idx) > 1)
    _idx_repo = np.hstack((_idx[0], _idx[_idx_diff], _idx[_idx_diff+1], _idx[-1]))

    if way == 'up':
        _check = lambda x, i: x[i-1] < thr < x[i] #< x[i+1]
    elif way =='down':
        _check = lambda x, i: x[i-1] > x[i] > x[i+1]
    else:
        raise ValueError("unknown `way` value.")

    _idx_repo.sort()
    _result = []
    _previous = -9999
    for idx in _idx_repo:
        try:
            if _check(arr, idx) and (idx - _previous > gap):
                _result.append(idx)
                _previous = idx
        except IndexError:
            pass

    return _result

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
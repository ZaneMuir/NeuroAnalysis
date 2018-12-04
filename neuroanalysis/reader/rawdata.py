import numpy as np

class RawData(object):
    def __init__(self):
        super().__init__()
        self.data = np.zeros((0,0,0))
        self.freq = 0.0
        pass
    
    def chunk_bymarker(self, marker, roi, mbias=0):
        ngap = int(np.ceil((roi[1] - roi[0]) * self.freq))

        _result = np.zeros((np.size(self.data, 0), ngap, len(marker)), dtype=self.data.dtype)
        for _idx, _marker in enumerate(marker):
            _start = int(np.floor((_marker + mbias + roi[0]) * self.freq))
            _result[:,:,_idx] = self.data[:, _start:_start+ngap]

        return _result
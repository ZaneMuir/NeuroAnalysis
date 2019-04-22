from .rawdata import RawData
from .edfdata import EDFData

def loadedf(filename, mode='headeronly'):
    _t = EDFData(filename)
    _t.load(mode=mode)
    return _t
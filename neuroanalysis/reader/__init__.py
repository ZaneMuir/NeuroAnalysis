__all__ = [
    "loadedf"
]

from .rawdata import RawData
from .edfdata import EDFData

def loadedf(filename, expname):
    return EDFData(filename, expname)
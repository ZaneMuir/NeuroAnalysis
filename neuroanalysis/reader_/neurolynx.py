import numpy as np
import re


class CscReader(object):
    """Neurolynx csc file reader

Unless you want to sort the spike from the sampling data,
you shouldn't use this reader.

Attributes:
    - \_time: timeline in numpy.ndarray
    - \_csc:  analogy voltage in numpy.ndarray
    - \_raw:  raw data

Example:

.. code-block::python
    >>> CscReader("path/to/csc/file")

    >>> from neuroanalysis import reader
    >>> mycsc = reader.neurolynx_read_csc("path/to/csc/file")
    >>> mycsc._csc
    >>> mycsc._time

    
"""
    def __init__(self, filename, with_analogy=True):
        """Denoted as reader.neurolynx_read_csc"""
        with open(filename, 'rb') as _cscfile:
            self._header = ''.join([chr(i)
                                    for i in _cscfile.read(2**14) if i != 0])
            # The format for a .ncs files according the the neuralynx docs is
            # uint64 - timestamp in microseconds
            # uint32 - channel number
            # uint32 - sample freq
            # uint32 - number of valid samples
            # int16 x 512 - actual csc samples
            dt = np.dtype([('time', '<Q'), ('channel', '<i'), ('freq', '<i'),
                           ('valid', '<i'), ('csc', '<h', (512,))])
            # five points for fast numpy dtype reading
            self._raw = np.fromfile(_cscfile, dt)

        self._ADBitVolts = float(self.getAttribute("ADBitVolts"))
        self._csc = self._raw['csc'].reshape((self._raw['csc'].size,))  # one-dimension
        self._csc = self._csc * 1e6 * self._ADBitVolts
        if self.getAttribute("InputInverted") == 'True':
            self._csc = - self._csc
        self._time = self.__get_time()
        return

    def getAttribute(self, attr):
        """
Get the key-value in the header.

Including:
    - ADBitVolts
        """
        __parser = r"-{attr} (.*?)\r\n".format(attr=attr)
        ans = re.findall(__parser, self._header)
        if len(ans) == 1:
            return ans[0].strip(' ')
        else:
            return False

    def __get_time(self):
        ts = np.zeros(self._csc.shape)
        ts[::512] = self._raw['time']
        xo = np.arange(0, ts.size)
        ts = np.interp(xo, xo[::512], ts[::512])
        # the last few are just filled with a constant, so increment them
        ts[-511:] = ts[-512] + (1 + np.arange(511)) * (ts[512] - ts[0]) / 512.0
        return ts

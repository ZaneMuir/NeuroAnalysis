"""
EDF/EDF+ file manipulation

author: Yizhan Miao
email: yzmiao@protonmail.com
last update: Apr 22 2019
"""

import numpy as np
from .rawdata import AbstractChannel, RawData

class EDFChannel(AbstractChannel):
    
    def __init__(self, name, index, notes, frequency, 
                 physical_unit, physical_dimension, nsamp,
                 value):
        super().__init__()
        self.name = name
        self.index = index
        self.notes = notes
        self.frequency = frequency
        self.physical_unit = physical_unit
        self.physical_dimension = physical_dimension
        self.nsamp = nsamp
        self.value = value
        

class EDFData(RawData):
    """
    EDF file handler.
    """
    
    def __init__(self, filename):
        super().__init__(filename)
    
    def load(self, mode='headeronly', index=None):
        """
        load edf file
        
        modes:
        - headeronly [default]: only import file headers and channel headers
        - all: import everything
        - channel: only import single channel, data would be return as 
                   ndarray, and won't store in class.
        """
        
        _file = open(self.filename, 'rb')
        if mode in ['headeronly', 'all']:
            _file_header_buffer = _file.read(256)
            self.meta = {
                "version": int((_file_header_buffer[0:8]).decode('utf-8').strip()),
                "patient_info": (_file_header_buffer[8:88]).decode('utf-8').strip(),
                "record_info": (_file_header_buffer[88:168]).decode('utf-8').strip(),
                "start_date": (_file_header_buffer[168:176]).decode('utf-8').strip(),
                "start_time": (_file_header_buffer[176:184]).decode('utf-8').strip(),
                "header_length": int((_file_header_buffer[184:192]).decode('utf-8').strip()),
                "_reserved": (_file_header_buffer[192:236]).decode('utf-8').strip(),
                "record_length": int((_file_header_buffer[236:244]).decode('utf-8').strip()),
                "record_duration": float((_file_header_buffer[244:252]).decode('utf-8').strip()),
                "channel_number": int((_file_header_buffer[252:]).decode('utf-8').strip()),
            }
            
            self.continuous_channels = []
            _channel_header_buffer = _file.read(self.meta['header_length']-256)
            _chn = self.meta["channel_number"]
            for idx in range(_chn):

                _label = _channel_header_buffer[16*(idx):16*(idx+1)].decode('utf-8').strip()
                _trans = _channel_header_buffer[80*(idx)+_chn*16:80*(idx+1)+_chn*16].decode('utf-8').strip()

                _phdim = _channel_header_buffer[8*(idx)+_chn*96:8*(idx+1)+_chn*96].decode('utf-8').strip()
                _phmin = float(_channel_header_buffer[8*(idx)+_chn*104:8*(idx+1)+_chn*104].decode('utf-8').strip())
                _phmax = float(_channel_header_buffer[8*(idx)+_chn*112:8*(idx+1)+_chn*112].decode('utf-8').strip())

                _dimin = int(_channel_header_buffer[8*(idx)+_chn*120:8*(idx+1)+_chn*120].decode('utf-8').strip())
                _dimax = int(_channel_header_buffer[8*(idx)+_chn*128:8*(idx+1)+_chn*128].decode('utf-8').strip())

                _t_prefl =     _channel_header_buffer[8*(idx)+_chn*136:8*(idx+1)+_chn*136].decode('utf-8').strip()
                _t_nsamp = int(_channel_header_buffer[8*(idx)+_chn*216:8*(idx+1)+_chn*216].decode('utf-8').strip())
                _t_reser =     _channel_header_buffer[32*(idx)+_chn*224:32*(idx+1)+_chn*224].decode('utf-8').strip()


                self.continuous_channels.append(EDFChannel( 
                    name = _label,
                    index = None,
                    notes = None,
                    frequency = int(_t_nsamp / self.meta['record_duration']),
                    physical_unit = (_phmax - _phmin) / (_dimax - _dimin),
                    physical_dimension = _phdim,
                    nsamp = _t_nsamp,
                    value = None))
        else:
            pass # nothing
        
        if mode in ['all']:
            _temp = np.frombuffer(_file.read(), dtype='i2').reshape((self.meta['record_length'], self.meta['channel_number'], -1))
            for idx in range(len(self.continuous_channels)):
                self.continuous_channels[idx].value = _temp[:, idx, :].flatten()

        elif mode in ['channel']:
            assert not isinstance(index, type(None)), "channel index not valid!"
            
            _nsamp = self.continuous_channels[index].nsamp
            _chn = self.meta['channel_number']
            
            _buffer = []
            for ridx in range(a.meta['record_length']):
                _offset = a.meta['header_length'] + _nsamp*2*chidx + _chn*_nsamp*2*ridx
                _file.seek(_offset)
                _buffer.append(_file.read(_nsamp*2))

            _file.close()
            return np.frombuffer(b''.join(_buffer), dtype='i2')
        
        _file.close()
        
        return
            
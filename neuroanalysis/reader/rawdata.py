"""
basic protocols for data io.

author: Yizhan Miao
email: yzmiao@protonmail.com
last update: Apr 22 2019
"""

import numpy as np
import h5py

class AbstractChannel(object):
    """
    prototype class for abstract channels
    """
    
    def __init__(self, name = None, index = None, notes = None, frequency = None, 
                 physical_unit = None, physical_dimension = None, value = None):
        """
        initialization
        
        should include:
        - name
        - index
        - physical_dimension: name of physical unit, e.g. "mV"
        - physical_unit: corresponding value of each digital value to physical value
        - value: digital signal values or another self-custom values
        """
        
        self.name = name
        self.index = index
        self.notes = notes
        self.frequency = frequency
        self.physical_unit = physical_unit
        self.physical_dimension = physical_dimension
        self.value = value
        
    def serialize(self):
        return {
            'name': self.name,
            'index': self.index,
            'notes': self.notes,
            'frequency': self.frequency,
            'physical_unit': self.physical_unit,
            'physical_dimension': self.physical_dimension,
            'value': self.value
        }

class RawData(object):
    """
    prototype class for raw data.
    
    - __init__(self, filename)
    - load(self)
    - save(self)
    
    """
    
    def __init__(self, filename, **kwargs):
        """
        initialization
        
        should include:
        - filename
        - meta: dictionary of file headers
        - event_channels: list of AbstractChannel class, meta and data of each event channel
        - spike_channels: list of AbstractChannel class, meta and data of each spike channel
        - continuous_channels: list of AbstractChannel class, meta and data of each continous channel
        """
        self.filename = filename
        self.meta = {}
        self.event_channels = []
        self.spike_channels = []
        self.continuous_channels = []
        
    def load(self, **kwargs):
        pass
    
    def save(self, **kwargs):
        pass
    
    def export_hdf5(self, filename, **kwargs):
        """
        export to hdf5 format dataset
        """
        
        _h5file = h5py.File(filename, 'w')
        _h5file.create_dataset('origin', data=self.filename)
        
        _meta = _h5file.create_group('meta')
        for key, val in self.meta.items():
            _meta.create_dataset(key, data=val)
        
        def _export_channels(channels, group_name):
            _subgroup = _h5file.create_group(group_name)
            for each in channels:
                _cont_chan_name = each.name if each.name != None else '%03d'%each.index
                _cont_chan = _subgroup.create_group(_cont_chan_name)
                for key, val in each.serialize().items():

                    if isinstance(val, type(None)):
                        _cont_chan.create_dataset(key, data=np.nan)
                    elif key == 'value':
                        _cont_chan.create_dataset(key, data=val, **kwargs)
                    else:
                        _cont_chan.create_dataset(key, data=val)
                        
                        
        _export_channels(self.event_channels, 'event')
        _export_channels(self.spike_channels, 'spike')
        _export_channels(self.continuous_channels, 'continuous')
        
        _h5file.close()
    
    def restore_hdf5(self, filename=None, importAll=True):
        """
        restore from hdf5 format dataset
        """
        if filename == None:
            filename = self.filename
            
        with h5py.File('test.h5', 'r') as _f:
            self.filename = _f['origin'].value
            _meta = {}
            for key, val in _f['meta'].items():
                _meta[key] = val.value
            self.meta = _meta

            def _restore_channels(name, importdata=True):
                _channels = []
                for _ch_name in _f[name].keys():
                    _c = {}
                    for key, val in _f['%s/%s'%(name, _ch_name)].items():
                        if not importdata and key == 'value':
                            continue
                        _c[key] = val.value
                    _ch = AbstractChannel(**_c)
                    _channels.append(_ch)
                return _channels
            
            self.continuous_channels = _restore_channels('continuous', importAll)
            self.spike_channels = _restore_channels('spike', importAll)
            self.event_channels = _restore_channels('event', importAll)
            
    def restore_hdf5_channel(self, chtype, chname):
        pass  # TODO
    
    def getchannel_byname(self, channels, name):
        try:
            if channels == 'continuous':
                return list(filter(lambda x:x.name == name, a.continuous_channels))[0]
            if channels == 'spike':
                return list(filter(lambda x:x.name == name, a.spike_channels))[0]
            if channels == 'event':
                return list(filter(lambda x:x.name == name, a.event_channels))[0]
            else:
                return None
        except IndexError:
            return None
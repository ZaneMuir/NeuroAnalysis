#!/usr/bin/env python3
# date: 2018-04-16
# authors: {zanemuir1995,}@gmail.com

import pandas as pd
import numpy as np
# import scipy.io
import h5py
import os

class SpikeUnit(object):
    """Storing information and data for each channel."""
    def __init__(self, session, mouse_id, channel, spike_train):
        """Create a new SpikeUnit Object.

        You wouldn't normally create a SpikeUnit object yourself, this is done
        for you when retreiving a mat file from your data directory.
        """
        self.session = session          # string ::
        self.mouse_id = mouse_id        # string ::
        self.channel = channel          # string ::
        self.spike_train = spike_train  # array  ::

def marker_validity(table, train, thresh=2.0):
    """Check .csv marker and .mat marker are valid or not.

    Method:
        the time shift between the first and the last marker of .csv and .mat
        file shall be less than thresh.

    Args:
        table:  the .csv marker in pd.DataFrame
        train:  the .mat marker in np.array
        thresh: the threshold, as float [optional, default: 2.0]

    Returns:
        shift:  the shift value. i.e. how many markers in .csv is not recorded
                in .mat markers.

    Raises:
        ValueError: when it doesn't pass the validity test.
    """
    shift = len(table)-2 - len(train)

    if shift >= 0:
        start_d = train[0] - table.time[1]
        end_d = train[-1] - table.time[len(table)-2-shift]
        if np.abs(start_d - end_d) <= thresh:
            return shift  # valid
        else:
            raise ValueError("marker value not match!")
    else:
        raise ValueError("electrode markers exceed stimulus markers!")

    return False


class SpikeMarker(object):
    """Storing and parsing marker information of each session."""
    def __init__(self, session, mouse_id, marker_table, marker_train,
                 mark_chunker=None):
        """Create a new SpikeMarker Object.

        You wouldn't normally create a SpikeMarker object yourself, this is done
        for you when retreiving a csv file from your data directory.

        Specially, the marker_table shall be a pandas.DataFrame, with coloumns
        ("time", "marker"); if you have a different layout, you should write
        your own ```mark_chunker``` function, which returns a tuple:
        (pandas.DataFrame('time','marker'), dict{markname: timearray[]}).
        """
        self.session = session          # string ::
        self.mouse_id = mouse_id        # string ::

        self._raw_table = marker_table  # pd.DataFrame(('time','mark'))
        self._raw_train = marker_train  # np.array

        if mark_chunker:
            self.table_marker, self.chunked_marker = mark_chunker(marker_table, marker_train)
        else:
            self.table_marker, self.chunked_marker = self._default_chunker()

        return

    def _default_chunker(self, skip=["START", "QUIT"]):
        _raw_table = self._raw_table
        _raw_train = self._raw_train
        shift = marker_validity(_raw_table, _raw_train)
        print(shift)
        if shift is False:
            raise ValueError("markers not valid! Please check it.")
        _table = _raw_table[1:-1-shift]
        # FIXME: Try using .loc[row_indexer,col_indexer] = value instead
        _table.time = _raw_train
        _uniques = _table.marker.unique()

        _chunking = {}
        for item in _uniques:
            if item in skip:
                continue
            _chunking[item] = _table[_table.marker == item].time.values

        return _table, _chunking


def import_spike_train_data(session, mouse_id, mat, csv='',
                            data_dir='data/', mat_marker_channel='DIG01',
                            csv_chunker=None):
    """Import .mat and .csv data.

    Args:
        session:    session name in string.
        mouse_id:   mouse name in string.
        mat:        .mat data file path.
        csv:        .csv data file path. [optional, default: None]
        data_dir:   data directory path. [optional, default: data/]
        mat_marker_channel: the marker channel name in .mat file.
                            [optional, default: DIG01]
        csv_chunker: custom csv chunker function [optional, default: None]

    Returns:
        spike_trains:   dict{channel_name: SpikeUnit}
        spike_marker:   SpikeMarker
    """
    _mat_file = os.path.join(data_dir, mat)

    _spike_marker_raw = None
    _spike_trains_raw = {}
    if isinstance(csv, pd.DataFrame):
        _marker_table = csv
    else:
        _csv_file = os.path.join(data_dir, csv)
        _marker_table = pd.read_csv(_csv_file) if csv else None

    with h5py.File(_mat_file,"r") as f:
        for channel in f.keys():
            if channel == mat_marker_channel:
                _spike_marker_raw = f.get(channel)['times'].value[0]
            else:
                _spike_trains_raw[channel] = f.get(channel)['times'].value[0]

    spike_trains = {}
    spike_marker = SpikeMarker(session, mouse_id, _marker_table, _spike_marker_raw, csv_chunker)
    for (channel, train) in _spike_trains_raw.items():
        spike_trains[channel] = SpikeUnit(session, mouse_id, channel, train)

    return spike_trains, spike_marker

import scipy.io as spio
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import pyarrow

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    def _check_keys(d):
        '''
        checks if entries in dictionary are mat_objects. If yes,
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _todict(matobj):
        '''
        A recursive function which constructs from mat_objects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif isinstance(elem, np.ndarray):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif isinstance(sub_elem, np.ndarray):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

#load .mat file, use self created loadmat function instead of build-in library
data = loadmat('Test_1_run_1.mat')

#choose measurement
mosfet = data['measurement']

#choose steadyState
avgMosfet = mosfet['steadyState']

#de-nest nested structure
dataframe = json_normalize(avgMosfet)

dataframe.columns = ['date',
                     'nanosec_time',
                     'timeEpoch',
                     'supplyVoltage',
                     'packageTemperature',
                     'drainSourceVoltage',
                     'drainCurrent',
                     'flangeTemperature']

#transfer to parquet file
dataframe.to_parquet('MOSFET.parquet', compression='gzip')



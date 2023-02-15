

import os
import pandas as pd


def collect_inputs(*args, **kwargs):
    pass


class EUZOnalInput():
    '''
    All ReEDS India inputs.
    '''

    def __init__(self, file, header='infer', col_names=None):
        self.file = file
        self.df = None

    def get_data(self, *args, **kwargs):
        if self.df is None:
            self.read_data(*args, **kwargs)
        return self.df.copy()


class EntsoEAPIInput(EUZOnalInput):
    '''
    ReEDS India .csv input files.
    '''
    def read_data(self, *args, **kwargs):
        pass


# All inputs for the India Zonal PCM based on ReEDS-India data
INPUTS = {
    
}

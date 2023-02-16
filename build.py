import os
import pandas as pd
import pysaint as ps
import datetime as dt
import shutil
from data import INPUTS
from helpers import saint_dll
from helpers import write_pickle_file, read_pickle_file

def get_model(*args, **kwargs):
    if kwargs['build_type'] == 'false':
        model = load_model(*args, **kwargs)
    else:
        model = build_model(*args, **kwargs)
    return model

def load_model(*args, **kwargs):
    return read_pickle_file('india_zonal', kwargs['out_dir'])


def build_model(*args, **kwargs):
    pass
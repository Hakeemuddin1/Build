import os
import shutil
import pandas as pd
import pysaint as ps
import datetime as dt
from data import INPUTS
from helpers import saint_dll
from helpers import write_pickle_file, read_pickle_file


def get_nodes(*args, **kwargs):
    """Read nodes from the bidding zones
    """
    nodes = INPUTS['nodes'].get_data()
    return nodes


def get_model(*args, **kwargs):
    if kwargs['build_type'] == 'false':
        model = load_model(*args, **kwargs)
    else:
        model = build_model(*args, **kwargs)
    return model


def load_model(*args, **kwargs):
    pass


def build_model(*args, **kwargs):
    # Get all object inputs
    # Node properties
    nodes = get_nodes(*args, **kwargs)

    # Use pysaint to build dataset
    eu_zonal = ps.create_electric_dataset()

    # Add an ENET object
    eu_zonal.add_object(
        'ENET',
        'EU_Zonal'
    )

    # Add nodes to dataset
    eu_zonal.add_objects_from_dataframe(
        nodes,
        'Name',
        ['X', 'Y'],
        'ENO',
    )

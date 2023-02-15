
from ctypes import *
import datetime
import os
import pickle
import numpy as np
import shutil
import pandas as pd

saint_dll = cdll.LoadLibrary(
    r"C:/Program Files/encoord/SAInt-v3/SAInt-API.dll")
saint_dll.evalCmdStr('from SAInt_API.Library import SolverType')
saint_dll.evalStr.restype = c_wchar_p
saint_dll.evalInt.restype = c_int
saint_dll.evalBool.restyhpe = c_bool
saint_dll.evalFloat.restype = c_float


def create_output_directory(*args, **kwargs):
    """
    Creating output directory for test model version
    """

    if kwargs['build_type'] == 'false':
        if kwargs['model_path'] == 'latest_test':
            out_dir = os.path.join(
                'io',
                'outputs',
                'testing',
                get_most_recent_version()
            )
        else:
            out_dir = kwargs['model_path']
    elif kwargs['build_type'] == 'test':
        now = datetime.datetime.now()
        dest_folder = '{}y_{}m_{}d_{}h_{}m'.format(
                        str(now.year),
                        str(now.month),
                        str(now.day),
                        str(now.hour),
                        str(now.minute)
        )

        os.mkdir(os.path.join('io', 'outputs', 'testing', dest_folder))
        out_dir = os.path.join('io', 'outputs', 'testing', dest_folder)
    elif kwargs['build_type'] == 'milestones':
        dest_folder = 'V{}.{}'.format(kwargs['version'], kwargs['milestones'])
        try:
            os.mkdir(os.path.join('io', 'outputs', 'milestones', dest_folder))
        except FileExistsError:
            pass
        out_dir = os.path.join('io', 'outputs', 'milestones', dest_folder)
    # TODO: Add elif for official builds
    else:
        print('Only build_type: "test" & "milestones" are currently supported')

    return out_dir


# Create a pickle file or open a saved pickle file
def write_pickle_file(input, filename, out_dir):
    """
    Write data in script to pickle file for later access

    Parameters
    ----------
    input : any
        Any data that is desired to be stored as a pickle file
    filename : str
        Name for pickle file
    out_dir : str
        Directory to location where pickle file will be stored
    """
    with open(os.path.join(out_dir, filename+'.pkl'), 'wb') as outp:
        pickle.dump(input, outp, pickle.HIGHEST_PROTOCOL)


def read_pickle_file(filename, path):
    """
    Read a pickle file and supply it as the output

    Parameters
    ----------
    filename : str
        name of the pickle file to be read
    path : str
        directory where the pickle file is stored

    Returns
    -------
    varies
        type is dependent on original data type
    """
    with open(os.path.join(path, filename+'.pkl'), 'rb') as inp:
        output = pickle.load(inp)
    return output


def get_most_recent_version():
    """
    Gets the most recent version of the dataset from testing folder based on
    folder name which is a timestamp.

    Returns
    -------
    str
        Most recent transformation of the dataset
    """
    test_versions = os.listdir(os.path.join('io', 'outputs', 'testing'))
    datetimes = []
    for version in test_versions:
        timestamp = version.split('_')
        year = int(timestamp[0][:-1])
        month = int(timestamp[1][:-1])
        day = int(timestamp[2][:-1])
        hour = int(timestamp[3][:-1])
        minute = int(timestamp[4][:-1])
        datetimes.append(datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        ))
    datetimes = np.array(datetimes)
    most_recent_version = max(datetimes)
    return '{}y_{}m_{}d_{}h_{}m'.format(
        str(most_recent_version.year),
        str(most_recent_version.month),
        str(most_recent_version.day),
        str(most_recent_version.hour),
        str(most_recent_version.minute)
    )


def transform(chars):
    """
    Parses the string returned by the SAInt API

    Parameters
    ----------
    chars : str
        SAInt API calls return a string that needs to be parsed before use

    Returns
    -------
    list
        Parsed data that can now be easily used/manipulated in python
    """
    chars = chars.split(',')
    chars = [m.replace('[', '') for m in chars]
    chars = [m.replace(']', '') for m in chars]
    chars = [m.replace("'", '') for m in chars]
    chars = [m.strip() for m in chars]
    return chars


def get_network_prop(obj_type, name, prop, dtype=float):
    result = saint_dll.evalStr('{}.{}.{}'.format(obj_type, name, prop))
    if name == '%':
        result = transform(result)
    if dtype == float:
        if isinstance(result, list):
            result = [float(x) for x in result]
        else:
            float(result)
    return result


def get_names(obj_type, props):
    raw = []
    for prop in props:
        raw.append(get_network_prop(obj_type, '%', prop, dtype=str))
    return pd.DataFrame(index=props, data=raw).T


# TODO: get gentype
def get_metadata():
    gen_metadata_file = os.path.join('Results', 'gen_metadata.pkl')
    if not os.path.isfile(gen_metadata_file):
        gen_metadata = get_names('GEN', ['Name', 'NodeName', 'Info'])
        fuel_names = get_names('FGEN', ['Name', 'FuelName'])
        zone_names = get_names('ENO', ['Name', 'ZoneName'])
        zone_names.rename(columns={'Name': 'NodeName'}, inplace=True)
        gen_metadata = gen_metadata.merge(
            zone_names, on='NodeName', how='left'
        )
        gen_metadata = gen_metadata.merge(fuel_names, on='Name', how='left')
        gen_metadata['Info'] = gen_metadata['Info'].replace({
            'HYDRO_DISP': 'HYDRO',
            'HYDRO_ROR': 'HYDRO',
            'landfill_gas': 'biopower'
            }
        )
        for i in gen_metadata.index:
            if gen_metadata.loc[i, 'Info'] == '-':
                gen_metadata.loc[i, 'Info'] = gen_metadata.loc[
                    i, 'Name'
                ].split('_')[0]
        gen_metadata.rename(columns={'Info': 'Group'}, inplace=True)
        with open(gen_metadata_file, 'wb') as outp:
            pickle.dump(gen_metadata, outp, pickle.HIGHEST_PROTOCOL)
    else:
        with open(gen_metadata_file, 'rb') as inp:
            gen_metadata = pickle.load(inp)
    return gen_metadata


def copy_files(from_path, to_path, exclude=None):
    # Fetching the list of all the files
    files = os.listdir(from_path)
    files.remove(exclude)

    # Fetching all the files to directory
    for filename in files:
        shutil.copy(
            os.path.join(from_path, filename),
            os.path.join(to_path, filename)
        )


import argparse
import logging
import os
import traceback

from build import get_model
from data import collect_inputs
from helpers import create_output_directory
from qa import quality_assurance


def EU_Zoanl(*args, **kwargs):
    """
    Build, run, and validate the India Zonal PCM
    """
    collect_inputs(*args, **kwargs)
    india_zonal = get_model(*args, **kwargs)
    quality_assurance(india_zonal, **kwargs)
    # run model()
    # process_results()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="""Running India Zonal PCM"""
    )
    # Use dictionary settings as args
    parser.add_argument("--version", default='0', help='some help string')
    parser.add_argument("--milestones", default='0')
    parser.add_argument("--build_type", default='false')
    parser.add_argument("--model_path", default='latest_test')
    parser.add_argument("--year", default=2022)
    parser.add_argument("--scen_name", default='reference_2022')
    args = parser.parse_args()
    SETTINGS = args.__dict__.copy()

    log_file = 'error.txt'
    logging.basicConfig(filename=log_file, level=logging.ERROR)
    logger = logging.getLogger(__name__)

    try:
        SETTINGS['out_dir'] = create_output_directory(**SETTINGS)
        India_Zonal(**SETTINGS)
    except:  # noqa
        logger.error(traceback.format_exc())
    logging.shutdown()
    if os.stat(log_file).st_size == 0:
        os.remove(log_file)

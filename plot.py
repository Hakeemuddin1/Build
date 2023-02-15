
from helpers import read_pickle_file

import os
import matplotlib.pyplot as plt
import pysaint as ps

# TODO: Define once groups are added to the dataset
GROUP_ORDER = []
GROUP_COLORS = []

GENTYPE_ORDER = [
    'NUCLEAR', 'COAL', 'CCGT', 'GASTURBINE', 'OIL', 'GEOTHERMAL',
    'BIOTHERMAL', 'HYDRO', 'WIND', 'PV', 'NONE'
]
GENTYPE_COLORS = [
    'darkred', 'black', 'indianred', 'lightcoral', 'darkgrey', 'brown',
    'darkgreen', 'darkblue', 'green', 'orange', 'pink'
]


def stacked_bar(
    df,
    filename,
    out_dir,
    how='GENTYPE',
    plt_title=None,
    lgnd_title=None,
    ylabel=None,
    ymax=None,
    ymin=None
):
    """
    Create a stack plot from a dataframe.

    Parameters
    ----------
    df : pandas DataFrame
        The structure of the dataframe must have the column names as the group
        of the gen type with the entries in the column as the value to plot on
        the stacked plot.
    filename : str
        Desired name to store the plot and plot data as
    out_dir : str
        Directory to where the file should be stored
    how : str, optional
        Tells how the data grouped, by default 'GENTYPE'
    plt_title : str, optional
        Desired name to be displayed as the plot title, by default None
    lgnd_title : str, optional
        Desired name to be displayed as the legend title, by default None
    ylabel : str, optional
        Desired y axis label, by default None
    ymax : int, optional
        Desired maximum value for y axis, by default None
    ymin : int, optional
        Desired minimum value for y axis, by default None
    """
    if how == 'EGRP':
        pass
    if how == 'GENTYPE':
        df = df[GENTYPE_ORDER]
        color = GENTYPE_COLORS
    fig = df.plot.bar(stacked=1, color=color)
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(
        handles[::-1],
        labels[::-1],
        title=lgnd_title,
        bbox_to_anchor=(1, 1),
        loc='upper left'
    )
    if plt_title is not None:
        plt.title(plt_title)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if ymax is not None:
        plt.ylim(0, ymax)
    if ymin is not None:
        plt.ylim(ymin, ymax)
    plt.savefig(os.path.join(out_dir, '{}.pdf'.format(filename)),
                dpi=300,
                bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, '{}.png'.format(filename)),
                dpi=300,
                bbox_inches='tight')
    plt.show()
    df.to_csv(os.path.join(out_dir, '{}.csv'.format(filename)))


def get_merit_order_curve(dataset, out_dir, scen_name, filename):
    """
    Import pickle file containing pysaint dataset and leverage pysaint to
    create a merit order curve for the network

    Parameters
    ----------
    pkl_filename : str
        Name of pickle file without '.pkl'
    scen_name : str
        Name of scenario
    filename : str
        Desired name to store the plot and plot data as
    out_dir : str
        Directory the file should be stored to
    """
    # Use pysaint to get Merit Order Curve
    fig = ps.utils.plot_merit_order(dataset, '{}'.format(scen_name))
    fig.savefig(
        os.path.join(out_dir, '{}.pdf'.format(filename)),
        dpi=300,
        bbox_inches='tight'
    )
    fig.savefig(
        os.path.join(out_dir, '{}.png'.format(filename)),
        dpi=300,
        bbox_inches='tight'
    )
    fig.show()

import argparse
import sys


import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg') # Disables the need for the monitor

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def test():
    print "All Systems Go"
    return 0

"""
def plot(date="TODAY", time=0, layer=0, fileName="NONE"):
    """ Makes a nams plot of the State of Oregon

    date -
    time -
    layer -
    """
    fig = pyplot.figure()

    ax = fig.add_subplot(111)
    bmap = Basemap(projection='merc',
                   resolution='h', area_thresh=1.0,
                   llcrnrlat=40.5833284543, urcrnrlat=47.4999927992,
                   llcrnrlon=-129, urcrnrlon=-123.7265625,
                   ax=ax, epsg=4326)


    lat = data_file.variables['lat']
    lon = data_file.variables['lon']
    x, y = bmap(lon, lat)

    var_u = 'u-component_of_wind_height_above_ground'
    var_v = 'v-component_of_wind_height_above_ground'

    wind_u = data_file.variables[var_u]
    wind_v = data_file.variables[var_v]

    wind_u = wind_u[:, 0, :, :] # All times of u
    wind_v = wind_v[:, 0, :, :] # All times of

    if downsample_ratio == 1:
        length = 3
    elif downsample_ratio == 2:
        length = 4.25

    bmap.barbs(x[::downsample_ratio, ::downsample_ratio],
               y[::downsample_ratio, ::downsample_ratio],
               wind_u[::downsample_ratio, ::downsample_ratio],
               wind_v[::downsample_ratio, ::downsample_ratio],
               ax=ax,
               length=length, sizes=dict(spacing=0.2, height=0.3))
               #barb_increments=dict(half=.1, full=10, flag=50))

    if(fileName == "NONE"):
        fig.savefig("./media/test.png")
    else
        fig.savefig("./media/" + filename + ".png")
    pyplot.close(fig)

    return 1 # Success
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Easy NAMS Plotting.')
    parser.add_argument('task',
                        help='task name',
                        type=str)
    parser.add_argument("-f", '--file',
                        help='File name to store the plot',
                        type=str)
    parser.add_argument("-t", '--time',
                        help='datetime object',
                        type=str)
    parser.add_argument("-d", '--date',
                        help='datetime object',
                        type=str)
    parser.add_argument("-l", '--layer',
                        help='integer',
                        type=int)
    parser.add_argument("-i", '--slice',
                        help='integer',
                        type=int)

    args = parser.parse_args()
    if args.task == "plot":
        plot()
    elif args.task == "test":
        test()
        sys.exit(0)
        #sys.exit(test())

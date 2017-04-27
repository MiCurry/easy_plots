import argparse
import sys

import numpy as np
import scipy
import matplotlib
from scipy.io import netcdf

matplotlib.use('Agg') # Disables the need for the monitor

import matplotlib.pyplot as pyplot
from mpl_toolkits.basemap import Basemap

from download import download

north = "46.5"; south = "41.7"; east = "-116"; west = "-125";

def test():
    print "All Systems Go"
    return 1

def test_plot():
    fig = pyplot.figure()

    ax = fig.add_subplot(111)
    bmap = Basemap(projection='merc',
                   resolution='h', area_thresh=1.0,
                   urcrnrlat=north, llcrnrlat=south,
                   urcrnrlon=east, llcrnrlon=west,
                   ax=ax, epsg=4326)
    return 1

def load_file():
    return netcdf.netcdf_file("data/WIND_2017-04-27.nc")

""" Makes a nams plot of the State of Oregon

date -
time -
layer -
"""
def plot(date="TODAY", time=0, layer=0, fileName="NONE"):
    if fileName == "NONE":
        fileName = download(north = "46.5", south = "41.7", east = "-116", west = "-125")
        data_file = load_file()

    print type(data_file)

    fig = pyplot.figure()

    ax = fig.add_subplot(111)
    bmap = Basemap(projection='merc',
                   resolution='h', area_thresh=1.0,
                   urcrnrlat=float(north), llcrnrlat=float(south),
                   urcrnrlon=float(east), llcrnrlon=float(west),
                   ax=ax, epsg=4326)

    lat = data_file.variables['lat']
    lon = data_file.variables['lon']
    x, y = bmap(lon, lat)

    print "CREATING A WIND PLOT"

    var_u = 'u-component_of_wind_height_above_ground'
    var_v = 'v-component_of_wind_height_above_ground'

    wind_u = data_file.variables[var_u]
    wind_v = data_file.variables[var_v]

    wind_u = wind_u[0, 0, :, :] # All times of u
    wind_v = wind_v[0, 0, :, :] # All times of

    downsample_ratio = 5
    length = 7

    bmap.drawcoastlines()
    bmap.drawstates()

    bmap.barbs(x[::downsample_ratio, ::downsample_ratio],
               y[::downsample_ratio, ::downsample_ratio],
               wind_u[::downsample_ratio, ::downsample_ratio],
               wind_v[::downsample_ratio, ::downsample_ratio],
               ax=ax,
               length=length, sizes=dict(spacing=0.2, height=0.3))
               #barb_increments=dict(half=.1, full=10, flag=50))

    print "WIND PLOT CREATED!"

    time = 0
    height = 0

    fig.savefig("/home/data/plots/WIND_plot-{0}-{1}".format(time, height),
                dpi = 500,
                bbox_inches='tight',
                pad_inches=0,
                transparent=True
                )

    return 1 # Success


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
    if args.task == "download":
        download(north, south, east, west)
    if args.task == "plot":
        plot()
    elif args.task == "test":
        test()
        sys.exit(0)
        #sys.exit(test())

import argparse
import sys
from string import replace
from datetime import datetime, timedelta

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

def load_file(date, height):
    print "Loading File", "data/WIND-"+str(date)+".nc"
    return netcdf.netcdf_file("data/WIND-"+str(date)+".nc")

""" Makes a nams plot of the State of Oregon

date -
time -
layer -
"""
def plot(date="TODAY",
         stride=0,
         height='0',
         layer=0):

    date = datetime.now().date()

    fileName = download(north = "46.5",
                        south = "41.7",
                        east = "-116",
                        west = "-125",
                        height = str(height))

    data_file = load_file(date, height)
    times = data_file.variables['time']
    ref_time = datetime.strptime(times.units, 'Hour since %Y-%m-%dT%H:%M:%SZ')

    """ Plotting """
    for i in range(times.shape[0]):
    #for i in range(4):

        # Create the Plot Figure
        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        # Specifiy the map projection and the latitude and longitude
        bmap = Basemap(projection='merc',
                       resolution='h', area_thresh=1.0,
                       urcrnrlat=float(north), llcrnrlat=float(south),
                       urcrnrlon=float(east), llcrnrlon=float(west),
                       ax=ax, epsg=4326)

        # Find the Latitude and longitude
        lat = data_file.variables['lat']
        lon = data_file.variables['lon']
        x, y = bmap(lon, lat)

        # Pull our the u and v vectors
        wind_v = data_file.variables['v-component_of_wind_height_above_ground']
        wind_u = data_file.variables['u-component_of_wind_height_above_ground']

        # Here we grab only the times we want to plot
        wind_u = wind_u[i, 0, :, :] # All times of u
        wind_v = wind_v[i, 0, :, :] # All times of

        downsample_ratio = 5
        length = 7

        bmap.drawcoastlines()
        bmap.drawstates()
        print "times[i]: ", times[i]
        print "i :", i

        date = ref_time + timedelta(hours=float(times[i]))
        print "Date:", date
        plot_date = str(date.date())
        plot_time = str(date.time())
        plot_date = plot_date.replace(":", "-", 3)
        plot_time = plot_time.replace(":", "-", 3)

        filename = "/home/data/WIND-{0}-{1}.png".format(plot_date, plot_time)
        print filename

        # here is where the plot is created
        bmap.barbs(x[::downsample_ratio, ::downsample_ratio],
                   y[::downsample_ratio, ::downsample_ratio],
                   wind_u[::downsample_ratio, ::downsample_ratio],
                   wind_v[::downsample_ratio, ::downsample_ratio],
                   ax=ax,
                   length=length, sizes=dict(spacing=0.2, height=0.3))
                   #barb_increments=dict(half=.1, full=10, flag=50))

        # And It is saved here!
        fig.savefig(str(filename),
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
    parser.add_argument("-u", '--height',
                        help='height above ground in meters',
                        type=int)
    parser.add_argument("-i", '--slice',
                        help='integer',
                        type=int)

    args = parser.parse_args()
    if args.task == "download":
        download(north, south, east, west, "0")
    if args.task == "plot":
        print "Plotting!"
        plot(height=args.height)
    elif args.task == "test":
        test()
        sys.exit(0)
        #sys.exit(test())

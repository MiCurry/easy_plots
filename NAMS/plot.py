import argparse
import sys

import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg') # Disables the need for the monitor

import matplotlib.pyplot as pyplot
from mpl_toolkits.basemap import Basemap

from download import download

north = 46.5; south = 41.7; east = -116; west = -125;

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

# IDEA: Make this a class
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
                   urcrnrlat=north, llcrnrlat=south,
                   urcrnrlon=east, llcrnrlon=west,
                   ax=ax, epsg=4326)

    # Set up lat and lon variables from the provided file
    tmp = np.loadtxt('./latlon.g218')
    lat = np.reshape(tmp[:, 2], [614,428])
    lon = np.reshape(tmp[:, 3], [614,428])
    x, y = bmap(lon, lat)
    for i in range(0, len(lon)):
        lon[i] = -lon[i]

    var_u = 'u-component_of_wind_height_above_ground'
    var_v = 'v-component_of_wind_height_above_ground'
    landMask = 'Land_cover_0__sea_1__land_surface'

    data_file = open_url(URL)

    wind_u = data_file[var_u][time+104, 0, :, :]
    wind_v = data_file[var_v][time+104, 0, :, :]

    wind_u = np.array(wind_u)
    wind_v = np.array(wind_v)

    print "Wind_u:", wind_u.shape
    print "Wind_v:", wind_v.shape

    # Remove the surface height dimension (Its only 1-Demensional)
    wind_u = np.squeeze(wind_u) # Removes The Surface Height Dimension
    wind_v = np.squeeze(wind_v) # Ditto

    if(1): # Debug
        print "Wind", wind_u, wind_v
        print "Wind_u:", wind_u.shape
        print "Wind_v:", wind_v.shape

    wind_u = data_file[var_u][time+104, 0, :, :]
    wind_v = data_file[var_v][time+104, 0, :, :]

    wind_u = np.squeeze(wind_u) # Squeeze out the time
    wind_v = np.squeeze(wind_v) # Squeeze out the time

    if(1): # Debug
        print "Wind", wind_u, wind_v
        print "Wind_u:", wind_u.shape
        print "Wind_v:", wind_v.shape

    wind_u = np.reshape(wind_u, (614, 428))
    wind_v = np.reshape(wind_v, (614, 428))

    if downsample_ratio == 1:
        length = 3
    elif downsample_ratio == 5:
        length = 7

    bmap.barbs(x[::downsample_ratio, ::downsample_ratio],
               y[::downsample_ratio, ::downsample_ratio],
               wind_u[::downsample_ratio, ::downsample_ratio],
               wind_v[::downsample_ratio, ::downsample_ratio],
               ax=ax,
               length=length)

    if(fileName == "NONE"):
        fig.savefig("./media/test.png")
    else:
        fig.savefig("./media/" + filename + ".png")
    pyplot.close(fig)

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

import numpy as np
import scipy
import matplotlib
import argparse
import numpy
matplotlib.use('Agg') # Disables the need for the monitor

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.io import netcdf
from netCDF4 import Dataset


from download import download

def cel2fahr(temp):
    return temp * 1.8 + 32

def load_file():
    #return netcdf.netcdf_file("/home/data/ROMS_2017-05-11.nc")
    return Dataset("ocean_his_4474_01-Apr-2017.nc.nc")

def sst_function(time_index=0,
                 downsample_ratio=5,
                 north=47.499,
                 south=40.5840806224,
                 east=-123.726199391,
                 west=-129.9):

    data_file = load_file()

    vectorized_conversion = numpy.vectorize(cel2fahr)

    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    # Specifiy the map projection and the latitude and longitude
    bmap = Basemap(projection='merc',
                   resolution='h', area_thresh=1.0,
                   urcrnrlat=float(north), llcrnrlat=float(south),
                   urcrnrlon=float(east), llcrnrlon=float(west),
                   ax=ax, epsg=4326)


    surface_temp = numpy.ma.array(vectorized_conversion( \
                                 data_file.variables['temp'][time_index][39]),
                                 mask=get_rho_mask(data_file))

    longs = data_file.variables['lon_rho'][:]
    lats = data_file.variables['lat_rho'][:]

    #get the max and min temps for the daytem
    #-------------------------------------------------------------------------
    all_day = data_file.variables['temp'][:, 39, :, :]
    min_temp = int(math.floor(cel2fahr(numpy.amin(all_day))))
    max_temp = int(math.ceil(cel2fahr(numpy.amax(numpy.ma.masked_greater(all_day, 1000))))) # REVIEW: Is this right?

    x, y = bmap(longs, lats)

    # calculate and plot colored contours for TEMPERATURE data
    # 21 levels, range from one over min to one under max, as the colorbar caps each have their color and will color
    # out of bounds data with their color.
    #-------------------------------------------------------------------------
    contour_range = ((max_temp - 1) - (min_temp + 1))
    contour_range_inc = float(contour_range)/NUM_COLOR_LEVELS
    color_levels = []
    for i in xrange(NUM_COLOR_LEVELS+1):
        color_levels.append(min_temp+1 + i * contour_range_inc)

    bmap.drawmapboundary(linewidth=0.0, ax=ax)
    overlay = bmap.contourf(x, y, surface_temp, color_levels, ax=ax, extend='both', cmap=get_modified_jet_colormap())


# We are not using the Salt model at this time.
#-------------------------------------------------------------------------
def salt_function(ax, data_file, bmap, key_ax, time_index, downsample_ratio):
    # salt has dimensions ('ocean_time', 's_rho', 'eta_rho', 'xi_rho')
    # s_rho corresponds to layers, of which there are 30, so we take the top one.
    surface_salt = numpy.ma.array(data_file.variables['salt'][time_index][39], mask=get_rho_mask(data_file))

    longs = data_file.variables['lon_rho'][:]
    lats = data_file.variables['lat_rho'][:]

    #get the max and min salinity for the day
    all_day = data_file.variables['salt'][:, 39, :, :]
    min_salt = int(math.floor(numpy.amin(all_day)))
    max_salt = int(math.ceil(numpy.amax(numpy.ma.masked_greater(all_day, 1000))))

    x, y = bmap(longs, lats)

    # calculate and plot colored contours for salinity data
    # 21 levels, range from one over min to one under max, as the colorbar caps each have their color and will color
    # out of bounds data with their color.
    contour_range = ((max_salt - 1) - (min_salt + 1))
    contour_range_inc = float(contour_range)/NUM_COLOR_LEVELS

    color_levels = []
    for i in xrange(NUM_COLOR_LEVELS+1):
        color_levels.append(min_salt+1 + i * contour_range_inc)

    bmap.drawmapboundary(linewidth=0.0, ax=ax)
    overlay = bmap.contourf(x, y, surface_salt, color_levels, ax=ax, extend='both', cmap=get_modified_jet_colormap())

    # add colorbar.
    cbar = pyplot.colorbar(overlay, orientation='horizontal', cax=key_ax)
    cbar.ax.tick_params(labelsize=10)
    cbar.ax.xaxis.label.set_color('white')
    cbar.ax.xaxis.set_tick_params(labelcolor='white')

    locations = numpy.arange(0, 1.01, 1.0/(NUM_COLOR_LEVELS))[::3]    # we just want every third label
    float_labels = numpy.arange(min_salt, max_salt + 0.01, contour_range_inc)[::3]
    labels = ["%.1f" % num for num in float_labels]
    cbar.ax.xaxis.set_ticks(locations)
    cbar.ax.xaxis.set_ticklabels(labels)
    cbar.set_label("Salinity (PSU)")

def currents_function(ax, data_file, bmap, key_ax, time_index, downsample_ratio):
    def compute_average(array):
        avg = numpy.average(array)
        return numpy.nan if avg > 10**3 else avg

    print "Currents Downsample Ratio:", downsample_ratio

    currents_u = data_file.variables['u'][time_index][39]
    currents_v = data_file.variables['v'][time_index][39]
    rho_mask = get_rho_mask(data_file)

    # average nearby points to align grid, and add the edge column/row so it's the right size.
    #-------------------------------------------------------------------------
    right_column = currents_u[:, -1:]
    currents_u_adjusted = ndimage.generic_filter(scipy.hstack((currents_u, right_column)),
                                                 compute_average, footprint=[[1], [1]], mode='reflect')
    bottom_row = currents_v[-1:, :]
    currents_v_adjusted = ndimage.generic_filter(scipy.vstack((currents_v, bottom_row)),
                                                 compute_average, footprint=[[1], [1]], mode='reflect')

    # zoom
    #-------------------------------------------------------------------------
    u_zoomed = crop_and_downsample(currents_u_adjusted, downsample_ratio)
    v_zoomed = crop_and_downsample(currents_v_adjusted, downsample_ratio)
    rho_mask[rho_mask == 1] = numpy.nan
    rho_mask_zoomed = crop_and_downsample(rho_mask, downsample_ratio)
    longs = data_file.variables['lon_rho'][:]
    lats = data_file.variables['lat_rho'][:]

    longs_zoomed = crop_and_downsample(longs, downsample_ratio, False)
    lats_zoomed = crop_and_downsample(lats, downsample_ratio, False)

    u_zoomed[rho_mask_zoomed == 1] = numpy.nan
    v_zoomed[rho_mask_zoomed == 1] = numpy.nan

    x, y = bmap(longs_zoomed, lats_zoomed)

    bmap.drawmapboundary(linewidth=0.0, ax=ax)

    overlay = bmap.quiver(x, y, u_zoomed, v_zoomed, ax=ax, color='black', units='inches',
                          scale=10.0, headwidth=2, headlength=3,
                          headaxislength=2.5, minlength=0.5, minshaft=.9)

    # Multiplying .5, 1, and 2 by .5144 is converting from knots to m/s
    #-------------------------------------------------------------------------
    quiverkey = key_ax.quiverkey(overlay, .95, .4, 0.5*.5144, ".5 knots", labelpos='S', labelcolor='white',
                                 color='white', labelsep=.5, coordinates='axes')
    quiverkey1 = key_ax.quiverkey(overlay, 3.75, .4, 1*.5144, "1 knot", labelpos='S', labelcolor='white',
                                  color='white', labelsep=.5, coordinates='axes')
    quiverkey2 = key_ax.quiverkey(overlay, 6.5, .4, 2*.5144, "2 knots", labelpos='S', labelcolor='white',
                                  color='white', labelsep=.5, coordinates='axes')
    key_ax.set_axis_off()

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
        download("0")
    if args.task == "plot":
        sst_function()
    elif args.task == "test":
        test()
        sys.exit(0)
        #sys.exit(test())

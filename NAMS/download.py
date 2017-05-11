import os
import sys
import urllib
from datetime import datetime, timedelta


# TODO: Change arguments to a float??
""" download(north, south, east, west, height)
north - north latitude value (string)
south - south latitude value (string)
east - east longitude value (string)
west - west longitude value (string)
height - height-above-ground (meters)

returns filename as WIND_date_height.nc
"""
def download(north, south, east, west, height):
    #list of file ids created
    new_file_ids = []

    current_time = datetime.now().date()
    end_time = datetime.now().date()+timedelta(days=1)
    begin = str(current_time) + 'T00%3A00%3A00Z'
    end = str(end_time) + 'T00%3A00%3A00Z'

    print "Downloading...."

    url = 'http://thredds.ucar.edu/thredds/ncss/grib/NCEP/NAM/CONUS_12km/conduit/Best?var=u-component_of_wind_height_above_ground&var=v-component_of_wind_height_above_ground&north='+north+'&west='+west+'&east='+east+'&south='+south+'&horizStride=1&time_start='+begin+'&time_end='+end+'&timeStride=1&addLatLon=true&='+str(height)+'&accept=netcdf'

    fileName = "/home/data/files/{0}-{1}_{2}.nc".format("WIND", current_time, height)
    urllib.urlretrieve(url, fileName)
    print "Downloaded File: ", fileName
    return file


north = "46.5"; south = "41.7"; east = "-116"; west = "-125"; height = "0";
download(north, south, east, west, height)

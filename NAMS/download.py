import os
import sys
import urllib
from datetime import datetime, timedelta


def download(north, south, east, west):
    #list of file ids created
    new_file_ids = []

    current_time = datetime.now().date()
    end_time = datetime.now().date()+timedelta(days=2)
    begin = str(current_time) + 'T00%3A00%3A00Z'
    end = str(end_time) + 'T00%3A00%3A00Z'

    url = 'http://thredds.ucar.edu/thredds/ncss/grib/NCEP/NAM/CONUS_12km/conduit/Best?var=u-component_of_wind_height_above_ground&var=v-component_of_wind_height_above_ground&north='+northk+'&west=-'+west+'&east=-'+east+'&south='+south+'&horizStride=1&time_start='+begin+'&time_end='+end+'&timeStride=1&vertCoord=&addLatLon=true&accept=netcdf'


    local_filename = "/home/data/{0}_{1}.nc".format("WIND", current_time)
    print "FileName: ", local_filename
    urllib.urlretrieve(url, local_filename)

    print "Successful!"


north = "46.5"; south = "41.7"; east = "-116"; west = "-125";
download(north, south, east, west)

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

    url = 'http://thredds.ucar.edu/thredds/ncss/grib/NCEP/NAM/CONUS_12km/conduit/Best?var=u-component_of_wind_height_above_ground&var=v-component_of_wind_height_above_ground&north='+str(north)+'&west=-'+str(west)+'&east=-'+str(east)+'&south='+str(south)+'&horizStride=1&time_start='+begin+'&time_end='+end+'&timeStride=1&vertCoord=&addLatLon=true&accept=netcdf'

    
    destination_directory = os.path.join("/home/NAMS/data/files/")
    local_filename = "{0}_{1}.nc".format("WIND", current_time)

    urllib.urlretrieve(url=url, filename=os.path.join(destination_directory,
    local_filename))

    print "Successful!"


north = 46.5; south = 41.7; east = -116; west = -125;
download(north, south, east, west)

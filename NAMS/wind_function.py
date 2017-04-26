def wind_function(ax, data_file, bmap, time_index, downsample_ratio, interp):

    print "CREATING A WIND PLOT"
    print "DOWNSAMPLERATIO = ", downsample_ratio, "Time Index =", time_index

    # Set up lat and lon variables from the provided file
    tmp = numpy.loadtxt('/opt/sharkeyes/src/latlon.g218')
    lat = numpy.reshape(tmp[:, 2], [614,428])
    lon = numpy.reshape(tmp[:, 3], [614,428])
    x, y = bmap(lon, lat)
    for i in range(0, len(lon)):
        lon[i] = -lon[i]

    var_u = 'u-component_of_wind_height_above_ground'
    var_v = 'v-component_of_wind_height_above_ground'
    landMask = 'Land_cover_0__sea_1__land_surface'

    data_file = open_url(settings.WIND_URL)

    wind_u = data_file[var_u][time_index+104, 0, :, :]
    wind_v = data_file[var_v][time_index+104, 0, :, :]


    if(interp == "TRUE"):
        wind_u = wind_u[:, 0, :, :] # All times of u
        wind_v = wind_v[:, 0, :, :] # All times of
    else:
        wind_u = wind_u[time_index+104, 0, :, :]
        wind_v = wind_v[time_index+104, 0, :, :]
    # Remove the surface height dimension (Its only 1-Demensional)
    wind_u = numpy.squeeze(wind_u) # Removes The Surface Height Dimension
    wind_v = numpy.squeeze(wind_v) # Ditto

    if(0): # Debug
        print "Wind_u.shape", wind_u.shape
        print "Wind_v.shape", wind_v.shape

    #TODO Interpolate Winds Every Hour Except Midnight and noon
    #TODO: This can be cleaned up

    if(interp == "TRUE"):
        print "INTERPOLATING"

        time = data_file['time']
        ts1 = []
        ts2 = []

        wind_u = numpy.reshape(wind_u, (time.shape[0], 428, 614))
        wind_v = numpy.reshape(wind_v, (time.shape[0], 428, 614))

        #TODO: Add some kind of error checking here
        # Generate a time range 0 ... 139 for every 4 hours using the python thingy
        #start_time = datetime.strptime(time.units, "Hour since %Y-%m-%dT%H:%M:%SZ")
        size = time.shape[0]

        # Create two different time stamps used for interpolating
        ts2 = numpy.arange(0, size * 3, 4) # One for every 4 hours
        ts1 = numpy.arange(0, size * 3, 3) # One for every 3  hours

        if(0): # Debug
            print "Wind_u:", wind_u.shape
            print "Wind_v:", wind_v.shape
            print "time.shape:", time.shape
            print "ts1.shape:", ts1.shape[0]
            print "ts2.shape:", ts2.shape[0]

        wind_u_int = numpy.empty([ts2.shape[0], 428, 614]) # Array to be filled
        wind_v_int = numpy.empty([ts2.shape[0], 428, 614]) # Ditto


        # Loop through each lat and long and intpolate each value from time stamp ts1
        # to ts2.  (ie from every 3rd hours to every 4hrs between the NAMS model time) see help(numpy.interp)
        for i in range(0, 427):
            for j in range(0, 613):
                wind_u_int[:,i,j] = numpy.interp(ts2, ts1, wind_u[:,i,j])
                wind_v_int[:,i,j] = numpy.interp(ts2, ts1, wind_v[:,i,j])

    if(interp == "TRUE"):
        wind_u = wind_u_int[time_index+104, :, :] #Pull out the time
        wind_v = wind_v_int[time_index+104, :, :] #Pull out the time
    else:
        wind_u = wind_u[time_index+104, :, :] #Pull out the time
        wind_v = wind_v[time_index+104, :, :] #Pull out the time

    wind_u = numpy.squeeze(wind_u) # Squeeze out the time
    wind_v = numpy.squeeze(wind_v) # Squeeze out the time

    wind_u = numpy.reshape(wind_u, (614, 428))
    wind_v = numpy.reshape(wind_v, (614, 428))

    if downsample_ratio == 1:
        length = 3
    elif downsample_ratio == 5:
        length = 7

    if(0): # Debug
        print "After pulling time"
        print "Wind_u:", wind_u.shape
        print "Wind_v:", wind_v.shape
        print "Lat:", lat.shape
        print "Lon:",  lon.shape
        print "x:", x.shape
        print "y:", y.shape

    bmap.barbs(x[::downsample_ratio, ::downsample_ratio],
               y[::downsample_ratio, ::downsample_ratio],
               wind_u[::downsample_ratio, ::downsample_ratio],
               wind_v[::downsample_ratio, ::downsample_ratio],
               ax=ax,
               length=length)
    print "WIND PLOT CREATED!"

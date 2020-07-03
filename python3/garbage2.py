def ncdump(nc_fid, verb=True):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print("\t\ttype:", repr(nc_fid.variables[key].dtype))
            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr)))
        except KeyError:
            print("\t\tWARNING: %s does not contain variable attributes" % key)

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print("NetCDF Global Attributes:")
        for nc_attr in nc_attrs:
            print('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print("NetCDF dimension information:")
        for dim in nc_dims:
            print("\tName:", dim)
            print("\t\tsize:", len(nc_fid.dimensions[dim]))
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print("NetCDF variable information:")
        for var in nc_vars:
            if var not in nc_dims:
                print('\tName:', var)
                print("\t\tdimensions:", nc_fid.variables[var].dimensions)
                print("\t\tsize:", nc_fid.variables[var].size)
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars


def findScaleOffset(nc_fid, var, scaleKey='SCale', offsetKey='offset',
                    print_info=False):
    '''
    findScaleOffset searchs for scale and offset in the attributes, return thems
    if found, otherwise returns 1 and 0 respectively

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    var : string
        var to search (tas, t2m, etc)
    scaleKey : string
        string to search for (case insensitive)
    offsetKey : string
        string to search for (case insensitive)

    Returns
    -------
    Found : boolean
        True if any of the scaling factors is found
    scale_factor : depends on the NetCDF (double, float, etc)
        The value of the scale factor
    add_offset : depends on the NetCDF (double, float, etc)
        The value of the offset
    '''

    # scale var
    found = False
    scale_factor = 1
    add_offset = 0

    try:
        var_attrs = nc_fid.variables[var].ncattrs()
        if print_info:
            print("%s attributes : %s" % (var, var_attrs))
        # print(type(tas_attrs)) #list
        for attr in var_attrs:
            if scaleKey.lower() in attr.lower():  # lower just to make it case insensitive
                scale_factor = nc_fid.variables[var].getncattr(attr)
                print("Found %s: %f" % (attr, scale_factor))
                found = True
            if offsetKey.lower() in attr.lower():
                add_offset = nc_fid.variables[var].getncattr(attr)
                print("Found %s: %f" % (attr, add_offset))
                found = True
    except:
        print("Error, leaving to default vals")
        # scale var
        found = False
        scale_factor = 1
        add_offset = 0
    return found, scale_factor, add_offset


def convertTime(cdo, nc_file_in, nc_file_out):
    cdo.setreftime("1850-01-01,00:00:00", input="-setcalendar,standard "+nc_file_in, output=nc_file_out)


def convertTemp(cdo, nc_file_in, nc_file_out):
    import os
    nc_file_out_aux = "convertTemp_aux.nc"
    cdo.subc("273.15", input=nc_file_in, output=nc_file_out_aux)
    cdo.chunit("K,C", input=nc_file_out_aux, output=nc_file_out)
    os.remove(nc_file_out_aux)


def convertPrecip(cdo, nc_file_in, nc_file_out):
    import os
    nc_file_out_aux = "convertPrecip_aux.nc"
    # 1 kg of rain water spread over 1 square meter of surface is 1 mm in thickness
    # there are 60X60X24=86400 seconds in one day.
    # Therefore, 1 kg/m2/s = 86400 mm/day.
    cdo.mulc("86400", input=nc_file_in, output=nc_file_out_aux)
    cdo.chunit("'kg m-2 s-1','mm day-1'", input=nc_file_out_aux, output=nc_file_out)
    os.remove(nc_file_out_aux)


def draw_map(m, scale=1):
    from itertools import chain
    import numpy as np
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)

    # Add Coastlines, States, and Country Boundaries
#    m.drawcoastlines()
#    m.drawstates()
    m.drawcountries()

    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 100))
    lons = m.drawmeridians(np.linspace(-180, 180, 300))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)

    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='b')


def get_subdirs(a_dir):
    '''
    Return (me da los nombres de cada directorio) the names of the directories inside the input folder,
    and the full path of each directory.
    '''
    import os
    return [[name, os.path.join(a_dir, name)] for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_subfiles(a_dir):
    '''
    Return the names of the files inside the input folder,
    and the full path of each file.
    '''
    import os
    return [[name, os.path.join(a_dir, name)] for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]


def check(dir_in):
    import os
    if os.path.exists(dir_in):
        return True
    else:
        return False


def check_and_create(dir_in):
    '''
    Check if a dir exists, if not, create it
    '''
    import os
    if os.path.exists(dir_in):
        pass  # does nothing
        # print("Dir already exists", dir_in)
    else:
        print("Create dir", dir_in)
        os.mkdir(dir_in)


def plotRavel(file_path, param):
    '''
    flaten array to 1D and plot it
    '''

    from netCDF4 import Dataset
    import numpy as np

    import matplotlib.pyplot as plt

    fh = Dataset(file_path, mode='r')  # file handle

    pr = fh.variables[param][:, :, :]
    fh.close()

    plt.plot(np.ravel(pr))
    plt.title(file_path)
    plt.show()


def moving_average(arr, win=3):
    ''' calculates non weigthed moving moving_average of array
    '''

    import numpy as np

    ret = np.cumsum(arr, dtype=float)
    ret[win:] = ret[win:] - ret[:-win]
    return ret[win - 1:] / win


def reorderLegend(ax=None, order=None, unique=False):
    '''
    #  Returns tuple of handles, labels for axis ax, after reordering them to
    conform to the label order `order`, and if unique is True,
    after removing entries with duplicate labels

    From https://gitlab.com/cpbl/cpblUtilities/blob/master/mathgraph.py
    '''
    import matplotlib.pyplot as plt
    import numpy as np

    if ax is None:
        ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))  # sort both labels and handles by labels
    if order is not None:  # Sort according to a given list (not necessarily complete)
        keys = dict(zip(order, range(len(order))))
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t, keys=keys: keys.get(t[0], np.inf)))
    if unique:
        labels, handles = zip(*unique_everseen(zip(labels, handles), key=labels))  # Keep only the first of each handle
    # ax.legend(handles, labels)
    return(handles, labels)


def unique_everseen(seq, key=None):
    seen = set()
    seen_add = seen.add
    return [x for x, k in zip(seq, key) if not (k in seen or seen_add(k))]


def draw_screen_poly(box_in, m):
    '''
    '''
    import numpy as np
    from matplotlib.patches import Polygon

    import matplotlib.pyplot as plt

    # to draw polygon
    lon0 = box_in[0]-360
    lon1 = box_in[1]-360
    lat0 = box_in[2]
    lat1 = box_in[3]
    resolution = 10
    lats_r = np.hstack((np.linspace(lat0, lat1, resolution),
                        np.linspace(lat1, lat0, resolution)))

    lons_r = np.hstack((np.linspace(lon0, lon0, resolution),
                        np.linspace(lon1, lon1, resolution)))

    x, y = m(lons_r, lats_r)
    xy = zip(x, y)
    poly = Polygon(list(xy), fc=(1, 0, 0, 0.0), ec=(0.8, 0, 0, 1), lw=2)
    plt.gca().add_patch(poly)


def plot_basemap_regions(nc_in, png_name_in, param_in, region_in, title_in, cdo, bounds_in, colors_in, over_in, under_in, poly_in=False):
    '''

    '''
    from netCDF4 import Dataset
    import numpy as np

    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from mpl_toolkits.basemap import Basemap

    boxDict = {
        "Andes": [283-1, 288+1, 0, 8.5+1],  # long1, long2, lat1, lat2
        "Alpine": [5-1, 14+1, 44.5-1, 48.5+1]
        }
    box_in = boxDict[region_in]
    box = "%d,%d,%d,%d" % (box_in[0], box_in[1], box_in[2], box_in[3])  # box of Cdo

    print(box)
    print(nc_in)
    print(param_in)

    fh = Dataset(nc_in, 'r')

    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    param = fh.variables[param_in][0:, :, :]

    param_units = fh.variables[param_in].units
    param_name = fh.variables[param_in].long_name
    # close file
    fh.close()

    # Get some parameters for the Stereographic Projection
    # lon_0 = lons.mean()
    # lat_0 = lats.mean()

    # m = Basemap(projection='moll',lon_0=0,resolution='l')
    # m = Basemap(width=50000, height=10000,
    #             resolution='l', projection='moll',\
    #             lat_ts=40, lat_0=lat_0, lon_0=lon_0)  # stere=stereographic projection
    #
    # m = Basemap(projection='ortho', lat_0=5, lon_0=-60, resolution='l')
    m = Basemap(projection='cass', llcrnrlat=box_in[2]-2, urcrnrlat=box_in[3]+2,
                llcrnrlon=box_in[0]-2, urcrnrlon=box_in[1]+2, resolution='l',
                lon_0=box_in[0]+3, lat_0=box_in[2]+4)

    lons_dim = len(lons.shape)
    if 2 == lons_dim:
        lon = lons
        lat = lats
    elif 1 == lons_dim:
        lon, lat = np.meshgrid(lons, lats)
    else:
        print("Error in lon lat array dimension: %d" % lons_dim)

    xi, yi = m(lon, lat)

    # Plot Data
    # cmap = plt.get_cmap('terrain')'' 0.7      0.6         0.5      0.4       0.3        0.2     0.1  0.0
    cmap = mpl.colors.ListedColormap(colors_in)
    cmap.set_over(over_in)
    cmap.set_under(under_in)

    norm = mpl.colors.BoundaryNorm(bounds_in, cmap.N)
    # cb3 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
    #                                 norm=norm,
    #                                 boundaries=[-10] + bounds + [10],
    #                                 extend='both',
    #                                 extendfrac='auto',
    #                                 ticks=bounds,
    #                                 spacing='uniform',
    #                                 orientation='horizontal')

    cs = m.pcolor(xi, yi, np.squeeze(param), alpha=0.7, cmap=cmap, norm=norm)

    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    # m.drawstates()
    m.drawcountries()
    m.shadedrelief()

    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label("%s (%s)" % (param_name, param_units))

    if (poly_in):
        draw_screen_poly(box_in, m)

    # Add Title
    title_region = (title_in)
    plt.title(title_region)
    plt.savefig(png_name_in, dpi=200)
    # plt.show()
    plt.close()


def plot_time_series(file_path_in_array, png_name_in=None, param_in=None, region=None, h_line=None, lat=0, lon=0):
    '''
    plot_time_series ...
    '''
    import pathlib
    from useful_functions import findScaleOffset
    from netcdftime import utime
    import matplotlib.pyplot as plt
    from useful_functions import moving_average
    from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
    import datetime as dt  # Python standard library datetime  module

    # Read time and param vars
    if param_in is None:
        return

    date_fill = None
    rcp45_p25_fill = None
    rcp45_p75_fill = None

    rcp85_p25_fill = None
    rcp85_p75_fill = None

    for file_path_in in file_path_in_array:

        plt.figure(region+' '+param_in, figsize=(15, 6))
        print("plot_time_series "+file_path_in)

        data_in = Dataset(file_path_in, mode='r')

        time = data_in.variables['time'][:]
        param = data_in.variables[param_in][:]
        # Scale var
        [scal_req, scale_factor, add_offset] = findScaleOffset(data_in, param_in)
        param_scaled = (scale_factor*param)+add_offset

        # create time vector
        time_uni = data_in.variables['time'].units
        time_cal = data_in.variables['time'].calendar

        cdftime = utime(time_uni, calendar=time_cal)
        date = [cdftime.num2date(t) for t in time]
        print("plot_time_series "+file_path_in)
        # ############# A plot of Maximum precipitation ##############

        plt.plot(date, param_scaled[:, lat, lon], alpha=0.5, label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0l)

        window = 10  # date [x:-y], where x+y = window - 1
        param_scaled_smoothed = moving_average(arr=param_scaled[:, lat, lon], win=window)
        plt.plot(date[5:-4], param_scaled_smoothed, 'k')
        #plt.plot(date[5:145], param_scaled_smoothed[:140], 'k')  #label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])

        if True:#"25" in file_path_in and "45" in file_path_in:
            rcp45_p25_fill = param_scaled_smoothed[139:]
            #plt.plot(date[144:-4], param_scaled_smoothed[139:], 'g--', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
        elif "75" in file_path_in and "45" in file_path_in:
            rcp45_p75_fill = param_scaled_smoothed[139:]
            date_fill = date[144:-4]
            #plt.plot(date[144:-4], param_scaled_smoothed[139:], 'g--', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
        elif "45" in file_path_in:
            plt.plot(date[144:-4], param_scaled_smoothed[139:], 'g', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])

        if "25" in file_path_in and "85" in file_path_in:
            rcp85_p25_fill = param_scaled_smoothed[139:]
            #plt.plot(date[144:-4], param_scaled_smoothed[139:], 'r--', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
        elif "75" in file_path_in and "85" in file_path_in:
            rcp85_p75_fill = param_scaled_smoothed[139:]
            date_fill = date[144:-4]
            #plt.plot(date[144:-4], param_scaled_smoothed[139:], 'r--', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
        elif "85" in file_path_in:
            plt.plot(date[144:-4], param_scaled_smoothed[139:], 'r', label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])

        plt.ylabel("%s Anomaly (%s)" % (data_in.variables[param_in].long_name,
                                        data_in.variables[param_in].units))

        plt.ticklabel_format(useOffset=False, axis='y')
        plt.xlabel("Time")
        plt.title('Annual '+data_in.variables[param_in].long_name+' Anomaly '+'in the ' + region + ' region (smoothed)', fontweight='bold')
        data_in.close()

        plt.legend()
        # add horizontal line at y=0
        if h_line is not None:
            plt.axhline(y=h_line, color='k')
        # highligth 1961 to 1990 range
        plt.axvspan(dt.datetime(1961, 1, 1), dt.datetime(1990, 12, 30), color='b', alpha=0.1)

        plt.grid(b=True, linestyle='--', linewidth=1)
        plt.show()

    if rcp45_p25_fill is not None:
        plt.fill_between(date_fill, rcp45_p25_fill, rcp45_p75_fill,
                    facecolor="g", # The fill color
                    #color='',       # The outline color
                    alpha=0.2)          # Transparency of the fill

    if rcp85_p25_fill is not None:
        plt.fill_between(date_fill, rcp85_p25_fill, rcp85_p75_fill,
                    facecolor="r", # The fill color
                    #color='',       # The outline color
                    alpha=0.2)          # Transparency of the fill

    plt.legend()#loc=(0, 0), fontsize=7, frameon=True, ncol=11,  bbox_to_anchor=(0, -0.5))  # Legend for smoothed
    plt.tight_layout(rect=[0, 0, 1, 1])

    # add horizontal line at y=0
    if h_line is not None:
        plt.axhline(y=h_line, color='k')
    # highligth 1961 to 1990 range
    plt.axvspan(dt.datetime(1961, 1, 1), dt.datetime(1990, 12, 30), color='b', alpha=0.1)

    plt.grid(b=True, linestyle='--', linewidth=1)
    #plt.show()

    if png_name_in is None:
        pass#plt.show()
    else:
        print(png_name_in)
        plt.savefig(png_name_in, dpi=150)

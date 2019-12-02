#this is a function
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
    cdo.setcalendar("standard", input=nc_file_in, output=nc_file_out)


def convertTemp(cdo, nc_file_in, nc_file_out):
    import os
    nc_file_out_aux = "convertTemp_temporal.nc"
    cdo.subc("273.15", input=nc_file_in, output=nc_file_out_aux)
    cdo.chunit("K,C", input=nc_file_out_aux, output=nc_file_out)
    os.remove(nc_file_out_aux)


def convertPrecip(cdo, nc_file_in, nc_file_out):
    import os
    nc_file_out_aux = "convertPrecip_temporal.nc"
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
    Return the names of the directories inside the input folder,
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


def check_and_create(dir_in):
    '''
    Check if a dir exists, if not, create it
    '''
    import os
    if os.path.exists(dir_in):
        print("%s Dir already exists" % dir_in)
    else:
        print("%s Create" % dir_in)
        os.mkdir(dir_in)

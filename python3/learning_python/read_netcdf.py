import netCDF4
import numpy as np

f= netCDF4.Dataset('/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/cmip5_converted/CSIRO-Mk3-6-0/tas/tas_Amon_CSIRO-Mk3-6-0_historical_r1i1p1_185001-200512.nc')
print(f.variables.keys()) # get all variable names
#temp= f.variables['tas']  #temperature variable --> current shape are the points of the dimensions in tas (time, lat, lon)
#print(temp)
#
# for d in f.dimensions.items():
#     print (d)

#print('tas.dimensions')

#print('tas.shape')   # number of elements, give us the shape of the numpy array

# EACH DIMENSION TIPICALLY HAS A VARIABLE ASSOIATED WITH IT (CALLED COODINATE VARIABLE)
# Coordinate variable are 1D variables that have the same name as dimensions
# Coordinate varibales and auxiliary coordinate variables (named by the coordinates attribute) locate values in time and space
# mt=f.variables['time']
# lat= f.variables['lat']
# lon= f.variables['lon']
# print(mt)
# print(lat)

################# ACCESSING DATA FROM A NETCDF VARIABLE OBJECT ####################
# netCDF variables object behave much like a numpy arrays
# slicing a netCDF variables object returns a numpy array with the data
# boolean array and integer sequence indexing behaves differently for a netCDF variables
# than for numpy arrays. Only 1-d boolean arrays and integer sequences are allowed,
# and these indices work independently along each dimension
# (similar to the day vector subscripts work in fortran)
# time=time[:]
# print(time)


################ EXTRACT LAT/LON VALUES (IN DEGREES) TO NUMPY ARRAYS #################
# latvals=lat[:]; lonvals=lon[:]
# # a function to find the index of the point closest pt
# # (in squared distance) to give lat/lon
# def getclosest_ij(lats,lons,latpt,lonpt):  #find squared distance of every point on grid
#     dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
#     minindex_flattened = dist_sq.argmin()      #1D index of minimum dist_sq elements
#     return np.unravel_index(minindex_flattened, lats.shape)  #get 2D index for latvals and lonvals arrays from 1D indexing
# iy_min, ix_min = getclosest_ij(latvals, lonvals, 50. , -140) # get the closest latitude and longitude values, i want lat 50, lon -140

# # WHAT IS THE TEMPERATURE AT THE SPECIFIC POINT?
# # Read values out of the netCDF file for temperature (Leer los valores del archivo netCDF para la temperatura )
# print ('%7.4f %s' % (temp[0,iy_min, ix_min], temp.units))

# ################### Remote data access via openDAP #######################
#"The following example showcases some nice netCDF features:\n",
#"1. We are seamlessly accessing **remote** data, from a TDS server.\n",
#"2. We are seamlessly accessing **GRIB2** data, as if it were netCDF data.\n",
#"3. We are generating **metadata** on-the-fly."
from siphon.catalog import get_latest_access_url
URL = get_latest_access_url('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p5deg/catalog.xml',
                           'OPENDAP')
gfs = netCDF4.Dataset(URL)

# Look at metadata for a specific variable\n",
# gfs.variables.keys() will show all available variables.\n",
sfctmp = gfs.variables['Temperature_surface']
# get info about sfctmp
print(sfctmp)
# print coord vars associated with this variable
for dname in sfctmp.dimensions:
    print(gfs.variables[dname])

# #################### MISSING VALUES #################
# # - When data == var.misssing_value somewhere , a masked array is returned
# # - illustrate with soil moisture data (only defined over land)\n",
# # - white areas on plot are masked values over water.
# soilmvar = gfs.variables['Volumetric_Soil_Moisture_Content_depth_below_surface_layer']
# # flip (voltear) the data in latitude so North Hemisphere is up on the plot
# soilm = soilmvar[0,0,::-1,:]
# print('shape=%s, type=%s, missing_value=%s' %
#       (soilm.shape, type(soilm), soilmvar.missing_value))
# import matplotlib.pyplot
# #%matplotlib inline
# cs = plt.contourf(soilm)

###################### Packed integer data #####################
# There is a similar feature for variables with `scale_factor` and `add_offset` attributes
#short integer data will automatically be returned as float data, with the scale and offset applied


####################### Dealing with dates and times ################
# - time variables usually measure relative to a fixed date using a certain calendar,
# with units specified like ''hours since YY:MM:DD hh-mm-ss''
# - ''num2date'' and ''date2num'' convenience functions provided to convert
# between these numeric time coordinates and handy python datetime instances.
# - ''date2index'' finds the time index corresponding to a datetime instance

from netCDF4 import num2date, date2num, date2index  # functions that helps to transform the date
timedim = sfctmp.dimensions[0]    # time dim name
print('name of time dimension = %s' % timedim)
times = gfs.variables[timedim]    # time coord var
print('units = %s, values = %s' % (times.units, times[:]))



##################### Simple multi-file aggregation #####################
# What if you have a bunch of netcdf files, each with data for a different year,
# and you want to access all the data as if it were in one file?
# "MFDataset" uses files globbing to patch together all the files into one big Dataser.
# Yoy can also pass it a list of specific files
# LIMITATIONS: - It can only aggregate the data along the lesftmos dimension of each variable
#              - Only works with NETCDF3 or NETCDF4_CLASSIC fotmatted files

# mf = netCDF4.MFDataset('../data/prmsl*nc')
# times = mf.variables['time']
# dates = num2date(times[:],times.units)
# print('starting date = %s' % dates[0])
# print('ending date = %s'% dates[-1])
# prmsl = mf.variables['prmsl']
# print('times shape = %s' % times.shape)
# print('prmsl dimensions = %s, prmsl shape = %s' %
#      (prmsl.dimensions, prmsl.shape))


######################### Closing your netCDF file ##################
# # It's good to close netCDF files, but not actually necessary when Dataset is open for read access only.
# f.close()
# gfs.close()

# ####################### Writing netCDF data ##########################
#Important Note**: when running this notebook interactively in a browser, you probably will not be able
#to execute individual cells out of order without getting an error.  Instead, choose \"Run All\" from the Cell menu after you modify a cell
# Opening a file, creating a new Dataset
#Let's create a new, empty netCDF file named '../data/new.nc', opened for writing
#Be careful, opening a file with 'w' will clobber any existing data (unless `clobber=False` is used, in which case an exception is raised if the file already exists).
# - `mode='r'` is the default.
# - `mode='a'` opens an existing file and allows for appending (does not clobber existing data)
# - `format` can be one of `NETCDF3_CLASSIC`, `NETCDF3_64BIT`, `NETCDF4_CLASSIC` or `NETCDF4` (default).
# `NETCDF4_CLASSIC` uses HDF5 for the underlying storage layer (as does `NETCDF4`) but enforces the classic netCDF 3 data model so data can be read with older clients.  "

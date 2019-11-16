#import packages (reading netCDF4)
from netCDF4 import Dataset
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# DEPRECATION WARNING: The system version of Tk is deprecated and may be removed
# in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1
# to suppress this warning.
TK_SILENCE_DEPRECATION=1

#file we want to open
my_example_nc_file = '../nc_files/examples/t2m_mon_2011-2015.nc'

#Dataset is a function from the netCDF4 Dataset
#open in read-only mode
fh = Dataset(my_example_nc_file, mode='r') #file handler

#print info and variables
print ("="*60)
print(fh)
print ("="*60)
print(fh.variables)
print ("="*60)

#put vars into numpy arrays
lons = fh.variables['longitude'][:]
lats = fh.variables['latitude'][:]
t2m  = fh.variables['t2m'][:,:,:] #air temperature

#If using MERRA-2 data with multiple time indices, the following
#line will subset the first time dimension.
#Note: Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.
#in this dataset, there are 5 years => time dimension is 60 (from 0 to 59)

#t2m(time, latitude, longitude) ;
t2m = t2m[59,:,:]

t2m_units = fh.variables['t2m'].units

#close file
fh.close()

# Get some parameters for the Stereographic Projection
lon_0 = lons.mean()
lat_0 = lats.mean()

 #    ==============   ====================================================
 # |      Keyword          Description
 # |      ==============   ====================================================
 # |      width            width of desired map domain in projection coordinates
 # |                       (meters).
 # |      height           height of desired map domain in projection coordinates
 # |                       (meters).

 # |      lon_0            center of desired map domain (in degrees).
 # |      lat_0            center of desired map domain (in degrees).

 #        lat_ts           latitude of true scale. Optional for stereographic,
 # |                       cylindrical equal area and mercator projections.
 # |                       default is lat_0 for stereographic projection.
 # |                       default is 0 for mercator and cylindrical equal area
 # |                       projections.

 # |      resolution       resolution of boundary database to use. Can be ``c``
 # |                       (crude), ``l`` (low), ``i`` (intermediate), ``h``
 # |                       (high), ``f`` (full) or None.
 # |                       If None, no boundary data will be read in (and
 # |                       class methods such as drawcoastlines will raise an
 # |                       if invoked).
 # |                       Resolution drops off by roughly 80% between datasets.
 # |                       Higher res datasets are much slower to draw.
 # |                       Default ``c``. Coastline data is from the GSHHS
 # |                       (http://www.soest.hawaii.edu/wessel/gshhs/gshhs.html).
 # |                       State, country and river datasets from the Generic
 # |                       Mapping Tools (http://gmt.soest.hawaii.edu).

 # |      projection       map projection. Print the module variable
 # |                       ``supported_projections`` to see a list of allowed
 # |                       values.

m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)     #stere=stereographic projection

# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(t2m))

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(t2m_units)

# Add Title
plt.title('Temperature')

plt.show()

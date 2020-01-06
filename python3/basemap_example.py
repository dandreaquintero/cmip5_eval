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
my_example_nc_file = '../nc_files/cmip5_converted_days/CanCM4/pr/pr_day_CanCM4_historical_r1i1p1_19610101-20051231.nc'
#my_example_nc_file = '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/cmip5_converted/BCC-CCM1.1/pr/pr_Amon_bcc-csm1-1_historical_r1i1p1_185001-201212.nc'

#Dataset is a function from the netCDF4 Dataset
#open in read-only mode
fh = Dataset(my_example_nc_file, mode='r')  # file handler

# print info and variables
print ("="*60)
print(fh)
print ("="*60)
print(fh.variables)
print ("="*60)

# put vars into numpy arrays
lons = fh.variables['lon'][:]-180
lats = fh.variables['lat'][:]
print(lats)
print(lons)
pr = fh.variables['pr'][:,:,:] # air temperature

#If using MERRA-2 data with multiple time indices, the following
#line will subset the first time dimension.
#Note: Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.
#in this dataset, there are 5 years => time dimension is 60 (from 0 to 59)

#t2m(time, latitude, longitude) ;
pr = pr[-10,:,:]

pr_units = fh.variables['pr'].units

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

# m = Basemap(width=50000000,height=35000000,
#             resolution='l',projection='stere',\
#             lat_ts=40,lat_0=lat_0,lon_0=lon_0)     #stere=stereographic projection

m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data
cs = m.pcolor(xi, yi, np.squeeze(pr))

# Add Grid Lines
# m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
# m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
#m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(pr_units)

# Add Title
plt.title('precipitation')

plt.show()

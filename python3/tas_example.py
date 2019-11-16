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
my_example_tas= '../nc_files/examples/tas_Amon_HadGEM2_1860_2005.nc'

#Dataset is a function from the netCDF4 Dataset
#open in read-only mode
fh = Dataset(my_example_tas, mode='r') #file handler

#print info and variables
print ("="*60)
print(fh)
print ("="*60)
print(fh.variables)
print ("="*60)

#put vars into numpy arrays
lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
tas  = fh.variables['tas'][:,:,:] #air temperature

#If using MERRA-2 data with multiple time indices, the following
#line will subset the first time dimension.
#Note: Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.
#in this dataset, there are 145 years => time dimension is 20315 (from 0 to 20312)

#t2m(time, latitude, longitude) ;
tas = tas[1000,:,:]

tas_units = fh.variables['tas'].units

#close file
fh.close()

# Get some parameters for the Stereographic Projection
lon_0 = lons.mean()
lat_0 = lats.mean()

m = Basemap(width=5000000,height=3500000,
            resolution='l',projection='stere',\
            lat_ts=40,lat_0=lat_0,lon_0=lon_0)     #stere=stereographic projection

# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(tas))

# Add Grid Lines
m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(tas_units)

# Add Title
plt.title('Temperature')

plt.show()

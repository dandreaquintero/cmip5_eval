import datetime as dt  # Python standard library datetime  module

from cdo import *
from useful_functions import ncdump
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import xarray as xr
import matplotlib.pyplot as plt

TK_SILENCE_DEPRECATION=1

nc_in  = '../nc_files/examples/t2m_mon_2011-2015.nc'  # Your filename
nc_out = '../nc_files/examples/output.nc'  # Your filename

#Initialize CDO
cdo=Cdo()
cdo.degub = True

#From http://www.bamboodream.sakura.ne.jp/hiroblog/?page_id=552

# instead of writing to file, return the data directly
# type: <class 'netCDF4._netCDF4.Dataset'>

#box values for avg (from insumos5 example):
lat1 = 3.75
lat2 = 8.25
long1 = 284.0
long2 = 288.75

box = "-sellonlatbox,%d,%d,%d,%d"%(long1,long2,lat1,lat2)

nc_data = cdo.fldmean(input=box+" "+nc_in, options='-f nc', returnCdf=True)

# write to a file
# cdo.fldmean(input="-sellonlatbox,-65,-80,-15,15 "+nc_in, output=nc_out \
#                   , options='-f nc', returnCdf=True)

# verify file is written correctly
# type: <class 'netCDF4._netCDF4.Dataset'>
#nc_fh = Dataset(nc_out, 'r') #filehandler

ncdump(nc_data,True)
lats = nc_data.variables['lat'][:]  # extract/copy the data
lons = nc_data.variables['lon'][:]
time = nc_data.variables['time'][:]
t2m  = nc_data.variables['t2m'][:]  # shape is time, lat, lon as shown above

#in this dataset the times is as hours since 1900-01-01
time_hours = [dt.date(1900, 1, 1) + dt.timedelta(hours=t) for t in time]

#scale var
add_offset = nc_data.variables['t2m'].add_offset
scale_factor = nc_data.variables['t2m'].scale_factor
t2m_scaled = (scale_factor*t2m)+add_offset
#print(type(t2m_scaled[:,0,0]))

# A plot of t2m_scaled
fig = plt.figure()
plt.plot(time_hours, t2m_scaled[:, 0, 0], c='r')

plt.ylabel("%s (%s)" % (nc_data.variables['t2m'].long_name,\
                        nc_data.variables['t2m'].units))
plt.ticklabel_format(useOffset=False, axis='y')
plt.xlabel("Time")
plt.title("%s from\n%s scaled" % (nc_data.variables['t2m'].long_name, nc_out ))
plt.grid()

# A plot of t2m_scaled not scaled
fig = plt.figure()
plt.plot(time_hours, t2m[:, 0, 0], c='b')

plt.ylabel("%s (%s)" % (nc_data.variables['t2m'].long_name,\
                        nc_data.variables['t2m'].units))
plt.xlabel("Time")
plt.title("%s from\n%s not scaled" % (nc_data.variables['t2m'].long_name, nc_out ))
plt.grid()

plt.show()

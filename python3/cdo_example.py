import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt

TK_SILENCE_DEPRECATION=1

nc_in = '../nc_files/examples/t2m_mon_2011-2015.nc'  # Your filename
nc_spat_avg = '../nc_files/examples/output.nc'  # Your filename

# Initialize CDO
cdo = Cdo()
cdo.degub = True

fh_orig = Dataset(nc_in, mode='r')  # file handler
#ncdump(fh_orig, True)

# put vars into numpy arrays
lons = fh_orig.variables['longitude'][:]
lats = fh_orig.variables['latitude'][:]

# print(type(lons))<class 'numpy.ma.core.MaskedArray'>
# print(type(lats))

print("lat min = %f" % min(lats))
print("lat max = %f" % max(lats))
print("lon min = %f" % min(lons))
print("lon max = %f" % max(lons))

# From http://www.bamboodream.sakura.ne.jp/hiroblog/?page_id=552

# instead of writing to file, return the data directly
# type: <class 'netCDF4._netCDF4.Dataset'>

# box values for avg (from insumos5 example):
lat1 = 3.75
lat2 = 8.25
long1 = 284.0
long2 = 288.75

box = "-sellonlatbox,%d,%d,%d,%d" % (long1, long2, lat1, lat2)

data_spat_avg = cdo.fldmean(input=box+" "+nc_in, options='-f nc', returnCdf=True)
cdo.fldmean(input=box+" "+nc_in, output=nc_spat_avg, options='-f nc', returnCdf=True)
#cdo -f nc -r -b 64 yearmean t2m_mon_2011-2015.nc t2m_mon_2011-2015_annual.nc
data_ymean = cdo.yearmean(input=nc_spat_avg, options='-f nc', returnCdf=True)
ncdump(data_ymean,True)
t2my = data_ymean.variables['t2m'][:]  # shape is time, lat, lon as shown above
print(t2my)
print("-"*70)
# write to a file
# cdo.fldmean(input="-sellonlatbox,-65,-80,-15,15 "+nc_in, output=nc_spat_avg \
#                   , options='-f nc', returnCdf=True)

# verify file is written correctly
# type: <class 'netCDF4._netCDF4.Dataset'>
# nc_fh = Dataset(nc_spat_avg, 'r') #filehandler

ncdump(data_spat_avg,True)
lats = data_spat_avg.variables['lat'][:]  # extract/copy the data
lons = data_spat_avg.variables['lon'][:]
time = data_spat_avg.variables['time'][:]
t2m = data_spat_avg.variables['t2m'][:]  # shape is time, lat, lon as shown above


# in this dataset the times is as hours since 1900-01-01
time_hours = [dt.date(1900, 1, 1) + dt.timedelta(hours=t) for t in time]

[scal_req, scale_factor, add_offset] = findScaleOffset(data_spat_avg, 't2m')

if scal_req:
    t2m_scaled = (scale_factor*t2m)+add_offset
    # print(type(t2m_scaled[:,0,0]))

    # A plot of t2m_scaled
    fig = plt.figure()
    plt.plot(time_hours, t2m_scaled[:, 0, 0], c='r')

    plt.ylabel("%s (%s)" % (data_spat_avg.variables['t2m'].long_name,
                            data_spat_avg.variables['t2m'].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    plt.title("%s from\n%s scaled" % (data_spat_avg.variables['t2m'].long_name, box))
    plt.grid()

# A plot of t2m_scaled not scaled
fig = plt.figure()
plt.plot(time_hours, t2m[:, 0, 0], c='b')

plt.ylabel("%s (%s)" % (data_spat_avg.variables['t2m'].long_name,
                        data_spat_avg.variables['t2m'].units))
plt.xlabel("Time")
plt.title("%s from\n%s not scaled" % (data_spat_avg.variables['t2m'].long_name, box))
plt.grid()

plt.show()

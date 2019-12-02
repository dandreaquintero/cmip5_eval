import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from useful_functions import draw_map
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netcdftime import utime
import matplotlib.pyplot as plt
import xarray as xr
import os.path
from mpl_toolkits.basemap import Basemap

TK_SILENCE_DEPRECATION=1

nc_file = "tas_Amon_HadGEM2AO_1860-2005_standardCal.nc"
nc_dir  = "../nc_files/"
cmip5_std_dir = "cmip5_standardCal/"

nc_in = nc_dir+cmip5_std_dir+nc_file  # Your filename
nc_spat_avg = os.path.splitext(nc_in)[0]+"_avg_spat.nc"
nc_spat_avg2 = os.path.splitext(nc_in)[0]+"_avg_spat2.nc"

# Initialize CDO
cdo = Cdo()
cdo.degub = True

fh_orig = Dataset(nc_in, mode='r')  # file handler
ncdump(fh_orig, False)
print("-"*80)
# put vars into numpy arrays
lons = fh_orig.variables['lon'][:]
lats = fh_orig.variables['lat'][:]

# print(type(lons))<class 'numpy.ma.core.MaskedArray'>
# print(type(lats))
# From http://www.bamboodream.sakura.ne.jp/hiroblog/?page_id=552

# instead of writing to file, return the data directly
# type: <class 'netCDF4._netCDF4.Dataset'>

# box values for avg (from insumos5 example):
# Region 1 (Colombia)
lat1 = -3
lat2 = 13
long1 = 281    # 360-
long2 = 294

# Region 2 (Alpin region)
lat3 = 42
lat4 = 50
long3 = 5    # 360-
long4 = 10

box = "-sellonlatbox,%d,%d,%d,%d" % (long1, long2, lat1, lat2)
box2 = "-sellonlatbox,%d,%d,%d,%d" % (long3, long4, lat3, lat4)

# region 1
data_spat_avg = cdo.fldmean(input=box+" "+nc_in, options='-f nc', returnCdf=True)
cdo.fldmean(input=box+" "+nc_in, output=nc_spat_avg, options='-f nc', returnCdf=True)

data_ymean = cdo.yearmean(input=nc_spat_avg, options='-f nc', returnCdf=True)
ncdump(data_ymean,False)
tas_year = data_ymean.variables['tas'][:]  # shape is time, lat, lon as shown above
print("number of data points: %d" % len(tas_year))
print("-"*80)

# region 2
data_spat_avg2 = cdo.fldmean(input=box2+" "+nc_in, options='-f nc', returnCdf=True)
cdo.fldmean(input=box2+" "+nc_in, output=nc_spat_avg2, options='-f nc', returnCdf=True)

data_ymean2 = cdo.yearmean(input=nc_spat_avg2, options='-f nc', returnCdf=True)
ncdump(data_ymean,False)
tas_year2 = data_ymean2.variables['tas'][:]  # shape is time, lat, lon as shown above
print("number of data points: %d" % len(tas_year))
print("-"*80)

# write to a file
# cdo.fldmean(input="-sellonlatbox,-65,-80,-15,15 "+nc_in, output=nc_spat_avg \
#                   , options='-f nc', returnCdf=True)
# verify file is written correctly
# type: <class 'netCDF4._netCDF4.Dataset'>
# nc_fh = Dataset(nc_spat_avg, 'r') #filehandler

nc_attrs, nc_dims, nc_vars = ncdump(data_spat_avg,True)

lats = data_spat_avg.variables['lat'][:]  # extract/copy the data
lons = data_spat_avg.variables['lon'][:]
time = data_spat_avg.variables['time'][:]
tas = data_spat_avg.variables['tas'][:]  # shape is time, lat, lon as shown above

lats2 = data_spat_avg2.variables['lat'][:]  # extract/copy the data
lons2 = data_spat_avg2.variables['lon'][:]
time2 = data_spat_avg2.variables['time'][:]
tas2 = data_spat_avg2.variables['tas'][:]  # shape is time, lat, lon as shown above

# ################ create time vector ####################
time_uni = data_spat_avg.variables['time'].units
time_cal = data_spat_avg.variables['time'].calendar

cdftime = utime(time_uni, calendar=time_cal)
date = [cdftime.num2date(t) for t in time]
# date1 = [dt.date(1860, 1, 1) + dt.timedelta(days=t) for t in time]

time_uni2 = data_spat_avg2.variables['time'].units
time_cal2 = data_spat_avg2.variables['time'].calendar

cdftime2 = utime(time_uni2, calendar=time_cal)
date2 = [cdftime2.num2date(t) for t in time]

# scale var
kelvin2cel = -273.15
[scal_req, scale_factor, add_offset] = findScaleOffset(data_spat_avg, 'tas')
tas_scaled = (scale_factor*tas)+add_offset+kelvin2cel
tas_scaled2 = (scale_factor*tas2)+add_offset+kelvin2cel

# print(type(tas_scaled[:,0,0]))

# ds = xr.open_dataset(nc_spat_avg)   # NetCDF or OPeNDAP URL
# #ds is of type <class 'xarray.core.dataset.Dataset'>
# # select a variable to plot
# ds['tas'].plot()
# plt.show()

# ############# A plot of tas_scaled (region 1)##############
fig = plt.figure()
plt.plot(date, tas_scaled[:, 0, 0], c='r')

plt.ylabel("%s (%s)" % (data_spat_avg.variables['tas'].long_name,
                        data_spat_avg.variables['tas'].units))
plt.ticklabel_format(useOffset=False, axis='y')
plt.xlabel("Time")
plt.title("Colombia Temperature")
plt.grid()

# ############### A plot of tas_scaled (region 2) #############
fig2 = plt.figure()
plt.plot(date2, tas_scaled2[:, 0, 0], c='r')

plt.ylabel("%s (%s)" % (data_spat_avg2.variables['tas'].long_name,
                        data_spat_avg2.variables['tas'].units))
plt.ticklabel_format(useOffset=False, axis='y')
plt.xlabel("Time")
plt.title("Alpin Region Temperature")
plt.grid()

# Map Colombia
fig3 = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution='h',
            llcrnrlat=-3, urcrnrlat=13,
            llcrnrlon=281, urcrnrlon=294, )  # lower-left corner, upper-right corner
draw_map(m, 1)


# Map Alpin Region
fig4 = plt.figure(figsize=(8, 6), edgecolor='w')
m2 = Basemap(projection='cyl', resolution='h',
             llcrnrlat=40, urcrnrlat=50,
             llcrnrlon=5, urcrnrlon=15, )
draw_map(m2, 1)

plt.show()

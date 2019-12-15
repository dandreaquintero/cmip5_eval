import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from useful_functions import draw_map
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netcdftime import utime
import matplotlib.pyplot as plt
import os.path

# ###################################################################
# test_file = '../nc_files/cmip5_converted_days/HadGEM2-AO_days/pr/pmax/pr_day_HadGEM2-AO_historical_r1i1p1_18600101-20051230_Andes_pmax.nc'
# # Create file handlers for field mean and year mean
# data_in = Dataset(test_file, mode='r')
#
# # Read time and param vars
# time = data_in.variables['time'][:]
# param = data_in.variables['pr'][-1, 0, 0]
# print(param)

test_file = '../nc_files/cmip5_converted_days/HadGEM2-AO_days/pr/box/pr_day_HadGEM2-AO_historical_r1i1p1_18600101-20051230_Andes_box.nc'

# Create file handlers for field mean and year mean
data_in = Dataset(test_file, mode='r')

# Read time and param vars
time = data_in.variables['time'][:]
# param = data_in.variables['pr'][-365:-1, 0, 0]
param = data_in.variables['pr'][:, 0, 0]
# print(max(param))

# ####################################################################

# Scale var
[scal_req, scale_factor, add_offset] = findScaleOffset(data_in, param)
param_scaled = (scale_factor*param)+add_offset

# create time vector
time_uni = data_in.variables['time'].units
time_cal = data_in.variables['time'].calendar

cdftime = utime(time_uni, calendar=time_cal)
date = [cdftime.num2date(t) for t in time]

# ############# A plot of field mean ##############
plt.figure()
plt.plot(date, param_scaled[:, 0, 0], c='r')

plt.ylabel("%s (%s)" % (data_in.variables[param].long_name,
                        data_in.variables[param].units))
plt.ticklabel_format(useOffset=False, axis='y')
plt.xlabel("Time")
plt.title(title_in)
plt.grid()
plt.show()

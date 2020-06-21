#import packages (reading netCDF4)
from cdo import *
from netCDF4 import Dataset
# import numpy as np
#
# import matplotlib as mpl
import matplotlib.pyplot as plt
from netcdftime import utime
# from matplotlib import cm
# #from colorspacious import cspace_converter
# from collections import OrderedDict
# from mpl_toolkits.basemap import Basemap


# Initialize CDO
cdo = Cdo()
cdo.degub = True

# DEPRECATION WARNING: The system version of Tk is deprecated and may be removed
# in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1
# to suppress this warning.
TK_SILENCE_DEPRECATION = 1

# file we want to open
nc_input = '/Volumes/wd_tesis/tasmin_tasmax_historical_converted_nocalendar/CCSM4/tasmax/Alpine/tasmax_day_CCSM4_historical_r1i1p1_18500101-20051231_Alpine.nc'
nc_fd_out = '/Users/danielaquintero/test_fd.nc'
nc_fd_fldmean_out = '/Users/danielaquintero/test_fd_fldmean.nc'

# cdo.eca_cdd(input=nc_input, output=nc_file_out)
# frost days: Annual count of days when TN (daily minimum temperature)< 0°C
# $cdo eca_fd,freq=year
cdo.etccdi_fd(input=nc_input, output=nc_fd_out, returnCdf=False)

cdo.fldmean(input=nc_fd_out, output=nc_fd_fldmean_out, options='-f nc', returnCdf=False)


data_fd_fldmean = Dataset(nc_fd_fldmean_out, mode='r')

# ##### PLOT ######
fd = data_fd_fldmean.variables["fdETCCDI"][:]
time = data_fd_fldmean.variables['time'][:]            # read the time
time_uni = data_fd_fldmean.variables['time'].units     # get the time units
time_cal = data_fd_fldmean.variables['time'].calendar  # read calendar
cdftime = utime(time_uni, calendar=time_cal)
date = [cdftime.num2date(t) for t in time]

plt.plot(date, fd[:, 0, 0])  # label=model)
plt.grid()
plt.xlabel("Year")
plt.ylabel("%s (%s)" % (data_fd_fldmean.variables["fdETCCDI"].long_name, data_fd_fldmean.variables["fdETCCDI"].units))
plt.title(data_fd_fldmean.variables["fdETCCDI"].long_name+' in the Alpine region', fontweight='bold')
plt.show()

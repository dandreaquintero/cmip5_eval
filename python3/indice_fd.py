#import packages (reading netCDF4)
from cdo import *
# from netCDF4 import Dataset
# import numpy as np
#
# import matplotlib as mpl
import matplotlib.pyplot as plt
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
TK_SILENCE_DEPRECATION=1

#file we want to open
my_example_nc_file = '/Volumes/wd_tesis/tasmin_tasmax_historical/CCSM4/tasmin/Alpine/tasmin_day_CCSM4_historical_r1i1p1_18500101-18841231_Alpine.nc'
nc_file_out = '/Users/danielaquintero/test_fd.nc'

# cdo.eca_cdd(input=my_example_nc_file, output=nc_file_out)
# frost days: Annual count of days when TN (daily minimum temperature)< 0°C
# $cdo eca_fd,freq=year
fd_values = cdo.etccdi_fd(input=my_example_nc_file,
                          output=nc_file_out,
                          returnCdf=True).variables[
                          "fdETCCDI"][:]
fd_values = fd_values.flatten()

###### PLOT ######
plt.plot(fd_values)
plt.grid()
plt.xlabel("Year")
plt.ylabel("Number of Frost days per year")
plt.show()

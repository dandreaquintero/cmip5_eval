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
my_example_nc_file = '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/cmip5_converted_days/CanCM4/pr/Alpine/pr_day_CanCM4_historical_r1i1p1_19610101-20051231_Alpine.nc'
nc_file_out = '/Users/danielaquintero/test.nc'

#cdo.eca_cdd(input=my_example_nc_file, output=nc_file_out)

#Highest 5day percipitation sum
#!export CDO_TIMESTAT_DATE="last"
#$cdo eca_rx5day,50,freq=year -runsum,5
rx5day_values = cdo.etccdi_rx5day(input="-runsum,5 "+my_example_nc_file,
                                  output=nc_file_out,
                                  returnCdf=True).variables["rx5dayETCCDI"][:]
rx5day_values = rx5day_values.flatten()

plt.plot(rx5day_values)
plt.grid()
plt.xlabel("Year")
plt.ylabel("Precipitation sum over 5 days [mm]")
plt.show()

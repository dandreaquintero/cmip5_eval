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

# !export CDO_PCTL_NBINS=302
tn10p_values = cdo.etccdi_tn10p(5,2071,2100, input=tasminHamburg+" tasmin_runmin.nc tasmin_runmax.nc", output="tn10p_hamburg.nc", returnCdf=True).variables["tn10pETCCDI"][:]
tn10p_values = tn10p_values.flatten()

# ###### PLOT ########
# plt.plot(tn10p_values)
# plt.grid()
# plt.xlabel("Year")
# plt.ylabel("Number of days with tmin < tmin90")
# plt.show()

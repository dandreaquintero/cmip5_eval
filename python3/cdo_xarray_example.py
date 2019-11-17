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
# nc_data = cdo.fldmean(input="-sellonlatbox,-65,-80,-15,15 "+nc_in \
#                   , options='-f nc', returnCdf=True)

# write to a file

#box values for avg (from insumos5 example):
lat1 = 3.75
lat2 = 8.25
long1 = 284.0
long2 = 288.75

box = "-sellonlatbox,%d,%d,%d,%d"%(long1,long2,lat1,lat2)
cdo.fldmean(input=box+" "+nc_in, output=nc_out \
                  , options='-f nc', returnCdf=True)

# verify file is written correctly
# type: <class 'netCDF4._netCDF4.Dataset'>
nc_fh = Dataset(nc_out, 'r') #filehandler
ncdump(nc_fh,True)
nc_fh.close()

# add_offset: 293.69328912771044
# scale_factor: 0.00038463520406703495




ds = xr.open_dataset(nc_out)   # NetCDF or OPeNDAP URL
#ds is of type <class 'xarray.core.dataset.Dataset'>
# select a variable to plot
ds['t2m'].plot()
plt.show()

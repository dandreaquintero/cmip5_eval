from cdo import *
from useful_functions import ncdump
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/

nc_f = '../nc_files/examples/t2m_mon_2011-2015.nc'  # Your filename
nc_fid = Dataset(nc_f, 'r')  # Dataset is the class behavior to open the file
                             # and create an instance of the ncCDF4 class
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid,True)

#Initialize CDO
cdo=Cdo()
cdo.degub = True

#From http://www.bamboodream.sakura.ne.jp/hiroblog/?page_id=552
nc_avg = cdo.fldmean(input="-sellonlatbox,-65,-80,-15,15 "+nc_f \
                  , options='-f nc', returnCdf=True)

print ("#"*60)
print ("#"*60)

nc_avg_attrs, nc_avg_dims, nc_avg_vars = ncdump(nc_avg,True)

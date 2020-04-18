# import packages (reading netCDF4)
from netCDF4 import Dataset
import numpy as np

import matplotlib.pyplot as plt

# file we want to open
my_example_nc_file = '/Volumes/SONY_EXFAT/cmip5_days/BCC-CSM1-1-m/pr/pr_day_bcc-csm1-1-m_historical_r1i1p1_18500101-20121231_Alpin_box.nc'
my_example_nc_file = '/Users/danielaquintero/Downloads/cmip5_days/bcc-csm1-1-m/pr/box/alpin/pr_day_bcc-csm1-1-m_historical_r1i1p1_18500101-20121231_Alpin_box.nc'
# Dataset is a function from the netCDF4 Dataset
# open in read-only mode
fh = Dataset(my_example_nc_file, mode='r')  # file handler
pr = fh.variables['pr'][:, :, :]  # air temperature

fh.close()

pr_flat = np.ravel(pr)
plt.plot(pr_flat[3000000:-1])
plt.show()

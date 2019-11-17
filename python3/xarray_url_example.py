import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

import datetime as dt
from datetime import datetime, timedelta #
#from https://nbviewer.jupyter.org/gist/rsignell-usgs/d55b37c6253f27c53ef0731b610b81b4#
#does not work as the url seems to be down, but may be useful for future dev.

#download dataset from yesterday
dayFile = datetime.now() - timedelta(days=1)
dayFile  = dayFile.strftime("%Y%m%d")
url='http://nomads.ncep.noaa.gov:9090/dods/nam/nam%s/nam1hr_00z' %(dayFile)
print(url)

ds = xr.open_dataset(url)

# Specify desired station time series location
# note we add 360 because of the lon convention in this dataset
#lati = 36.605; loni = -121.85899   # west of Pacific Grove, CA
lati = 41.4; loni = -100.8  # Georges Bank

# extract a dataset closeste to specified point
dsloc = ds.sel(lon=loni, lat=lati, method='nearest')

# select a variable to plot
dsloc['dswrfsfc'].plot()
plt.show()

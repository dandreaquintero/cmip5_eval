from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from useful_functions import get_subdirs
from useful_functions import get_subfiles

# DEPRECATION WARNING: The system version of Tk is deprecated and may be removed
# in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1
# to suppress this warning.
TK_SILENCE_DEPRECATION = 1


def plot_basemap(var, lats, lons, title):
    # Get some parameters for the Stereographic Projection
    # lon_0 = lons.mean()
    # lat_0 = lats.mean()

    m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80,
                llcrnrlon=-170, urcrnrlon=170, lat_ts=20, resolution='c')
    # m = Basemap(width=50000000,height=35000000,
    #             resolution='l',projection='stere',\
    #             lat_ts=40,lat_0=lat_0,lon_0=lon_0)  # stere=stereographic projection

    # Because our lon and lat variables are 1D
    # use meshgrid to create 2D arrays
    # Not necessary if coordinates are already in 2D arrays.
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)

    # Plot Data
    cs = m.pcolor(xi, yi, np.squeeze(var))

    # Add Grid Lines
    # m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
    # m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    # m.drawstates()
    m.drawcountries()

    # Add Colorbar
    m.colorbar(cs, location='bottom', pad="10%")
    # cbar.set_label(pr_units)

    # Add Title
    plt.title(title)

    plt.show()


def all_months(path_in, param, file):
    fh_in = Dataset(path_in, mode='r')  # open in read-only mode, file handler is the result of the Dataset
    # put vars into numpy arrays
    lons = fh_in.variables['lon'][:]-180
    lats = fh_in.variables['lat'][:]
    var = fh_in.variables[param][:, :, :]
    fh_in.close()

    i = 0
    for var_month in var:
        title = file + ' ' + param + ' ' + str(i)
        i = i+1
        plot_basemap(var_month, lats, lons, title)


nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_converted/"

max_models = 50
i_models = 0
# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(nc_files_dir+proyect_dir):
    i_models = i_models + 1
    if(i_models > max_models):
        break
    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):
        # loop all files inside the param path
        for file, file_path in get_subfiles(param_path):
            if file.endswith(".nc"):  # check if file is .nc_files_dir
                all_months(file_path, param, file)
                break

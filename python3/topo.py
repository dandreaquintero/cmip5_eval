# import packages (reading netCDF4)
from netCDF4 import Dataset
import numpy as np
from matplotlib.patches import Polygon

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create

from cdo import *

import os.path

# ___________________________________________________________________________
# DEPRECATION WARNING: The system version of Tk is deprecated and may be removed
# in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1
# to suppress this warning.
TK_SILENCE_DEPRECATION = 1
# ___________________________________________________________________________


def draw_screen_poly(box_in, m):
    '''
    '''
    # to draw polygon
    lon0 = box_in[0]-360
    lon1 = box_in[1]-360
    lat0 = box_in[2]
    lat1 = box_in[3]
    resolution = 10
    lats_r = np.hstack((np.linspace(lat0, lat1, resolution),
                        np.linspace(lat1, lat0, resolution)))

    lons_r = np.hstack((np.linspace(lon0, lon0, resolution),
                        np.linspace(lon1, lon1, resolution)))

    x, y = m(lons_r, lats_r)
    xy = zip(x, y)
    poly = Polygon(list(xy), fc=(1, 0, 0, 0.0), ec=(0.8, 0, 0, 1), lw=2)
    plt.gca().add_patch(poly)


def plot_basempap_regions(nc_in, param_in, region_in, box_in, model_in):
    '''

    '''

    nc_in_filename = os.path.basename(nc_in)
    nc_box = os.path.splitext(nc_in_filename)[0]+'_'+region_in+"_box.nc"
    png_box = os.path.splitext(nc_in_filename)[0]+'_'+region_in+"_box.png"

    out_dir = nc_in.replace(nc_in_filename, 'box/')
    check_and_create(out_dir)
    nc_box = nc_in.replace(nc_in_filename, 'box/'+nc_box)
    png_box = nc_in.replace(nc_in_filename, 'box/'+png_box)

    # Initialize CDO
    cdo = Cdo()
    cdo.degub = True

    box = "%d,%d,%d,%d" % (box_in[0]-7, box_in[1]+8, box_in[2]-10, box_in[3]+7)  # box of Cdo

    print(box)
    print(nc_in)
    print(nc_box)
    print(png_box)
    print(param_in)

    cdo.sellonlatbox(box, input=nc_in, output=nc_box, options='-f nc',
                     returnCdf=True)

    fh = Dataset(nc_box, 'r')

    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    param = fh.variables[param_in][:, :]

    # last month of last year
    #param = param[-1, :, :]

    param_units = fh.variables[param_in].units
    param_name = fh.variables[param_in].long_name

    # close file
    fh.close()

    # Get some parameters for the Stereographic Projection
    # lon_0 = lons.mean()
    # lat_0 = lats.mean()

    # m = Basemap(projection='moll',lon_0=0,resolution='l')
    # m = Basemap(width=50000, height=10000,
    #             resolution='l', projection='moll',\
    #             lat_ts=40, lat_0=lat_0, lon_0=lon_0)  # stere=stereographic projection
    #
    # m = Basemap(projection='ortho', lat_0=5, lon_0=-60, resolution='l')
    m = Basemap(projection='cass', llcrnrlat=box_in[2]-6, urcrnrlat=box_in[3]+4,\
                llcrnrlon=box_in[0]-4, urcrnrlon=box_in[1]+6, resolution='h' ,\
                lon_0=box_in[0]+3, lat_0=box_in[2]+3)

    lons_dim = len(lons.shape)
    if 2 == lons_dim:
        lon = lons
        lat = lats
    elif 1 == lons_dim:
        lon, lat = np.meshgrid(lons, lats)
    else:
        print("Error in lon lat array dimension: %d" % lons_dim)

    xi, yi = m(lon, lat)

    # Plot Data
    # cmap = plt.get_cmap('terrain')''
    cmap = mpl.colors.ListedColormap(['royalblue', 'darkgreen', 'green','forestgreen', 'yellowgreen',
                                      'khaki', 'wheat', 'burlywood','tan', 'goldenrod', 'darkgoldenrod',
                                      'sienna', 'saddlebrown', 'whitesmoke'])
    cmap.set_over('white')
    cmap.set_under('blue')

    bounds = [0, 50, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800]  # 11 colors
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    # cb3 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
    #                                 norm=norm,
    #                                 boundaries=[-10] + bounds + [10],
    #                                 extend='both',
    #                                 extendfrac='auto',
    #                                 ticks=bounds,
    #                                 spacing='uniform',
    #                                 orientation='horizontal')

    cs = m.pcolor(xi, yi, np.squeeze(param), alpha=0.7, cmap=cmap, norm=norm)

    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    # m.drawstates()
    m.drawcountries()
    m.shadedrelief()

    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label("%s (%s)" % (param_name, param_units))

    draw_screen_poly(box_in, m)

    # Add Title
    title_region = ('Model ' + model_in + ' for region ' + region_in + ' box '+ box)
    plt.title(title_region)
    plt.savefig(png_box, dpi=200)
    # plt.show()
    plt.close()


# Here starts the script
regionArray = ['Andes', 'Alpin']
boxAndes = [283-1, 288+1, 0, 8.5+1]  # long1, long2, lat1, lat2
boxAlpin = [5-1, 14+1, 44.5-1, 48.5+1]

boxesArray = [boxAndes, boxAlpin]

nc_files_dir = "/Users/danielaquintero/Downloads/"
proyect_dir = "nctest/"

# loop the regionArray and boxesArray together
for region, box in zip(regionArray, boxesArray):

    # loop of all models inside the cmip5 proyect dir
    for model, model_path in get_subdirs(nc_files_dir+proyect_dir):
        # model_path = '../nc_files/cmip5_converted/CMCC-CESM/'
        # model = 'CMCC-CESM'
        # loop of all parameters inside each model
        for param, param_path in get_subdirs(model_path):

            # loop all files inside the param path
            for file, file_path in get_subfiles(param_path):

                if file.startswith("._"):
                    print("Error, file %s starts with ._" % file)

                elif file.endswith(".nc"):  # check if file is .nc_files_dir

                    # plot the subregion
                    plot_basempap_regions(file_path, param, region, box, model)

                    # print("plot_basempap_regions ERROR: Maybe not enough values to unpack")
                else:
                    print("Error, file %s not an .nc" % file)

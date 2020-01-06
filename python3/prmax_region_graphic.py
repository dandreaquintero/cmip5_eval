#import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netcdftime import utime
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os.path
from useful_functions import moving_average


def plot_time_series(data_in, param_in, region):
    '''
    plot_time_series ...
    '''
    # Read time and param vars
    time = data_in.variables['time'][:]
    param = data_in.variables[param_in][:]
    # Scale var
    [scal_req, scale_factor, add_offset] = findScaleOffset(data_in, param_in)
    param_scaled = (scale_factor*param)+add_offset

    # create time vector
    time_uni = data_in.variables['time'].units
    time_cal = data_in.variables['time'].calendar

    cdftime = utime(time_uni, calendar=time_cal)
    date = [cdftime.num2date(t) for t in time]

    # ############# A plot of Maximum precipitation ##############

    plt.figure(region+' '+param_in, figsize=(15, 6))
    plt.plot(date, param_scaled[:, 0, 0], label=model)

    window = 10  # date [x:-y], where x+y = window - 1
    param_scaled_smoothed = moving_average(arr=param_scaled[:, 0, 0], win=window)
    plt.plot(date[5:-4], param_scaled_smoothed, label=model+'_smoothed')

    plt.ylabel("%s (%s)" % (data_in.variables[param_in].long_name,
                            data_in.variables[param_in].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    plt.title('Maximum daily precipitation for ' + region + ' region')


'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _converted folder
The nc files will be analyzed for different regions (for now two)
'''
regionArray = ['Andes', 'Alpin']
paramArray = []

nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_converted_days/"

max_models = 10
# loop the regionArray and boxesArray together
for region in regionArray:
    i_models = 0

    # loop of all models inside the cmip5 proyect dir
    for model, model_path in get_subdirs(nc_files_dir+proyect_dir):
        i_models = i_models + 1
        if(i_models > max_models):
            break
        # loop of all parameters inside each model
        for param, param_path in get_subdirs(model_path):
            # create array of params
            if param not in paramArray:
                paramArray.append(param)

            for subparam, subparam_path in get_subdirs(param_path):
                # loop all files inside the param path
                for file, file_path in get_subfiles(subparam_path):
                    if file.endswith("pmax_fldmax.nc"):  # check if file is .nc_files_dir
                        if region in file:

                            # ploth the time series of the spatial avg
                            data_prmax = Dataset(file_path, mode='r')
                            plot_time_series(data_prmax, param, region)
                            data_prmax.close()

# https://matplotlib.org/examples/color/colormaps_reference.html
colormap = plt.cm.tab20

# after ploting all models, set colors and legend for all the figures
for region in regionArray:
    for param in paramArray:
        fig = plt.figure(region+' '+param)
        allaxes = fig.get_axes()

        colors = [colormap(i) for i in np.linspace(0, 1, len(allaxes[0].lines))]
        linestyles = ['-', '-.']
        for i, j in enumerate(allaxes[0].lines):
            j.set_color(colors[i])
            j.set_linestyle(linestyles[i % len(linestyles)])

        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()

        plt.grid(b=True, linestyle='--', linewidth=1)

        # plt.legend(bbox_to_anchor=(0.5, 0., 0.5, 0.5), loc='best', fontsize='small', frameon=True)
        # plt.legend(loc='best')
        plt.legend(loc=(1.01, 0), fontsize='small', frameon=True)
        # plt.subplots_adjust(right=0.7)
        plt.tight_layout(rect=[0, 0, 1, 1])

        plt.savefig('../'+region+'_'+param+'_max.png', dpi=600)
plt.show()

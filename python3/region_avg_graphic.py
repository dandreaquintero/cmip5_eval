# import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from useful_functions import moving_average
from useful_functions import reorderLegend
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netcdftime import utime
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# import statsmodels.api as sm
# from dateutil.relativedelta import relativedelta
import os.path


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

    # ############# A plot of field mean ##############

    plt.figure(region+' '+param_in, figsize=(15, 6))
    # ########## PLOT ORIGINAL DATA ############
    plt.plot(date, param_scaled[:, 0, 0], label=model)
    # lowess = sm.nonparametric.lowess(param_scaled[:, 0, 0], time, frac=0.06)  # Filter lowess
    # plt.plot(date, lowess[:, 1], label=model)

    # ########## PLOT DATA SMOOTHED #############
    # window = 8  # date [x:-y], where x+y = window - 1
    # param_scaled_smoothed = moving_average(arr=param_scaled[:, 0, 0], win=window)
    # plt.plot(date[4:-3], param_scaled_smoothed, label=model)

    plt.ylabel("%s (%s)" % (data_in.variables[param_in].long_name,
                            data_in.variables[param_in].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    # plt.title('Annual Average '+data_in.variables[param_in].long_name
    #          + ' in the '+region+' region', fontweight='bold')
    plt.title('Annual Average '+data_in.variables[param_in].long_name  # title plot smoothed
              + ' in the '+region+' region', fontweight='bold')
    # plt.show()


def avg_time_series(nc_in, param_in, region, box_in, model_in, print_info):
    '''
    avg_time_series ....

    Parameters
    ----------
    nc_in : string
        path to nc file to be analyzed
    param : string
        the parameter to be read from the nc files
    region : string
        Just the name of a region
    box_in : numerical arrays
        array of 4 numbers that indicates the long1, long2, lat1, lat2 of the
        region
    model_in : string
        Just the name of the model

    Returns
    -------
    '''
    print(nc_in)
    print(param_in)
    print(region)
    print(box_in)
    print(model_in)

    nc_in_filename = os.path.basename(nc_in)  # ###
    nc_fldmean = os.path.splitext(nc_in_filename)[0]+'_'+region+"_fldmean.nc"
    nc_ymean = os.path.splitext(nc_in_filename)[0]+'_'+region+"_ymean.nc"

    png_fldmean = os.path.splitext(nc_in_filename)[0]+'_'+region+"_fldmean.png"
    png_ymean = os.path.splitext(nc_in_filename)[0]+'_'+region+"_ymean.png"

    out_dir = nc_in.replace(nc_in_filename, 'avg')
    check_and_create(out_dir)
    nc_fldmean = nc_in.replace(nc_in_filename, 'avg/'+nc_fldmean)
    nc_ymean = nc_in.replace(nc_in_filename, 'avg/'+nc_ymean)

    png_fldmean = nc_in.replace(nc_in_filename, 'avg/'+png_fldmean)
    png_ymean = nc_in.replace(nc_in_filename, 'avg/'+png_ymean)

    print(nc_fldmean)
    print(nc_ymean)

    print("-"*80)

    # Initialize CDO
    cdo = Cdo()
    cdo.degub = True

    data_in = Dataset(nc_in, mode='r')  # file handler
    if print_info:
        ncdump(data_in, True)
        print("-"*80)
    data_in.close()

    box = "-sellonlatbox,%d,%d,%d,%d" % (box_in[0], box_in[1], box_in[2], box_in[3])

    # Create nc files for field mean and year mean.
    if os.path.exists(nc_fldmean):
        print("%s already exists", nc_fldmean)
    else:
        print("%s Create", nc_fldmean)
        cdo.fldmean(input=box+" "+nc_in, output=nc_fldmean, options='-f nc', returnCdf=True)

    if os.path.exists(nc_ymean):
        print("%s already exists", nc_ymean)
    else:
        print("%s Create", nc_ymean)
        cdo.yearmean(input=nc_fldmean, output=nc_ymean, options='-f nc', returnCdf=True)

    # Create file handlers for field mean and year mean
    data_fldmean = Dataset(nc_fldmean, mode='r')
    data_ymean = Dataset(nc_ymean, mode='r')

    # Check field mean is ok
    if print_info:
        ncdump(data_fldmean, True)

    # Check year mean is ok
    if print_info:
        ncdump(data_ymean, True)
        param_year = data_ymean.variables[param_in][:]
        print("number of data points: %d" % len(param_year))
        print("-"*80)

    # title_fldmean = ('Field mean for ' + param_in + ' for ' + region + ' region'
#                  + ' for model ' + model_in)

    # title_ymean = ('Year and field mean for ' + param_in + ' for ' + region
    #           + ' region' + ' for model ' + model_in)

    # plot_time_series (data_fldmeanmean, param_in, region, title_fldmean)
    plot_time_series(data_ymean, param_in, region)
    # plt.savefig(png_ymean, dpi=300)

    data_fldmean.close()
    data_ymean.close()


'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _converted folder
The nc files will be analyzed for different regions (for now two)
'''
regionArray = ['Andes', 'Alpine']
boxAndes = [283-1, 288+1, 0, 8.5+1]  # long1, long2, lat1, lat2
boxAlpine = [5-1, 14+1, 44.5-1, 48.5+1]
boxesArray = [boxAndes, boxAlpine]
paramArray = []

nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_historical_converted/"

max_models = 50
# loop the regionArray and boxesArray together
for region, box in zip(regionArray, boxesArray):
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
                paramArray.append(param)    # create an array to plot with all the models saved

            # loop all files inside the param path
            for file, file_path in get_subfiles(param_path):
                if file.startswith("._"):
                    pass  # does nothing
                elif file.endswith(".nc"):  # check if file is .nc_files_dir
                    # ploth the time series of the spatial avg
                    avg_time_series(file_path, param, region, box, model, False)
                    break

# https://matplotlib.org/examples/color/colormaps_reference.html
colormap = plt.cm.tab20

# after ploting all models, set colors and legend for all the figures

modelsHigh = ['MIROC4h',      'CESM1_BGC',      'CESM1_CAM5',       'CESM1_FASTCHEM',
              'CCSM4',    'CNRM-CM5',       'CNRM-CM5-2',       'EC-EARTH',
              'CMCC-CM',    'MIROC5',         'MRI-CGCM3',        'MRI-ESM1']

modelsHighColors = ['red',  'royalblue',     'black',     'rebeccapurple',
                    'brown',    'cyan',     'darkorange',   'purple',
                    'crimson',  'deepskyblue',  'yellowgreen',  'lightseagreen']

for region in regionArray:
    for param in paramArray:
        fig = plt.figure(region+' '+param)
        allaxes = fig.get_axes()

        modelsLowcolors = [colormap(i) for i in np.linspace(0, 0.4, len(allaxes[0].lines))]
        modelsLowlinestyles = ['--', ':']

        for i, line in enumerate(allaxes[0].lines):
            mod = line.get_label()

            # For models in High Res list, use - and predefined color
            if mod in modelsHigh:
                line.set_linestyle('-')
                line.set_color(modelsHighColors[modelsHigh.index(mod)])

            # For Low Res models, use eq. spaced color, non - linestyle and set transparency
            else:
                line.set_linestyle(modelsLowlinestyles[i % len(modelsLowlinestyles)])
                line.set_color(modelsLowcolors[i])
                line.set_alpha(.6)

        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()

        plt.grid(b=True, linestyle='--', linewidth=1)

        # order axes to put High Res models first, and move the legend to the bottom
        [handles, labels] = reorderLegend(allaxes[0], modelsHigh)
        # plt.legend(handles, labels, loc=(0, 0), fontsize=7, frameon=True, ncol=11, bbox_to_anchor=(-0, -0.38))  # loc=(1.01, 0)
        # plt.legend(bbox_to_anchor=(0.5, 0., 0.5, 0.5), loc='best', fontsize='small', frameon=True)
        # plt.legend(loc='best')
        # plt.legend(loc=(0, 0), fontsize=7, frameon=True, ncol=11, bbox_to_anchor=(-0, -0.38))  # loc=(1.01, 0)
        plt.legend(handles, labels, loc=(0, 0), fontsize=7, frameon=True, ncol=11, bbox_to_anchor=(-0, -0.4)) # Legend for smoothed
        # plt.subplots_adjust(right=0.7)
        plt.tight_layout(rect=[0, 0, 1, 1])

        plt.savefig('../'+region+'_'+param+'_annual_avg.png', dpi=150)
plt.show()

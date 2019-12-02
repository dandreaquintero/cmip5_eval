#import datetime as dt  # Python standard library datetime  module
from cdo import *
from useful_functions import ncdump
from useful_functions import findScaleOffset
from useful_functions import draw_map
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netcdftime import utime
import matplotlib.pyplot as plt
# import xarray as xr
import os.path
# from mpl_toolkits.basemap import Basemap


def plot_time_series(data_in, param_in, title_in):
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
    plt.figure()
    plt.plot(date, param_scaled[:, 0, 0], c='r')

    plt.ylabel("%s (%s)" % (data_in.variables[param_in].long_name,
                            data_in.variables[param_in].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    plt.title(title_in)
    plt.grid()


def avg_time_series(nc_in, param_in, region, box_in, model_in, print_info=False):
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

    nc_in_filename = os.path.basename(nc_in)
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

    title_fldmean = ('Field mean for ' + param_in + ' for ' + region + ' region'
                     + ' for model ' + model_in)

    title_ymean = ('Year and field mean for ' + param_in + ' for ' + region
                   + ' region' + ' for model ' + model_in)

    plot_time_series(data_fldmean, param_in, title_fldmean)
    plt.savefig(png_fldmean)

    plot_time_series(data_ymean, param_in, title_ymean)
    plt.savefig(png_ymean)

    data_fldmean.close()
    data_ymean.close()

    plt.show()

'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _standardCal folder
The nc files will be analyzed for different regions (for now two)
'''
regionArray = ['Colombia', 'Alpin']
boxCol = [281, 294, -3, 13]  # long1, long2, lat1, lat2
boxAlpin = [5, 10, 42, 50]
boxesArray = [boxCol, boxAlpin]

nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_converted/"

# loop the regionArray and boxesArray together
for region, box in zip(regionArray, boxesArray):

    # loop of all models inside the cmip5 proyect dir
    for model, model_path in get_subdirs(nc_files_dir+proyect_dir):

        #  TODO: Call function to plot region

        # loop of all parameters inside each model
        for param, param_path in get_subdirs(model_path):

            # loop all files inside the param path
            for file, file_path in get_subfiles(param_path):

                if file.endswith(".nc"):  # check if file is .nc_files_dir

                    # ploth the time series of the spatial avg
                    avg_time_series(file_path, param, region, box, model)


# test_file = '../nc_files/tests/test.nc'

# avg_time_series(test_file, 'pr', regionArray[0],
#                 boxesArray[0], 'HadGEM2AO', True)
import datetime as dt  # Python standard library datetime  module
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
import os.path


def plot_time_series(data_in, param_in):
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

    plt.figure()
    plt.plot(date, param_scaled[:, 0, 0], c='r')

    plt.ylabel("%s (%s)" % (data_in.variables[param_in].long_name,
                            data_in.variables[param_in].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    plt.title('Maximum '+data_in.variables[param_in].long_name + ' in the '+region+' region for each year')
    plt.grid()


def max_time_series(nc_in, param_in, model_in, print_info=False):
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
    print(model_in)

    # replace .nc with _time....nc
    nc_in_filename = os.path.basename(nc_in)  #
    nc_timemax = os.path.splitext(nc_in_filename)[0]+"_timemax_annual.nc"
    nc_timemax_fldmax = os.path.splitext(nc_in_filename)[0]+"_timemax_fldmax_annual.nc"

    # replace .nc with time_.... png
    png_timemax = os.path.splitext(nc_in_filename)[0]+"_timemax_annual.png"
    png_timemax_fldmax = os.path.splitext(nc_in_filename)[0]+"_timemax_fldmax_annual.png"

    # create output dir and add dirname to .nc and .png file names
    out_dir = nc_in.replace(nc_in_filename, 'timemax_fldmax')  # folder where files will be saved
    check_and_create(out_dir)
    nc_timemax = nc_in.replace(nc_in_filename, 'timemax_fldmax/'+nc_timemax)
    nc_timemax_fldmax = nc_in.replace(nc_in_filename, 'timemax_fldmax/'+nc_timemax_fldmax)

    png_timemax = nc_in.replace(nc_in_filename, 'timemax_fldmax/'+png_timemax)
    png_timemax_fldmax = nc_in.replace(nc_in_filename, 'timemax_fldmax/'+png_timemax_fldmax)

    print(nc_timemax_fldmax)
    print(png_timemax_fldmax)
    print("-"*80)

    # Initialize CDO
    cdo = Cdo()
    cdo.degub = True

    data_in = Dataset(nc_in, mode='r')  # file handler
    if print_info:
        ncdump(data_in, True)
        print("-"*80)
    data_in.close()
    # box = "-sellonlatbox,%d,%d,%d,%d" % (box_in[0], box_in[1], box_in[2], box_in[3])

    # Create nc files for precipitation max for year.
    if os.path.exists(nc_timemax):
        print("%s already exists", nc_timemax)
    else:
        print("%s Create", nc_timemax)
    #   cdo.yearmax(input=box+" "+nc_in, output=nc_pmax, options='-f nc', returnCdf=True)
        cdo.yearmax(input=nc_in, output=nc_timemax, options='-f nc', returnCdf=True)

    if os.path.exists(nc_timemax_fldmax):
        print("%s already exists", nc_timemax_fldmax)

    else:
        print("%s Create", nc_timemax_fldmax)
        cdo.fldmax(input=nc_timemax, output=nc_timemax_fldmax, options='-f nc', returnCdf=True)

    # Create file handlers for field mean and year mean
    data_timemax = Dataset(nc_timemax, mode='r')
    data_timemax_fldmax = Dataset(nc_timemax_fldmax, mode='r')

    # Check timemax and fldmax are ok
    if print_info:
        ncdump(data_timemax, True)

    if print_info:
        ncdump(data_timemax_fldmax, True)

    # Check timemax temporal is ok
    if print_info:
        ncdump(data_timemax, True)
        param_year = data_timemax.variables[param_in][:]
        print("number of data points: %d" % len(param_year))
        print("-"*80)

    plot_time_series(data_timemax_fldmax, param_in)
    # plt.savefig(png_pmax_fldmax)
    plt.savefig(png_timemax_fldmax, dpi=100)   # ../ queda guardado en el directorio anterior en donde esta
    data_timemax.close()
    data_timemax_fldmax.close()
    plt.show()


'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _standardCal folder
The nc files will be analyzed for different regions (for now two)
'''


model_array = ['CESM1-CAM5']
nc_files_dir = "/Volumes/wd_tesis/"
proyect_dir = "tasmin_tasmax_historical_converted/"

# loop the regionArray and boxesArray together
# for region, box in zip(regionArray, boxesArray):

# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(nc_files_dir+proyect_dir):
    if model not in model_array:  #
        continue                 #
    print(model)

    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):

        for region, region_path in get_subdirs(param_path):
            # loop all files inside the param path
            for file, file_path in get_subfiles(region_path):

                if file.startswith("._"):
                    pass  # does nothing
                elif file.endswith(".nc"):  # check if file is .nc_files_dir

                    # ploth the time series of the spatial avg
                    max_time_series(file_path, param, model, False)
                    # pr_time_series(file_path, param, region, box, model)

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

    plt.figure()
    plt.plot(date, param_scaled[:, 0, 0], c='r')

    plt.ylabel("%s (%s)" % (data_in.variables[param_in].long_name,
                            data_in.variables[param_in].units))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.xlabel("Time")
    plt.title('Maximum '+data_in.variables[param_in].long_name + ' in the '+region+' region')
    plt.grid()


def pr_time_series(nc_in, param_in, model_in, print_info=False):
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

    nc_in_filename = os.path.basename(nc_in)  # ###
    nc_pmax = os.path.splitext(nc_in_filename)[0]+"_pmax.nc"
    nc_pmax_fldmax = os.path.splitext(nc_in_filename)[0]+"_pmax_fldmax.nc"

    png_pmax = os.path.splitext(nc_in_filename)[0]+"_pmax.png"
    png_pmax_fldmax = os.path.splitext(nc_in_filename)[0]+"_pmax_fldmax.png"

    out_dir = nc_in.replace(nc_in_filename, 'pmax')
    check_and_create(out_dir)
    nc_pmax = nc_in.replace(nc_in_filename, 'pmax/'+nc_pmax)
    nc_pmax_fldmax = nc_in.replace(nc_in_filename, 'pmax/'+nc_pmax_fldmax)

    png_pmax = nc_in.replace(nc_in_filename, 'pmax/'+png_pmax)
    png_pmax_fldmax = nc_in.replace(nc_in_filename, 'pmax/'+png_pmax_fldmax)

    print(nc_pmax_fldmax)
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
    if os.path.exists(nc_pmax):
        print("%s already exists", nc_pmax)
    else:
        print("%s Create", nc_pmax)
    #   cdo.yearmax(input=box+" "+nc_in, output=nc_pmax, options='-f nc', returnCdf=True)
        cdo.yearmax(input=nc_in, output=nc_pmax, options='-f nc', returnCdf=True)

    if os.path.exists(nc_pmax_fldmax):
        print("%s already exists", nc_pmax_fldmax)

    else:
        print("%s Create", nc_pmax_fldmax)
        cdo.fldmax(input=nc_pmax, output=nc_pmax_fldmax, options='-f nc', returnCdf=True)

    # Create file handlers for field mean and year mean
    data_pmax = Dataset(nc_pmax, mode='r')
    data_fld_max = Dataset(nc_pmax_fldmax, mode='r')

    # Check pmax and fldmax are ok
    if print_info:
        ncdump(data_pmax, True)

    if print_info:
        ncdump(data_fld_max, True)

    # Check pmax temporal is ok
    if print_info:
        ncdump(data_pmax, True)
        param_year = data_pmax.variables[param_in][:]
        print("number of data points: %d" % len(param_year))
        print("-"*80)

    title_pmax = ('Precipitation max for ' + nc_in_filename)

    plot_time_series(data_fld_max, param_in, title_pmax)
    # plt.savefig(png_pmax_fldmax)
    plt.savefig('../'+region+'_'+param+'.png', dpi=300)   # ../ queda guardado en el directorio anterior en donde esta
    data_pmax.close()
    data_fld_max.close()
    plt.show()


'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _standardCal folder
The nc files will be analyzed for different regions (for now two)
'''
# regionArray = ['Andes', 'Alpin']
# boxAndes = [283-1, 288+1, 2.5-1, 8.5+1]  # long1, long2, lat1, lat2
# boxAlpin = [5-1, 14+1, 44.5-1, 48.5+1]
# boxesArray = [boxAndes, boxAlpin]

nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_converted_days/"

# loop the regionArray and boxesArray together
# for region, box in zip(regionArray, boxesArray):

# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(nc_files_dir+proyect_dir):

    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):

        # loop all files inside the param path
        for file, file_path in get_subfiles(param_path):

            if file.endswith(".nc"):  # check if file is .nc_files_dir

                # ploth the time series of the spatial avg
                pr_time_series(file_path, param, model, False)
                # pr_time_series(file_path, param, region, box, model)

# test_file = '../nc_files/cmip5_converted_days/HadGEM2-AO_days/pr/pr_day_HadGEM2-AO_historical_r1i1p1_18600101-20051230_Alpin_pmax.nc'

# pr_time_series(test_file, 'pr', regionArray[0],
#                boxesArray[0], 'HadGEM2-AO_days', True)

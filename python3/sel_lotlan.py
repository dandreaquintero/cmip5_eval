from cdo import *
from useful_functions import ncdump
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import os.path


def cut_region(nc_in, param_in, region, box_in, model_in, print_info):
    '''
    Parameters
    ----------
    nc_in : string
        path to nc file to be analyzed
    -------
    '''
    print(nc_in)
    print(param_in)
    print(region)
    print(box_in)
    print(model_in)

    nc_in_filename = os.path.basename(nc_in)  #
    nc_region = os.path.splitext(nc_in_filename)[0]+'_'+region+".nc"

    out_dir = nc_in.replace(nc_in_filename, region+'/')
    check_and_create(out_dir)
    nc_region = nc_in.replace(nc_in_filename, region+'/'+nc_region)

    print("-"*80)

    # Initialize CDO
    cdo = Cdo()
    cdo.degub = True

    if print_info:
        data_in = Dataset(nc_in, mode='r')  # file handler
        ncdump(data_in, True)
        print("-"*80)
        data_in.close()

    # Create nc files for field mean and year mean.
    if os.path.exists(nc_region):  # False:
        print("%s already exists", nc_region)
    else:
        print("%s Create", nc_region)
        box = "%d,%d,%d,%d" % (box_in[0], box_in[1], box_in[2], box_in[3])
        cdo.sellonlatbox(box, input=nc_in, output=nc_region, options='-f nc', returnCdf=True)


# The nc files are organized by Model and parameter
# The nc files to be used are the ones from the _converted folder
# The nc files will be analyzed for different regions (for now two)

# model_array = ['CMCC-CM','CSIRO-Mk3L-1-2','EC-EARTH','FGOALS-s2','GISS-E2-H','GISS-E2-R','HadCM3','HadGEM2-CC','HadGEM2-ES','INM-CM4']
model_array = ['CESM1-CAM5']

regionArray = ['Andes', 'Alpine']
boxAndes = [283-1, 288+1, 0, 8.5+1]  # long1, long2, lat1, lat2
boxAlpine = [5-1, 14+1, 44.5-1, 48.5+1]
boxesArray = [boxAndes, boxAlpine]

nc_files_dir = "/Volumes/wd_tesis/"   # /Users/danielaquintero/Downloads/
proyect_dir = "tasmin_tasmax_historical/"  # proyect_dir = "cmip5_days/"
# proyect_dir = "cmip5_days/"

max_models = 50
# loop the regionArray and boxesArray together
for region, box in zip(regionArray, boxesArray):
    i_models = 0
    # loop of all models inside the cmip5 proyect dir
    for model, model_path in get_subdirs(nc_files_dir+proyect_dir):

        if model not in model_array:
            continue

        print(model)

        i_models = i_models + 1
        if(i_models > max_models):
            break
        # loop of all parameters inside each model
        for param, param_path in get_subdirs(model_path):
            # create array of params
            # loop all files inside the param path
            for file, file_path in get_subfiles(param_path):
                if file.startswith("._"):
                    pass  # does nothing
                elif file.endswith(".nc"):  # check if file is .nc_files_dir
                    # ploth the time series of the spatial avg
                    cut_region(file_path, param, region, box, model, False)

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


def anomalies(nc_in, param_in):
    '''
    anomalies
    '''

    cdo = Cdo()
    cdo.degub = True

    nc_avg_61_90 = nc_in.replace('ymean', 'avg_61_90')
    nc_anomal = nc_in.replace('ymean', 'anomal')

    year_range = "-selyear,1961/1990"
    cdo.timmean(input=year_range+" "+nc_in, output=nc_avg_61_90, options='-f nc', returnCdf=True)

    data = Dataset(nc_avg_61_90, mode='r')
    avg_61_90_val = data.variables[param_in][0, 0, 0]

    cdo.subc(avg_61_90_val, input=nc_in, output=nc_anomal)
    data.close()

'''
Here starts the execution
Feed the main function (avg_time_series) all the .nc files we want to analyze
The nc files are organized by Model and parameter
The nc files to be used are the ones from the _converted folder
The nc files will be analyzed for different regions (for now two)
'''
nc_files_dir = "../nc_files/"
proyect_dir = "cmip5_historical_converted/"

# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(nc_files_dir+proyect_dir):
    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):
        # loop all files inside the param path
        for file, file_path in get_subfiles(param_path+'/avg/'):
            if file.endswith("ymean.nc"):  # check if file is .nc_files_dir
                # ploth the time series of the spatial avg
                try:
                    anomalies(file_path, param)
                except:
                    print("Error for file: %s" % file_path)

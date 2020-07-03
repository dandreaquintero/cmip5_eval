from cdo import *
from useful_functions import convertTime
from useful_functions import ncdump
from netCDF4 import Dataset
import os
from useful_functions import convertTemp
from useful_functions import convertPrecip

from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check_and_create
from useful_functions import plotRavel

# Initialize CDO
cdo = Cdo()
cdo.degub = True


project_dir = "/Users/danielaquintero/Downloads/tmasmin"
project_dir_converted = "/Users/danielaquintero/Downloads/tmasmin_converted" # "../nc_files/rcp85_pr_daily_converted/"
file_path_aux = "/Users/danielaquintero/Downloads/file_path_aux.nc"
# project_dir = "/Volumes/wd_personal/rcp85_tmasmin"
# project_dir_converted = "../nc_files/rcp85_tmasmin_daily_converted/"
# file_path_aux = "/Volumes/SONY_FAT32/file_path_aux.nc"

max_models = 45
i_models = 0

# model_array = ['EC-EARTH']
# loop of all models inside the cmip5 project dir
for model, model_path in get_subdirs(project_dir):

    # if model not in model_array:
    #    continue

    print(model)
    i_models = i_models + 1
    if(i_models > max_models):
        break

    model_path_converted = model_path.replace(project_dir, project_dir_converted)
    check_and_create(model_path_converted)

    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):  # me da todo lo que hay dentro de la carpeta modelo (osea parametros)
        param_path_converted = param_path.replace(project_dir, project_dir_converted)
        check_and_create(param_path_converted)

        for region, region_path in get_subdirs(param_path):
            region_path_converted = region_path.replace(project_dir, project_dir_converted)
            check_and_create(region_path_converted)

            # loop all files inside the param path
            for file, file_path in get_subfiles(region_path):

                if file.startswith("._"):
                    pass  # does nothing
                    # print("Starts with ._" , file)
                elif file.endswith(".nc"):  # check if file is .nc
                    file_path_converted = file_path.replace(project_dir, project_dir_converted)

                    if os.path.exists(file_path_converted):
                        print("Aready exists", file_path_converted)
                    else:
                        print("Create", file_path_converted)

                # try:
                    if (param == 'tas') or (param == 'tasmax') or (param == 'tasmin'):
                        convertTime(cdo, file_path, file_path_converted)
                        print("convert "+param)
                        # convertTemp(cdo, file_path_aux, file_path_converted)
                    elif param == 'pr':
                        convertTime(cdo, file_path, file_path_aux)
                        print("convert pr")
                        convertPrecip(cdo, file_path_aux, file_path_converted)
                    else:
                        print("*** Param not recognized ***", param)
                # except:
                    # print("\n\n************************+*")
                    # print("**** Conversion error ****")
                    # print("************************+*\n\n")

                else:
                    pass  # does nothing
                    # print("Not an .nc", file)

os.remove(file_path_aux)

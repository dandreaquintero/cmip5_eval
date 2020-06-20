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

# nc_files_dir = "../nc_files/"
proyect_dir = "/Volumes/wd_tesis/RCP8_5/"
# proyect_dir = "/Users/danielaquintero/Downloads/"
# proyect_dir_converted = "../nc_files/cmip5_historical_converted/"
proyect_dir_converted = "../nc_files/RCP8_5_converted/"
file_path_aux = "/Volumes/wd_tesis/file_path_aux.nc"

max_models = 50
i_models = 0
# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(proyect_dir):
    i_models = i_models + 1
    if(i_models > max_models):
        break

    model_path_converted = model_path.replace(proyect_dir, proyect_dir_converted)
    check_and_create(model_path_converted)

    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):
        param_path_converted = param_path.replace(proyect_dir, proyect_dir_converted)
        check_and_create(param_path_converted)

        # loop all files inside the param path
        for file, file_path in get_subfiles(param_path):

            if file.startswith("._"):
                pass  # does nothing
                # print("Starts with ._" , file)
            elif file.endswith(".nc"):  # check if file is .nc
                file_path_converted = file_path.replace(proyect_dir, proyect_dir_converted)
                if os.path.exists(file_path_converted):
                    print("Aready exists", file_path_converted)
                else:
                    print("Create", file_path_converted)

                    try:
                        convertTime(cdo, file_path, file_path_aux)

                        if param == 'tas':
                            print("convert tas")
                            convertTemp(cdo, file_path_aux, file_path_converted)
                        elif param == 'pr':
                            print("convert pr")
                            convertPrecip(cdo, file_path_aux, file_path_converted)
                        else:
                            print("*** Param not recognized ***", param)
                    except:
                        print("\n\n************************+*")
                        print("**** Conversion error ****")
                        print("************************+*\n\n")

                    # fh = Dataset(file_path_converted, 'r')
            else:
                pass  # does nothing
                # print("Not an .nc",, file)

os.remove(file_path_aux)

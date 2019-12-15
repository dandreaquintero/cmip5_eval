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
# Initialize CDO
cdo = Cdo()
cdo.degub = True

# nc_files_dir = "../nc_files/"
proyect_dir = "/Volumes/SONY_EXFAT/cmip5_days/"
proyect_dir_converted = "../nc_files/cmip5_converted_days/"
file_path_aux = "/Volumes/SONY_EXFAT/file_path_aux.nc"

# loop of all models inside the cmip5 proyect dir
for model, model_path in get_subdirs(proyect_dir):

    model_path_converted = model_path.replace(proyect_dir, proyect_dir_converted)
    check_and_create(model_path_converted)

    # loop of all parameters inside each model
    for param, param_path in get_subdirs(model_path):
        param_path_converted = param_path.replace(proyect_dir, proyect_dir_converted)
        check_and_create(param_path_converted)

        # loop all files inside the param path
        for file, file_path in get_subfiles(param_path):

            if file.endswith(".nc"):  # check if file is .nc
                file_path_converted = file_path.replace(proyect_dir, proyect_dir_converted)
                if os.path.exists(file_path_converted):
                    print("%s already exists", file_path_converted)
                else:
                    print("%s Create", file_path_converted)

                    convertTime(cdo, file_path, file_path_aux)

                    if param == 'tas':
                        print("convert tas")
                        convertTemp(cdo, file_path_aux, file_path_converted)
                    elif param == 'pr':
                        print("convert pr")
                        convertPrecip(cdo, file_path_aux, file_path_converted)
                    else:
                        print("Error, param %s not recognized" % param)

                    fh = Dataset(file_path_converted, 'r')
            else:
                print("Error, file %s not an .nc" % file)

os.remove(file_path_aux)

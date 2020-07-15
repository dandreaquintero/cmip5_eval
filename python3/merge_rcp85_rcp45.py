from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check
import pathlib
import argparse
import sys

nc_dir = "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/"
index_dir = "indices/wsdieca"

cdo = Cdo()
cdo.degub = True

for region, region_path in get_subdirs(nc_dir+index_dir):
    for model_rcp85, model_rcp85_path in get_subdirs(region_path+"/rcp85/models/"):
        file_rcp85_merge = ""
        file_rcp45_merge = ""
        for file_rcp85, file_rcp85_path in get_subfiles(model_rcp85_path):
            if file_rcp85.startswith("._"):
                continue  # go to next file
            if file_rcp85.endswith("ts.nc"):  # check if file is .nc
                file_rcp85_merge = file_rcp85_path

        model_rcp45_path = model_rcp85_path.replace("rcp85", "rcp45")

        if not check(model_rcp45_path):
            print(model_rcp45_path)
            print("NO RCP45 equivalent\n")
            continue
        else:
            for file_rcp45, file_rcp45_path in get_subfiles(model_rcp45_path):
                if file_rcp45.startswith("._"):
                    continue  # go to next file
                if file_rcp45.endswith("ts.nc"):  # check if file is .nc
                    file_rcp45_merge = file_rcp45_path

        print(file_rcp85_merge)
        print(file_rcp45_merge)

        if file_rcp85_merge == "":
            print("no files in histo path")
            continue
        if file_rcp45_merge == "":
            print("no files in rcp path")
            continue

        file_merge = file_rcp85_merge.replace("2005", "1861")
        print(file_merge)
        print("")

        cdo.mergetime(input="-selyear,1861/2005 "+file_rcp45_merge + " " + "-selyear,2006/2090 " + file_rcp85_merge,
                      output=file_merge, options='-f nc', force=False, returnCdf=False)

from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import check
import pathlib
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--rcp45", help="Merges Historical to rcp45", action="store_true")
parser.add_argument("--rcp85", help="Merges Historical to rcp85", action="store_true")
parser.add_argument("--force", help="If set, forces cdo to overwrite", action="store_true")
parser.add_argument("--verb", help="Enable verbose", action="store_true")
parser.add_argument("--pr", help="merge pr", action="store_true")
parser.add_argument("--temp", help="merge temp", action="store_true")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

nc_dir = "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/"

if args.pr:

    histo_path = "historical_pr_daily_converted"
    rcp45_path = "rcp45_pr_daily_converted"
    rcp85_path = "rcp85_pr_daily_converted"

    histo_rcp45_merge = "histo_rcp45_pr_daily_converted"
    histo_rcp85_merge = "histo_rcp85_pr_daily_converted"

    if args.rcp45:
        rcp_path = rcp45_path
        merge_path = histo_rcp45_merge

    elif args.rcp85:
        rcp_path = rcp85_path
        merge_path = histo_rcp85_merge

    else:
        parser.print_help()
        sys.exit()

elif args.temp:
    histo_path = "historical_tmasmin_daily_converted"
    rcp45_path = "rcp45_tmasmin_daily_converted"
    rcp85_path = "rcp85_tmasmin_daily_converted"

    histo_rcp45_merge = "histo_rcp45_tmasmin_daily_converted"
    histo_rcp85_merge = "histo_rcp85_tmasmin_daily_converted"

    if args.rcp45:
        rcp_path = rcp45_path
        merge_path = histo_rcp45_merge

    elif args.rcp85:
        rcp_path = rcp85_path
        merge_path = histo_rcp85_merge

    else:
        parser.print_help()
        sys.exit()
else:
    parser.print_help()
    sys.exit()

cdo = Cdo()
if args.verb:
    cdo.degub = True


for model_histo, model_histo_path in get_subdirs(nc_dir+histo_path):
    # loop of all parameters inside each model
    for param_histo, param_histo_path in get_subdirs(model_histo_path):
        # loop all regions inside each parameter
        for region_histo, region_histo_path in get_subdirs(param_histo_path):
            # loop all files inside the param path
            file_histo_merge = ""
            file_rcp_merge = ""
            for file_histo, file_histo_path in get_subfiles(region_histo_path):
                if file_histo.startswith("._"):
                    continue  # go to next file
                if file_histo.endswith(".nc"):  # check if file is .nc
                    file_histo_merge = file_histo_path

            region_rcp_path = region_histo_path.replace(histo_path, rcp_path)

            if not check(region_rcp_path):
                print(file_histo_merge)
                print("NO RCP equivalent\n")
                continue
            else:
                for file_rcp, file_rcp_path in get_subfiles(region_rcp_path):
                    if file_rcp.startswith("._"):
                        continue  # go to next file
                    if file_rcp.endswith(".nc"):  # check if file is .nc
                        file_rcp_merge = file_rcp_path

            print(file_histo_merge)
            print(file_rcp_merge)

            if file_histo_merge == "":
                print("no files in histo path")
                continue
            if file_rcp_merge == "":
                print("no files in rcp path")
                continue

            first_year = (file_histo_merge.split("_"))[-2].split("-")[0]
            last_year = (file_rcp_merge.split("_"))[-2].split("-")[1]

            if int(first_year[0:4]) > 1861:
                print("Does not include 1861\n")
                continue
            if int(last_year[0:4]) < 2090:
                print("Does not include 2090\n")
                continue

            pathlib.Path(region_histo_path.replace(histo_path, merge_path)).mkdir(parents=True, exist_ok=True)  # To create the output dir

            histo_and_ens = (file_histo_merge.split("_"))[-4]+"-"+(file_histo_merge.split("_"))[-3]
            rcp_and_ens = (file_rcp_merge.split("_"))[-4]+"-"+(file_rcp_merge.split("_"))[-3]

            file_merge = (region_histo_path.replace(histo_path, merge_path)+"/"+param_histo+"_day_"+model_histo+"_"+histo_and_ens+"_"+rcp_and_ens
                          + "_18610101-20901231_"+region_histo+".nc")

            print(file_merge)
            print("")
            cdo.mergetime(input="-selyear,1861/2005 "+file_histo_merge + " " + "-selyear,2006/2090 " + file_rcp_merge,
                          output=file_merge, options='-f nc', force=args.force, returnCdf=False)

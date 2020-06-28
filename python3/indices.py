from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import plot_basemap_regions
from useful_functions import plot_time_series
import pathlib
import argparse
import sys
import shutil


def selyear_index(index_in, param_in, nc_in=None, out_dir_in=None, first_year_in=None):
    '''
    For indexes that need a selyear to generate a timeseries, like sdii
    '''
    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        print("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        print("Error, output dir is was not specified")
        return -1

    pathlib.Path(out_dir_in + '/years/').mkdir(parents=True, exist_ok=True)

    # if a first year is given, start from there, otherwise, start from the first year on the file name
    first_year_file = ((nc_in.split("_"))[-2].split("-")[0])[0:4]
    first_year = first_year_in
    if first_year is None:
        first_year = first_year_file

    last_year = ((nc_in.split("_"))[-2].split("-")[1])[0:4]
    nc_out_array = ""
    for year in range(int(first_year), int(last_year)+1):
        cdo_selyear_command = "-selyear,"+str(year)
        nc_out = out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_sdii"+str(year)+".nc"
        # try:
        if args.verbose:
            print(nc_out)
        # force to False so if the file already exists is not overwritten
        index_cdo_function(input=cdo_selyear_command+" "+nc_in,
                           output=nc_out, options='-f nc', force=True, returnCdf=False)
        nc_out_array = nc_out_array+" "+nc_out
        # except CDOException:
        #    print("CDO Exception")
    # try:
    nc_out_merge = (out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_sdii.nc").replace(first_year_file, first_year)  # adapt the name to the actual first year used
    cdo.mergetime(input=nc_out_array, output=nc_out_merge, options='-f nc', force=True, returnCdf=False)

    nc_out_fldmean = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_sdii_ts.nc").replace(first_year_file, first_year)
    cdo.fldmean(input=nc_out_merge, output=nc_out_fldmean, options="-f nc", force=True, returnCdf=False)

    print("")
    print(nc_out_fldmean)
    print("")
    try:
        shutil.rmtree(out_dir_in + '/years/')
    except OSError as e:
        print("Error: %s" % (e.strerror))

    # except CDOException:
    #    print("CDO Exception")


def seasons_index(index_in, param_in, nc_in=None, out_dir_in=None):
    '''
    For indices that give a single value for the timeperiod, like sdii
    Generate given index for the following 4 periods:
    Past        : 1861 1890
    Reference   : 1961 1990
    Present     : 1991 2020
    Future      : 2061 2090

    The index is calculated for seasons ANN DJF and JJA
    '''
    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        print("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        print("Error, output dir is was not specified")
        return -1

    for season in seasons:
        pathlib.Path(out_dir_in + '/' + season).mkdir(parents=True, exist_ok=True)
        cdo_season_command = sel_season+season
        for year_range, name in zip(year_range_array, period_name_array):
            cdo_year_command = sel_year_range+year_range
            nc_out = out_dir_in + "/" + season + "/" + pathlib.Path(nc_in).stem + "_sdii_" + name + ".nc"

            print(nc_out)
            try:
                # force to False so if the file already exists is not overwritten
                index_cdo_function(input=cdo_year_command+" "+cdo_season_command+" "+nc_in,
                                   output=nc_out, options='-f nc', force=False, returnCdf=False)
            except CDOException:
                print("CDO error")  # lik


def loop_models():
    print("Calculate %s using %s" % (index, req_param))
    # loop the experiment folders we have
    for experiment in experiment_array:
        # loop of all models inside the experiment folder
        for model, model_path in get_subdirs(experiment):
            # loop of all parameters inside each model
            for param, param_path in get_subdirs(model_path):
                # if the param is the required one for the index
                if param == req_param:
                    for region, region_path in get_subdirs(param_path):
                        # loop all files inside the param path
                        for file, file_path in get_subfiles(region_path):

                            if file.startswith("._"):
                                pass  # does nothing

                            elif file.endswith(".nc"):  # check if file is .nc
                                first_year = None
                                output_dir = None
                                if "rcp45" in experiment:
                                    output_dir = indices_output_dir + '/' + index + '/' + region + '/rcp45/models/' + model
                                elif "rcp85" in experiment:
                                    first_year = 2006  # To avoid calculating sdii again for the historical data
                                    output_dir = indices_output_dir + '/' + index + '/' + region + '/rcp85/models/' + model
                                if index == "sdii":
                                    selyear_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir, first_year_in=first_year)
                                    seasons_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir)


def merge_seasons(rcp_path):

    for season in seasons:
        pathlib.Path(rcp_path + '/' + season).mkdir(parents=True, exist_ok=True)
        nc_ensmean_reference = ''
        for period in period_name_array:

            index_file_pathlib_list = pathlib.Path(rcp_path + '/models').rglob('*' + season + '*/*' + period + '*.nc')
            index_all_models = ''
            for index_file_pathlib in index_file_pathlib_list:
                index_file = str(index_file_pathlib)
                if (index_file.startswith("._")) or ("regrid" in index_file):
                    continue  # jump to next file
                index_file_regrid = index_file.replace('.nc', '_regrid.nc')
                target_grid_file = rcp_path + '/target_grid.nc'

                cdo.remapbil(target_grid_file, input=index_file, output=index_file_regrid, froce=False)

                index_all_models += index_file_regrid + ' '

            if index_all_models == '':
                print("No files found for Season %s and period %s" % (season, period))
            else:
                nc_ensmean_out = rcp_path + '/' + season + '/' + index + "_" + period + '.nc'
                try:
                    print(nc_ensmean_out)
                    cdo.enspctl("50", input=index_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)  # median = 50th percentil
                    if "reference" in period:
                        nc_ensmean_reference = nc_ensmean_out

                    elif nc_ensmean_reference != '':  # substract reference from period. Only for non reference period, if reference file has been found.
                        nc_ensmean_sub_out = rcp_path + '/' + season + '/' + index + "_" + period + '_sub.nc'
                        print(nc_ensmean_sub_out)
                        cdo.sub(input=nc_ensmean_out + " " + nc_ensmean_reference, output=nc_ensmean_sub_out, options='-f nc', force=True, returnCdf=False)
                except CDOException:
                    print("CDO error")


def merge_ts(rcp_path):
    array_all_models = ""
    for model, model_path in get_subdirs(rcp_path+"/models/"):
        for file, file_path in get_subfiles(model_path):
            if file.startswith("._"):
                continue

            elif file.endswith(".nc"):  # check if file is .nc
                array_all_models += file_path + ' '

    if array_all_models == '':
        print("No files found in %s" % rcp_path)
    else:
        nc_ensmean_out = rcp_path + '/' + index + '_ts.nc'
        cdo.enspctl("50", input=array_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)  # median = 50th percentil

        # find anomalie
        nc_avg_61_90 = nc_ensmean_out.replace('_ts.nc', '_avg_61_90.nc')
        nc_anomal = nc_ensmean_out.replace('_ts.nc', '_ts_anomal.nc')

        year_range = "-selyear,1961/1990"
        avg_61_90_val = cdo.timmean(input=year_range+" "+nc_ensmean_out, output=nc_avg_61_90, options='-f nc', returnCdf=True).variables[index+"ETCCDI"][0, 0, 0]

        cdo.subc(avg_61_90_val, input=nc_ensmean_out, output=nc_anomal)
        print(nc_anomal)


def merge_index():
    for index, index_path in get_subdirs(indices_output_dir):
        for region, region_path in get_subdirs(index_path):
            for rcp, rcp_path in get_subdirs(region_path):
                merge_seasons(rcp_path)
                merge_ts(rcp_path)


def graph_map():
    bounds = [-0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]  # 11 colors
    colors = ['red', 'firebrick', 'tomato', 'salmon', 'lightcoral',
              'lightsalmon', 'papayawhip', 'snow', 'paleturquoise', 'skyblue', 'lightskyblue',
              'steelblue', 'dodgerblue', 'blue', 'darkblue']
    for index, index_path in get_subdirs(indices_output_dir):
        param = index+"ETCCDI"
        for region, region_path in get_subdirs(index_path):
            for rcp, rcp_path in get_subdirs(region_path):
                for season, season_path in get_subdirs(rcp_path):
                    for file, file_path in get_subfiles(season_path):
                        if file.startswith("._"):
                            pass
                        elif file.endswith("sub.nc"):  # if files ends with _sub.nc is the result of a substraction, and needs to be graphed
                            for period in period_name_array:
                                if period in file:
                                    title = index + " in the " + period + " for season " + season + " in region " + region
                                    plot_basemap_regions(file_path, file_path.replace(".nc", ".png"), param, region, title, cdo, bounds, colors, colors[-1], colors[0])


def graph_ts():
    for index, index_path in get_subdirs(indices_output_dir):
        param = index+"ETCCDI"
        for region, region_path in get_subdirs(index_path):
            for rcp, rcp_path in get_subdirs(region_path):
                for file, file_path in get_subfiles(rcp_path):
                    if file.startswith("._"):
                        continue
                    elif file.endswith("anomal.nc"):  # if files ends with anomal.nc is the result of a substraction, and needs to be graphed
                        plot_time_series(file_path, param, region)


# __________________Here starts the script ______________________

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--full", help="Perform all of the operations", action="store_true")
parser.add_argument("-l", "--loop", help="Loop all the models and calculates the index", action="store_true")
parser.add_argument("-m", "--merge", help="Merge the index from all the models", action="store_true")
parser.add_argument("-g", "--graph", help="Graph the merged index", action="store_true")
parser.add_argument("-v", "--verbose", help="Enable verbose", action="store_true")
parser.add_argument("-i", "--index", help="Index to calculate\nPossile values: sdii")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

index = ""
req_pr = ""
if args.index == "sdii":
    index = "sdii"
    req_param = "pr"

experiment_array = ["/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp45_pr_daily_converted",
                    "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp85_pr_daily_converted"]

indices_output_dir = "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/indices/"

year_range_array = ["1961/1990", "1861/1890", "1991/2020", "2061/2090"]  # reference should go first, to calculate the subs
period_name_array = ["reference_1961-1990", "past_1861-1890", "present_1991-2020", "future_2061-2090"]
sel_year_range = "-selyear,"
# seasons = annual  Dec-Feb    Jun-Aug
seasons = ["ANN",   "DJF",   "JJA"]
sel_season = "-select,season="

# Initialize CDO
cdo = Cdo()
if args.verbose:
    cdo.degub = True

if args.full or args.loop:
    print("Looping all the models")
    loop_models()

if args.full or args.merge:
    print("Merging index")
    merge_index()

if args.full or args.graph:
    print("Creating graphs")
    # graph_map()
    graph_ts()

print("FINISHED")

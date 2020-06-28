from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import plot_basemap_regions
import pathlib
import argparse
import sys


def absolute_index(index_in, param_in, nc_histo_in=None, nc_rcp45_in=None, nc_rcp85_in=None, out_dir_in=None):
    '''
    Generate given index for the following 4 periods:
    Past        : 1861 1890
    Reference   : 1961 1990
    Present     : 1991 2020
    Future      : 2071 2100

    The index is calculated for seasons ANN DJF and JJA, and are saved in folder .index/ANN/, .index/DJF ./index/JJA
    '''
    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        print("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        print("Error, output dir is was not specified")
        return -1

    # year ranges and correspondig input file.

    year_range_array = []
    nc_in_array = []
    name_array = []
    if nc_histo_in is not None:
        year_range_array = ["1861/1890", "1961/1990", "1991/2020"]
        nc_in_array = [nc_histo_in, nc_histo_in, nc_histo_in]
        name_array = ["past_1861-1890.nc", "reference_1961-1990.nc", "present_1991-2020.nc"]

    if nc_rcp45_in is not None:
        year_range_array.append("2071/2100")
        nc_in_array.append(nc_rcp45_in)
        name_array.append("future_rcp45_2070-2100.nc")

    if nc_rcp85_in is not None:
        year_range_array.append("2071/2100")
        nc_in_array.append(nc_rcp85_in)
        name_array.append("future_rcp85_2070-2100.nc")

    sel_year_range = "-selyear,"

    # seasons = annual  Dec-Feb    Jun-Aug
    seasons = ["ANN",   "DJF",   "JJA"]
    sel_season = "-select,season="

    for season in seasons:
        pathlib.Path(out_dir_in + '/' + season).mkdir(parents=True, exist_ok=True)
        cdo_season_command = sel_season+season
        for year_range, nc_in, name in zip(year_range_array, nc_in_array, name_array):
            cdo_year_command = sel_year_range+year_range
            cdo_selparam_command = '-select,name='+param_in
            nc_out = out_dir_in + '/' + season + '/' + name
            if args.verbose:
                print(nc_out)
            try:
                # force to False so if the file already exists is not overwritten
                index_cdo_function(input=cdo_selparam_command+" "+cdo_year_command+" "+cdo_season_command+" "+nc_in,
                                   output=nc_out, options='-f nc', force=False, returnCdf=False)
            except CDOException:
                print("CDO error")  # like the selyear failed bcs the model does not have past range


def loop_models():
    # loop all the index we want to obtain, and the required param for that index
    for index, req_param in zip(index_array, req_param_array):
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
                                    output_dir = indices_output_dir + '/' + index + '/' + region + '/models/' + model
                                    if "historical" in experiment:
                                        absolute_index(index_in=index, param_in=param, nc_histo_in=file_path, out_dir_in=output_dir)
                                    elif "rcp45" in experiment:
                                        absolute_index(index_in=index, param_in=param, nc_rcp45_in=file_path, out_dir_in=output_dir)
                                    elif "rcp85" in experiment:
                                        absolute_index(index_in=index, param_in=param, nc_rcp85_in=file_path, out_dir_in=output_dir)


def merge_index():
    for index, index_path in get_subdirs(indices_output_dir):
        for region, region_path in get_subdirs(index_path):
            for season in seasons:

                pathlib.Path(region_path + '/' + season).mkdir(parents=True, exist_ok=True)
                nc_ensmean_reference = ''
                for period in periods:

                    index_file_pathlib_list = pathlib.Path(region_path + '/models').rglob('*' + season + '*/*' + period + '*.nc')
                    index_all_models = ''
                    for index_file_pathlib in index_file_pathlib_list:
                        index_file = str(index_file_pathlib)
                        if (index_file.startswith("._")) or ("regrid" in index_file):
                            continue  # jump to next file
                        index_file_regrid = index_file.replace('.nc', '_regrid.nc')
                        target_grid_file = region_path + '/target_grid.nc'

                        cdo.remapbil(target_grid_file, input=index_file, output=index_file_regrid, froce=False)

                        index_all_models += index_file_regrid + ' '

                    if index_all_models == '':
                        print("No files found for Season %s and period %s" % (season, period))
                    else:
                        nc_ensmean_out = region_path + '/' + season + '/' + period + '.nc'
                        try:
                            print(nc_ensmean_out)
                            cdo.ensmean(input=index_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)
                            if period == "reference":
                                nc_ensmean_reference = nc_ensmean_out

                            elif nc_ensmean_reference != '':  # substract reference from period. Only for non reference period, if reference file has been found.
                                nc_ensmean_sub_out = region_path + '/' + season + '/' + period + '_sub.nc'
                                print(nc_ensmean_sub_out)
                                cdo.sub(input=nc_ensmean_out + " " + nc_ensmean_reference, output=nc_ensmean_sub_out, options='-f nc', force=True, returnCdf=False)
                        except CDOException:
                            print("CDO error")


def graph_index():
    bounds = [-0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]  # 11 colors
    colors = ['red', 'firebrick', 'tomato', 'salmon', 'lightcoral',
              'lightsalmon', 'papayawhip', 'snow', 'paleturquoise', 'skyblue', 'lightskyblue',
              'steelblue', 'dodgerblue', 'blue', 'darkblue']
    for index, index_path in get_subdirs(indices_output_dir):
        param = index+"ETCCDI"
        for region, region_path in get_subdirs(index_path):
            for season, season_path in get_subdirs(region_path):
                for file, file_path in get_subfiles(season_path):
                    if file.startswith("._"):
                        pass
                    elif file.endswith("sub.nc"):  # if files ends with _sub.nc is the result of a substraction, and needs to be graphed
                        for period in periods:
                            if period in file:
                                title = index + " in the " + period + " for season " + season + " in region " + region
                        plot_basemap_regions(file_path, file_path.replace(".nc", ".png"), param, region, title, cdo, bounds, colors, colors[-1], colors[0])


# __________________Here starts the script ______________________

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--full", help="Perform all of the operations", action="store_true")
parser.add_argument("-l", "--loop", help="Loop all the models and calculates the index", action="store_true")
parser.add_argument("-m", "--merge", help="Merge the index from all the models", action="store_true")
parser.add_argument("-g", "--graph", help="Graph the merged index", action="store_true")
parser.add_argument("-v", "--verbose", help="Enable verbose", action="store_true")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

index_array = ["sdii"]
req_param_array = ["pr"]

experiment_array = ["/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/historical_pr_daily_converted",
                    "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/rcp45_pr_daily_converted"]

indices_output_dir = "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/indices/"

seasons = ["ANN", "DJF", "JJA"]
periods = ["reference", "past", "present", "future_rcp45", "future_rcp85"]  # reference should go first.

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
    graph_index()

print("FINISHED")

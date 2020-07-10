from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
import pathlib
import argparse
import sys
from indices_misc import debug, clean, rcp_paths, indices_output_dir, period_name_array, period_title_array
from indices_graph_functions import plot_basemap_regions, plot_time_series
from indices_definitions import indices
from indices_merge_functions import merge_periods, merge_ts


def loop_models():
    # loop the required folders (for indices that require two parameters)
    for experiment in experiment_set:
        # loop of all models inside the experiment folder
        for model, model_path in get_subdirs(experiment):
            param_path_list = {}
            if 'ignore' in index_in and [model, args.rcp] in index_in['ignore']:  # this model/rcp should not be used for this index
                continue
            # loop of all parameters inside each model
            for param, param_path in get_subdirs(model_path):
                # if the param is the required one for the index
                if param in index_in['param']:
                    for region, region_path in get_subdirs(param_path):
                        if 'ignore' in index_in and region in index_in['ignore']:
                            continue

                        if region not in param_path_list.keys():
                            param_path_list[region] = [''] * (len(index_in['param']) + 1)  # 1 more for the out_dir
                        # loop all files inside the param path
                        for file, file_path in get_subfiles(region_path):

                            if file.startswith("._"):
                                continue  # does nothing

                            elif file.endswith(".nc"):  # check if file is .nc
                                output_dir = None
                                if "rcp45" in experiment:
                                    output_dir = indices_output_dir + '/' + index_in['name'] + '/' + region + '/rcp45/models/' + model
                                elif "rcp85" in experiment:
                                    output_dir = indices_output_dir + '/' + index_in['name'] + '/' + region + '/rcp85/models/' + model

                                pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

                                if len(index_in['param']) == 1:
                                    for function in index_in['loop_functions']:
                                        function(index=index_in, cdo=cdo, out_dir=output_dir, nc_in=file_path)
                                else:  # index with multiple param
                                    param_path_list[region][-1] = output_dir
                                    param_path_list[region][index_in['param'].index(param)] = file_path

            for region, paths in param_path_list.items():
                for function in index_in['loop_functions']:
                    if paths[-1] != '' and paths[0] != '' and paths[1] != '':
                        function(index=index_in, cdo=cdo, out_dir=paths[-1], nc_in=paths[0], nc_in2=paths[1])
                    else:
                        debug(clean("Missign param for out_dir: " + paths[-1]))


def merge_index(periods=False, ts=False):
    # loop indices folders until we find the one we want to merge
    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index_in['name']:
            continue
        for region, region_path in get_subdirs(index_path):
            # loop rcps folders until we find the one we want to merge
            for rcp, rcp_path in get_subdirs(region_path):
                if rcp != args.rcp:
                    continue
                # for function in index_in['merge_functions']:
                #    function(cdo=cdo, rcp_path=rcp_path, index=index_in)
                if periods:
                    merge_periods(cdo=cdo, rcp_path=rcp_path, index=index_in)
                if ts:
                    merge_ts(cdo=cdo, rcp_path=rcp_path, index=index_in)


def graph_map():

    import numpy as np
    from netCDF4 import Dataset

    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index_in['name']:
            continue

        for region, region_path in get_subdirs(index_path):
            if 'ignore' in index_in and region in index_in['ignore']:
                continue
            # first find the minumum and maximum for the index
            max_list = []
            min_list = []

            min_list_ref = []
            max_list_ref = []

            max_list_rel = []
            min_list_rel = []
            for rcp, rcp_path in get_subdirs(region_path):
                for season, season_path in get_subdirs(rcp_path):
                    for file, file_path in get_subfiles(season_path):
                        if file.startswith("._"):
                            pass
                        elif (file.endswith("sub.nc") and index_in['do_anom']) or (file.endswith('.nc') and 'reference' not in file and not index_in['do_anom']):
                            if any(period in file for period in period_name_array):
                                fh = Dataset(file_path, 'r')
                                param = fh.variables[index_in['cdo_name']][0:, :, :]
                                max_list.append(np.amax(param))
                                min_list.append(np.amin(param))
                                fh.close()
                        elif file.endswith("sub_rel.nc"):
                            if any(period in file for period in period_name_array):
                                fh = Dataset(file_path, 'r')
                                param = fh.variables[index_in['cdo_name']][0:, :, :]
                                max_list_rel.append(np.amax(param))
                                min_list_rel.append(np.amin(param))
                                fh.close()
                        elif 'reference' in file and file.endswith('.nc'):
                            fh = Dataset(file_path, 'r')
                            param = fh.variables[index_in['cdo_name']][0:, :, :]
                            max_list_ref.append(np.amax(param))
                            min_list_ref.append(np.amin(param))
                            fh.close()

            # The min and max may be extremes that would make the graph hard to read.
            # Instead use percentiles.
            min_sub = np.percentile(np.array(min_list), index_in['min_perc'])
            max_sub = np.percentile(np.array(max_list), index_in['max_perc'])

            min_ref = min(min_list_ref)
            max_ref = max(max_list_ref)

            if not index_in['do_anom']:  # for indices with implicit anomaly, it is better to use the same scale for reference period and other periods
                min_ref = min_sub
                max_ref = max_sub

            if (index_in['do_rel']):
                min_rel = np.percentile(np.array(min_list_rel), index_in['min_perc_rel'])
                max_rel = np.percentile(np.array(max_list_rel), index_in['max_perc_rel'])

            # plot
            for rcp, rcp_path in get_subdirs(region_path):
                if rcp != args.rcp:
                    continue
                for season, season_path in get_subdirs(rcp_path):
                    season_name = ''
                    if season != 'ANN':
                        season_name = " (" + season + ")"

                    for file, file_path in get_subfiles(season_path):
                        for period in period_name_array:
                            if period in file:
                                title = period_title_array[period_name_array.index(period)] + season_name
                                if 'future' in period:
                                    title += ' (' + str.upper(rcp).replace('5', '.5') + ')'
                                break

                        if file.startswith("._"):
                            pass
                        elif (file.endswith("sub.nc") and index_in['do_anom']) or (file.endswith('.nc') and 'reference' not in file and not index_in['do_anom']):
                            plot_basemap_regions(index_in, file_path, file_path.replace(".nc", ".png"), region, title, min_sub, max_sub)

                        elif 'reference' in file and file.endswith('.nc'):
                            plot_basemap_regions(index_in, file_path, file_path.replace(".nc", ".png"), region, title, min_ref, max_ref)

                        elif 'ignore' in index_in and region in index_in['ignore']:
                            continue

                        elif file.endswith("sub_rel.nc") and index_in['do_rel']:
                            plot_basemap_regions(index_in, file_path, file_path.replace(".nc", ".png"), region, title, min_rel, max_rel)


def graph_ts():

    import numpy as np
    from netCDF4 import Dataset

    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index_in['name']:
            continue

        # first find the minumum and maximum for the index
        max_list_models = []
        min_list_models = []

        max_list = {}
        min_list = {}
        avg6190 = {}
        models_plot = {}
        for region, region_path in get_subdirs(index_path):
            if 'ignore' in index_in and region in index_in['ignore']:
                continue
            avg6190[region] = None
            models_plot[region] = []
            max_list[region] = []
            min_list[region] = []
            for rcp, rcp_path in get_subdirs(region_path):
                for file, file_path in get_subfiles(rcp_path):
                    if file.startswith("._"):
                        continue
                    elif file.endswith("ts.nc"):
                        fh = Dataset(file_path, 'r')
                        param = fh.variables[index_in['cdo_name']][:, 0, 0]
                        max_list[region].append(np.amax(param))
                        min_list[region].append(np.amin(param))
                        fh.close()
                    elif file.endswith("Avg6190.nc"):
                        fh = Dataset(file_path, 'r')
                        avg6190[region] = fh.variables[index_in['cdo_name']][0, 0, 0]
                        fh.close()

                # all models
                for model, model_path in get_subdirs(rcp_path+"/models/"):
                    for file, file_path in get_subfiles(model_path):
                        if file.startswith("._"):
                            continue

                        elif (file.endswith("ts_anomal.nc") and index_in['do_anom']) or (file.endswith('ts.nc') and not index_in['do_anom']):
                            fh = Dataset(file_path, 'r')
                            param = fh.variables[index_in['cdo_name']][:, 0, 0]
                            max_list_models.append(np.amax(param))
                            min_list_models.append(np.amin(param))
                            fh.close()
                            models_plot[region].append(file_path)

        # plot
        for region, region_path in get_subdirs(index_path):
            if 'ignore' in index_in and region in index_in['ignore']:
                continue
            files_to_plot = []
            for rcp, rcp_path in get_subdirs(region_path):
                for file, file_path in get_subfiles(rcp_path):
                    if file.startswith("._"):
                        continue
                    elif file.endswith("ts.nc"):
                        files_to_plot.append(file_path)
                        debug(clean((file_path)))
            plot_time_series(index_in, files_to_plot, models_plot_array=models_plot[region], region=region,
                             png_name_in=region_path+"/"+index_in['name']+'_'+region+'_Models_ts.png', min=min(min_list[region]), max=max(max_list[region]), avg6190=avg6190[region])
            plot_time_series(index_in, files_to_plot, region=region,
                             png_name_in=region_path+"/"+index_in['name']+'_'+region+'_ts.png', min=min(min_list[region]), max=max(max_list[region]), avg6190=avg6190[region])

# __________________Here starts the script ______________________


print()

parser = argparse.ArgumentParser()
parser.add_argument("--loop", help="Loop all the models and calculates the index", action="store_true")
parser.add_argument("--merge", help="Merge the index from all the models")
parser.add_argument("--graph", help="Graph the merged index")
parser.add_argument("--index", help="Index to calculate")
parser.add_argument("--rcp", help="rcp experiment: posisble values")

args = parser.parse_args()
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if args.index not in indices:
    debug(clean(("Index not supported. Here is a list of the supported indeces: ")))
    debug(list(indices.keys()))
    sys.exit()
index_in = indices[args.index]
debug(clean((index_in['name'] + ": " + index_in['description'])))
debug(clean(("Required Parameter(s): " + str(index_in['param']))))

if 'cdo_fun' in index_in:
    debug(clean((index_in['cdo_fun'])))

if args.rcp not in rcp_paths:
    debug(clean(("RCP not supported. Here is a list of the supported RCPs:")))
    debug(clean((list(rcp_paths.keys()))))
    sys.exit()

experiment_set = set([])
for param in index_in['param']:
    experiment_set.add(rcp_paths[args.rcp][param])
debug(clean(("Experiment Path: " + str(experiment_set))))

print()
# input("Press Enter to continue...")
print()

# # Initialize CDO
cdo = Cdo()
cdo.degub = True

if args.loop:
    debug(clean(("Looping all models")))
    print()
    loop_models()


elif args.merge == 'map':
    debug(clean(("Merging maps")))
    print()
    merge_index(periods=True)

elif args.merge == 'ts':
    debug(clean(("Merging ts")))
    print()
    merge_index(ts=True)

elif args.merge == 'all':
    debug(clean(("Merging maps and ts")))
    print()
    merge_index(periods=True, ts=True)


elif args.graph == 'ts':
    debug(clean(("Creating time series")))
    graph_ts()

elif args.graph == 'map':
    debug(clean(("Creating colormap")))
    graph_map()

print()
debug(clean(("FINISHED")))
print()

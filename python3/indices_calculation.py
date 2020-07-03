from cdo import *
from useful_functions import get_subdirs
from useful_functions import get_subfiles
from useful_functions import plot_basemap_regions
from useful_functions import plot_time_series
import pathlib
import argparse
import sys
import shutil
import os.path
import logging
from indices_definitions import indices
from folder_definitions import rcp_paths, indices_output_dir


# def selyear_index(index_in, param_in, nc_in=None, out_dir_in=None, first_year_in=None):
#     '''
#     For indexes that need a selyear to generate a timeseries, like sdii
#     '''
#     index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index
#
#     if index_cdo_function is None:
#         logger.debug("Error, not an index from etccdi")
#         return -1
#
#     if out_dir_in is None:
#         logger.debug("Error, output dir is was not specified")
#         return -1
#
#     # if a first year is given, start from there, otherwise, start from the first year on the file name
#     first_year_file = ((nc_in.split("_"))[-2].split("-")[0])[0:4]
#     first_year = first_year_in
#     if first_year is None:
#         first_year = first_year_file
#
#     last_year = ((nc_in.split("_"))[-2].split("-")[1])[0:4]
#     nc_out_array = ""
#     if first_year_file != "1861" or last_year != "2090":
#         logger.debug("Error in first or last year "+first_year_file+"-"+last_year)
#         return
#
#     nc_out_fldmean = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_" + index_in + "_ts.nc").replace(first_year_file, first_year)
#     # Create nc files for field mean and year mean.
#     if os.path.exists(nc_out_fldmean):  # False:
#         logger.debug("%s already exists", nc_out_fldmean)
#         return
#
#     pathlib.Path(out_dir_in + '/years/').mkdir(parents=True, exist_ok=True)
#
#     for year in range(int(first_year), int(last_year)+1):
#         cdo_selyear_command = "-selyear,"+str(year)
#         nc_out = out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_" + index_in + str(year)+".nc"
#         # try:
#         logger.debug(nc_out)
#         # force to False so if the file already exists is not overwritten
#         index_cdo_function(input=cdo_selyear_command+" "+nc_in,
#                            output=nc_out, options='-f nc', force=False, returnCdf=False)
#         nc_out_array = nc_out_array+" "+nc_out
#         # except CDOException:
#         #    logger.debug("CDO Exception")
#     # try:
#     nc_out_merge = (out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_" + index_in + ".nc").replace(first_year_file, first_year)  # adapt the name to the actual first year used
#     cdo.mergetime(input=nc_out_array, output=nc_out_merge, options='-f nc', force=False, returnCdf=False)
#     cdo.fldmean(input="-setreftime,1850-01-01,00:00:00 "+nc_out_merge, output=nc_out_fldmean, options="-f nc", force=False, returnCdf=False)
#
#     logger.debug("")
#     logger.debug(nc_out_fldmean)
#     logger.debug("")
#     try:
#         shutil.rmtree(out_dir_in + '/years/')
#     except OSError as e:
#         logger.debug("Error: %s" % (e.strerror))
#
#     except CDOException:
#         logger.debug("CDO Exception")
#
#
# def direct_periods_index(index_in, param_in, nc_in=None, out_dir_in=None):
#     '''
#     For indices that give a single value for the timeperiod, like sdii
#     Generate given index for the following 4 periods:
#     Past        : 1861 1890
#     Reference   : 1961 1990
#     Present     : 1991 2020
#     Future      : 2061 2090
#
#     The index is calculated for seasons ANN DJF and JJA
#     '''
#     index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index
#
#     if index_cdo_function is None:
#         logger.debug("Error, not an index from etccdi")
#         return -1
#
#     if out_dir_in is None:
#         logger.debug("Error, output dir  was not specified")
#         return -1
#     if nc_in is None:
#         logger.debug("Error, nc_in was not specified")
#         return -1
#
#     for season in seasons:
#         pathlib.Path(out_dir_in + '/' + season).mkdir(parents=True, exist_ok=True)
#         cdo_season_command = sel_season+season
#         for year_range, name in zip(year_range_array, period_name_array):
#             cdo_year_command = sel_year_range+year_range
#             nc_out = out_dir_in + "/" + season + "/" + pathlib.Path(nc_in).stem + "_" + index_in + "_" + name + ".nc"
#
#             logger.debug(nc_out)
#             try:
#                 # force to False so if the file already exists is not overwritten
#                 index_cdo_function(input=cdo_year_command+" "+cdo_season_command+" "+nc_in,
#                                    output=nc_out, options='-f nc', force=False, returnCdf=False)
#             except CDOException:
#                 logger.debug("CDO error")  # lik


def percentile_index(index_in, param_in, nc_in=None, out_dir_in=None, isTemp=False):
    '''
    Calculate percentile indices.
    For temperature that require bootstrapping first calculates runmin and runmax (if not already generated)
    '''
    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        logger.debug("Error, output dir is was not specified")
        return -1

    nc_out_runmin = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_runmin.nc")
    nc_out_runmax = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_runmax.nc")
    nc_out_percentile = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_"+index_in+".nc")

    windowDays = ""
    bootstrapping = "1961,1990"

    if isTemp:
        windowDays = "5"  # Number of timestamps
        # Genreate runmin and runmax (if not already generated)
        logger.debug(nc_out_runmin)
        cdo.ydrunmin(windowDays, input=nc_in, output=nc_out_runmin, options='-f nc', force=False, returnCdf=False)
        logger.debug(nc_out_runmax)
        cdo.ydrunmax(windowDays, input=nc_in, output=nc_out_runmax, options='-f nc', force=False, returnCdf=False)
        windowDays = "5,"  # Number of timestamps, add comma for next command
    else:
        # Genreate runmin and runmax (if not already generated)
        # timmin, timmax calculate the min and max in time (so the result is a point for each grid)
        # setrtomiss sets the values in the range to missing value. Because we are interested in days with precipitation larger than 1, wet-day precipitation (PR > 1 mm)
        # then set precipitation in range 0,1 to the missing value (to ignore it)
        logger.debug(nc_out_runmin)
        cdo.timmin(input="-setrtomiss,0,1 "+nc_in, output=nc_out_runmin, options='-f nc', force=False, returnCdf=False)
        logger.debug(nc_out_runmax)
        cdo.timmax(input="-setrtomiss,0,1 "+nc_in, output=nc_out_runmax, options='-f nc', force=False, returnCdf=False)

    logger.debug(nc_out_percentile)
    index_cdo_function(windowDays+bootstrapping, input=nc_in+" "+nc_out_runmin+" "+nc_out_runmax,
                       output=nc_out_percentile, options='-f nc', force=False, returnCdf=False)
    logger.debug("")


def normal_index(index_in, param_in, nc_in, out_dir_in):
    '''
    Calculate "normal" indices, that generate a matrix out, without needing any additional input parameters
    '''
    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index
    nc_out_normal = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_"+index_in+".nc")

    additional_command = ""
    additional_parameters = ""
    if index == "rx5day":
        additional_command = "-runsum,5 "
        if args.mon:
            additional_parameters = "50,freq=month"
            nc_out_rx5day = nc_out_normal
            nc_out_normal = nc_out_rx5day.replace(".nc", "_withDay17.nc")

    index_cdo_function(additional_parameters, input=additional_command + nc_in, output=nc_out_normal, options='-f nc', force=True, returnCdf=False)

    if index == "rx5day" and args.mon:
        cdo.delete("day=17", input="-delete,day=16,hour=12 "+nc_out_normal, output=nc_out_rx5day, options='-f nc', force=True, returnCdf=False)


def manual_index(index_in, param_in, nc_in, out_dir_in):
    '''
    Calculate indices manually
    '''
    nc_out = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_"+index_in+".nc")
    long_name = {
        "txx": "\"Monthly maximum value of daily maximum temperature\"",
        "tnx": "\"Monthly maximum value of daily minimum temperature\"",
        "txn": "\"Monthly minimum value of daily maximum temperature\"",
        "tnn": "\"Monthly minimum value of daily minimum temperature\""
    }

    operation = {
        "txx": " -monmax ",
        "tnx": " -monmax ",
        "txn": " -monmin ",
        "tnn": " -monmin "
    }

    cdo.chname(req_param+","+index+"ETCCDI", input="-setattribute,"+req_param+"@long_name="+long_name[index_in]+" -chunit,K,C -subc,273.15 "+operation[index] + nc_in,
               output=nc_out, options='-f nc', force=True, returnCdf=False)


def generate_periods(index_in, out_dir_in=None):

    if out_dir_in is None:
        logger.debug("Error, output_dir_in is was not specified")
        return -1

    for year_range, name in zip(year_range_array, period_name_array):
        cdo_year_command = sel_year_range+year_range
        for file, file_path in get_subfiles(out_dir_in):
            if file.startswith("._"):
                continue  # does nothing
            elif file.endswith(index_in+".nc"):  # if file ends with index.nc, it is the pure idex file, with matrix values (temp and field)
                pathlib.Path(out_dir_in + "/ANN/").mkdir(parents=True, exist_ok=True)
                nc_out = out_dir_in + "/ANN/" + pathlib.Path(file_path).stem + "_" + name + ".nc"
                logger.debug(nc_out)
                logger.debug("")
                cdo.timmean(input="-setreftime,1850-01-01,00:00:00 "+cdo_year_command + " " + file_path, output=nc_out, options='-f nc', force=True, returnCdf=False)


def generate_ts(index_in, out_dir_in=None):
    if out_dir_in is None:
        logger.debug("Error, output_dir_in is was not specified")
        return -1

    for file, file_path in get_subfiles(out_dir_in):
        if file.startswith("._"):
            continue  # does nothing
        elif file.endswith(index_in+".nc"):  # if file ends with index.nc, it is the pure idex file, with matrix values (temp and field)
            nc_out = out_dir_in + "/" + pathlib.Path(file_path).stem + "_ts.nc"
            logger.debug(nc_out)
            logger.debug("")
            cdo.fldmean(input="-setreftime,1850-01-01,00:00:00 "+file_path, output=nc_out, options='-f nc', force=True, returnCdf=False)


def loop_models():
    logger.debug("Calculate %s using %s" % (index, req_param))

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
                                # first_year = "1996"  # To avoid calculating indices again for the historical data
                                output_dir = indices_output_dir + '/' + index + '/' + region + '/rcp85/models/' + model

                            pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

                            if index in ("sdii"):
                                selyear_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir, first_year_in=first_year)
                                direct_periods_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir)
                                logger.debug("")

                            elif index in ("r95p"):
                                percentile_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir, isTemp=False)
                                generate_periods(index_in=index, out_dir_in=output_dir)
                                generate_ts(index_in=index, out_dir_in=output_dir)

                            elif index in ("tx90p"):
                                percentile_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir, isTemp=True)
                                generate_periods(index_in=index, out_dir_in=output_dir)
                                generate_ts(index_in=index, out_dir_in=output_dir)

                            elif index in ("fd", "rx5day", "r20mm", "cdd", "su", "tr"):
                                normal_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir)
                                generate_periods(index_in=index, out_dir_in=output_dir)
                                generate_ts(index_in=index, out_dir_in=output_dir)

                            elif index in ("txx", "tnx", "txn", "tnn"):
                                manual_index(index_in=index, param_in=param, nc_in=file_path, out_dir_in=output_dir)
                                generate_periods(index_in=index, out_dir_in=output_dir)
                                generate_ts(index_in=index, out_dir_in=output_dir)


def merge_periods(rcp_path, index, do_seasons=False, do_sub=False):

    if do_seasons is False:
        seasons_local = ["ANN"]     # No seasons
    else:
        seasons_local = seasons  # the globally defined seasons
    for season in seasons_local:
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

                cdo.remapbil(target_grid_file, input=index_file, output=index_file_regrid, froce=True)  # regrid to target grid

                index_all_models += index_file_regrid + ' '

            if index_all_models == '':
                logger.debug("No files found for Season %s and period %s" % (season, period))
            else:
                nc_ensmean_out = rcp_path + '/' + season + '/' + index + "_" + period + '.nc'
                try:
                    logger.debug(nc_ensmean_out)
                    # logger.debug(index_all_models)
                    cdo.enspctl("50", input=index_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)  # median = 50th percentil

                    if do_sub:
                        if "reference" in period:
                            nc_ensmean_reference = nc_ensmean_out

                        elif nc_ensmean_reference != '':  # substract reference from period. Only for non reference period, if reference file has been found.
                            nc_ensmean_sub_out = rcp_path + '/' + season + '/' + index + "_" + period + '_sub.nc'
                            logger.debug(nc_ensmean_sub_out)
                            cdo.sub(input=nc_ensmean_out + " " + nc_ensmean_reference, output=nc_ensmean_sub_out, options='-f nc', force=True, returnCdf=False)
                except CDOException:
                    logger.debug("CDO error")
            logger.debug("\n\n")


def merge_ts(rcp_path, param, region, do_anom=False):     # ts= timeseries
    array_all_models = ""
    file_path_list = []
    for model, model_path in get_subdirs(rcp_path+"/models/"):
        for file, file_path in get_subfiles(model_path):
            if file.startswith("._"):
                continue

            elif file.endswith("ts.nc"):  # check if end is ts.nc which means it is a time series and needs to be ensembled
                #if "BCC-CSM1.1" not in file:
                    if do_anom:
                        nc_avg_61_90 = file_path.replace('_ts.nc', '_avg_61_90.nc')
                        nc_anomal = file_path.replace('_ts.nc', '_ts_anomal.nc')

                        year_range = "-selyear,1961/1990"
                        avg_61_90_val = cdo.timmean(input=year_range+" "+file_path, output=nc_avg_61_90, force=True, options='-f nc', returnCdf=True).variables[index+"ETCCDI"][0, 0, 0]

                        cdo.subc(avg_61_90_val, input=file_path, force=True, output=nc_anomal)  # substract il file 61-90

                        array_all_models += nc_anomal + ' '
                        file_path_list.append(nc_anomal)  # only to plot individually for debbugging
                    else: # no anomaly required
                        array_all_models += file_path + ' '
                        file_path_list.append(file_path)  # only to plot individually for debbugging

    if array_all_models == '':
        logger.debug("No files found in %s" % rcp_path)
    else:
        if do_anom:
            plot_time_series(file_path_list, png_name_in=rcp_path + '/' + index + "_allModels_ts_anom.png", param_in=param, region=region, h_line=0)
        else:
            plot_time_series(file_path_list, png_name_in=rcp_path + '/' + index + "_allModels_ts.png", param_in=param, region=region, h_line=0)
        percentil_array = ["25", "50", "75"]  # median = 50th percentil
        for percentil in percentil_array:
            nc_ensmean_out = rcp_path + '/' + index + '_percent_' + percentil + '_ts.nc'

            if percentil == "mean":
                cdo.ensmean(input=array_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)
            else:
                cdo.enspctl(percentil, input=array_all_models, output=nc_ensmean_out, options='-f nc', force=True, returnCdf=False)  # Ensemble percentiles

            if do_anom:
                # find anomalie
                nc_avg_61_90 = nc_ensmean_out.replace('_ts.nc', '_avg_61_90.nc')
                nc_anomal = nc_ensmean_out.replace('_ts.nc', '_ts_anomal.nc')

                year_range = "-selyear,1961/1990"
                avg_61_90_val = cdo.timmean(input=year_range+" "+nc_ensmean_out, output=nc_avg_61_90, options='-f nc', returnCdf=True).variables[index+"ETCCDI"][0, 0, 0]

                cdo.subc(avg_61_90_val, input=nc_ensmean_out, output=nc_anomal)  # substract il file 61-90
                logger.debug(nc_anomal)


def merge_index():
    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index:
            continue
        for region, region_path in get_subdirs(index_path):
            for rcp, rcp_path in get_subdirs(region_path):
                if rcp != args.rcp:
                    continue
                if index_l in ("sdii"):
                    # merge_periods(rcp_path, index_l, do_seasons=True, do_sub=True)
                    merge_ts(rcp_path, index+"ETCCDI", region, do_anom=True)

                elif index_l in ("tx90p"):
                    merge_periods(rcp_path, index_l, do_seasons=False, do_sub=False)
                    merge_ts(rcp_path, index+"ETCCDI", region, do_anom=False)

                elif index_l in ("r95p", "fd", "rx5day", "r20mm", "cdd", "su", "tr", "txx", "txn", "tnx", "tnn"):
                    merge_periods(rcp_path, index_l, do_seasons=False, do_sub=True)
                    merge_ts(rcp_path, index+"ETCCDI", region, do_anom=True)


def graph_map():
    # bounds = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1]   # 18 for sdii
    #bounds = [-30, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300]                     # for r95p
    # bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]                         # for tx90p
    # bounds = [-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]        # for tx90p RCP85
    # bounds = [-60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10]              # FD
    #bounds = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]                       # R20mm
    #bounds = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]                       # CDD
    bounds = [-30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]                         # for SU

    #colors = ['darkred', 'red', 'orangered', 'tomato', 'salmon', 'lightcoral',                                      # for sdii and r95p
    #          'lightsalmon', 'papayawhip', 'snow', 'paleturquoise', 'lightskyblue', 'skyblue', 'turquoise',
    #          'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue', 'midnightblue']
    # colors = ['navy', 'blue', 'mediumblue', 'dodgerblue', 'deepskyblue', 'lightskyblue',                           # for tx90p  RCP45
    #          'lightblue', 'moccasin', 'yellow', 'gold', 'orange', 'darkorange',
    #          'coral', 'tomato', 'red', 'darkred']
    #colors = ['mediumturquoise', 'paleturquoise', 'lightcyan', 'snow', 'lemonchiffon', 'yellow', 'gold', 'orange',   # FOR TX90P RCP85
    #          'darkorange', 'lightcoral', 'coral', 'tomato', 'orangered', 'red', 'firebrick', 'crimson', 'darkviolet', 'purple', 'indigo']
    # colors = ['darkred', 'firebrick', 'red', 'orangered', 'tomato', 'salmon', 'coral', 'darkorange', 'orange', 'gold', 'yellow', 'lemonchiffon', 'snow',  # FD
    #          'paleturquoise', 'mediumturquoise', 'turquoise']
    #colors = ['orangered', 'tomato', 'salmon', 'lightcoral',                                                        # for r20mm
    #          'lightsalmon', 'snow', 'paleturquoise', 'lightskyblue', 'skyblue', 'turquoise',
    #          'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue', 'midnightblue']
    #colors = ['red', 'orangered', 'tomato', 'salmon', 'lightcoral', 'snow', 'lightskyblue', 'turquoise',             #CDD
    #          'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue', 'midnightblue']
    colors = ['mediumblue', 'deepskyblue', 'lightskyblue', 'snow', 'moccasin', 'yellow', 'gold', 'orange', 'darkorange',
              'coral', 'salmon', 'tomato', 'red', 'darkred']

    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index:
            continue

        param = index+"ETCCDI"
        for region, region_path in get_subdirs(index_path):
            for rcp, rcp_path in get_subdirs(region_path):
                if rcp != args.rcp:
                    continue
                for season, season_path in get_subdirs(rcp_path):
                    for file, file_path in get_subfiles(season_path):
                        if file.startswith("._"):
                            pass
                        elif file.endswith(".nc"):  # if files ends with _sub.nc is the result of a substraction, and needs to be graphed
                            for period in period_name_array:
                                if period in file:
                                    title = index + " in the " + period + " for season " + season + " in region " + region
                                    plot_basemap_regions(file_path, file_path.replace(".nc", ".png"), param, region, title, cdo, bounds, colors, colors[-1], colors[0])


def graph_ts():
    for index_l, index_path in get_subdirs(indices_output_dir):
        if index_l != index:
            continue

        param = index+"ETCCDI"
        for region, region_path in get_subdirs(index_path):
            files_to_plot = []
            for rcp, rcp_path in get_subdirs(region_path):
                # if rcp != args.rcp:
                #    continue
                # files_to_plot = []
                for file, file_path in get_subfiles(rcp_path):
                    if file.startswith("._"):
                        continue
                    elif file.endswith("ts.nc"):  # if files ends with anomal.nc is the result of a substraction, and needs to be graphed
                    # elif file.endswith("ts_anomal.nc"):   # if files ends with anomal.nc is the result of a substraction, and needs to be graphed
                        files_to_plot.append(file_path)
                        logger.debug(file_path)
                # plot_time_series(files_to_plot, png_name_in=rcp_path+"/"+index+"_ts.png", param_in=param, region=region, h_line=0)    # just for 1 rcp

            plot_time_series(files_to_plot, png_name_in=region_path+"/"+index+"_ts.png", param_in=param, region=region, h_line=0)
            # plot_time_series(files_to_plot, png_name_in=region_path+"/"+index+"_ts_anomal.png", param_in=param, region=region, h_line=0)


# __________________Here starts the script ______________________

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
print()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--full", help="Perform all of the operations", action="store_true")
parser.add_argument("-l", "--loop", help="Loop all the models and calculates the index", action="store_true")
parser.add_argument("-m", "--merge", help="Merge the index from all the models", action="store_true")
parser.add_argument("-g", "--graph", help="Graph the merged index", action="store_true")
parser.add_argument("-i", "--index", help="Index to calculate")
parser.add_argument("-r", "--rcp", help="rcp experiment: posisble values")
parser.add_argument("--mon", help="Calculate the index in a monthy basis. Valid for rx5day", action="store_true")

args = parser.parse_args()
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if args.index not in indices:
    logger.debug("Index not supported. Here is a list of the supported indeces: ")
    logger.debug(list(indices.keys()))
    sys.exit()
index = indices[args.index]
logger.debug(args.index + ": " + index['description'])
logger.debug("Required Parameter(s): " + str(index['param']))

if args.rcp not in rcp_paths:
    logger.debug("RCP not supported. Here is a list of the supported RCPs:")
    logger.debug(list(rcp_paths.keys()))
    sys.exit()
experiment = rcp_paths[args.rcp][index['param']]
logger.debug("Experiment Path: " + experiment)




year_range_array = ["1961/1990", "1861/1890", "1991/2020", "2061/2090"]  # reference should go first, to calculate the subs
period_name_array = ["reference_1961-1990", "past_1861-1890", "present_1991-2020", "future_2061-2090"]
sel_year_range = "-selyear,"
# seasons = annual  Dec-Feb    Jun-Aug
seasons = ["ANN",   "DJF",   "JJA", "AM"]  # April-May
sel_season = "-select,season="


# # Initialize CDO
cdo = Cdo()
cdo.degub = True

# if args.full or args.loop:
#     logger.debug("Looping all the models")
#     loop_models()
#
# if args.full or args.merge:
#     logger.debug("Merging index")
#     merge_index()
#
# if args.full or args.graph:
#     logger.debug("Creating graphs")
#     graph_map()
#     graph_ts()

logger.debug("FINISHED")
print()

# This file contains the funcitons required for the merge of results from different models.
# Only two functions are required, as the merge should be the same for all indices, with some small variations


def merge_periods(cdo, rcp_path, index):

    from indices_misc import logger, clean
    from indices_misc import period_name_array
    import pathlib

    for season in index['seasons']:
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

                cdo.remapbil(target_grid_file, input=index_file, output=index_file_regrid, froce=False)  # regrid to target grid

                index_all_models += index_file_regrid + ' '

            if index_all_models == '':
                logger.debug(clean(("No files found for Season %s and period %s" % (season, period))))
            else:
                nc_ensmean_out = rcp_path + '/' + season + '/' + index['name'] + "_" + period + '.nc'
                logger.debug(clean((nc_ensmean_out)))
                cdo.enspctl("50", input=index_all_models, output=nc_ensmean_out, options='-f nc', force=False, returnCdf=False)  # median = 50th percentil

                if index['do_anom']:
                    if "reference" in period:
                        nc_ensmean_reference = nc_ensmean_out

                    elif nc_ensmean_reference != '':  # substract reference from period. Only for non reference period, if reference file has been found.
                        nc_ensmean_sub_out = rcp_path + '/' + season + '/' + index['name'] + "_" + period + '_sub.nc'
                        nc_ensmean_sub_rel_out = rcp_path + '/' + season + '/' + index['name'] + "_" + period + '_sub_rel.nc'
                        logger.debug(clean((nc_ensmean_sub_out)))
                        cdo.sub(input=nc_ensmean_out + " " + nc_ensmean_reference, output=nc_ensmean_sub_out, options='-f nc', force=False, returnCdf=False)
                        logger.debug(clean((nc_ensmean_sub_rel_out)))
                        setrtomiss = ' '
                        if 'setrtomiss' in index:
                            setrtomiss = index['setrtomiss']
                        cdo.mulc(100, input="-setattribute,"+index['cdo_name']+"@units=\"Relative Change (%)\" -div "+nc_ensmean_sub_out + setrtomiss
                                 + ' -abs ' + nc_ensmean_reference, output=nc_ensmean_sub_rel_out, options='-f nc', force=True, returnCdf=False)


def merge_ts(cdo, rcp_path, index):     # ts= timeseries

    from indices_misc import logger, clean
    from useful_functions import get_subdirs
    from useful_functions import get_subfiles
    from indices_graph_functions import plot_time_series

    array_all_models = ""
    file_path_list = []  # Just to plot all models
    array_all_models_avg6190 = ""

    for model, model_path in get_subdirs(rcp_path+"/models/"):
        for file, file_path in get_subfiles(model_path):
            if file.startswith("._"):
                continue

            elif file.endswith("ts.nc"):  # check if end is ts.nc which means it is a time series and needs to be ensembled
                if index['do_anom']:  # if index requires anomalie, before merging, calculate it
                    nc_avg_61_90 = file_path.replace('_ts.nc', '_avg_61_90.nc')
                    nc_anomal = file_path.replace('_ts.nc', '_ts_anomal.nc')

                    year_range = "-selyear,1961/1990"
                    avg_61_90_val = cdo.timmean(input=year_range+" "+file_path, output=nc_avg_61_90, force=False, options='-f nc',
                                                returnCdf=True).variables[index['cdo_name']][0, 0, 0]

                    cdo.subc(avg_61_90_val, input=file_path, force=False, output=nc_anomal)  # substract the timeman of period 61-90

                    array_all_models += nc_anomal + ' '
                    file_path_list.append(nc_anomal)  # only to plot individually for debbugging
                    array_all_models_avg6190 += nc_avg_61_90 + ' '
                else:  # no anomaly required
                    array_all_models += file_path + ' '
                    file_path_list.append(file_path)  # only to plot individually for debbugging

    if array_all_models == '':
        logger.debug(clean(("No files found in %s" % rcp_path)))
    else:
        if index['do_anom']:
            plot_time_series(index=index, file_path_in_array=file_path_list, png_name_in=rcp_path + '/' + index['name'] + "_allModels_ts_anom.png")
        else:
            plot_time_series(index, file_path_list, png_name_in=rcp_path + '/' + index['name'] + "_allModels_ts.png")

        percentil_array = ["25", "50", "75"]  # median = 50th percentil
        for percentil in percentil_array:
            nc_ensmean_out = rcp_path + '/' + index['name'] + '_percent_' + percentil + '_ts.nc'

            if percentil == "mean":
                cdo.ensmean(input=array_all_models, output=nc_ensmean_out, options='-f nc', force=False, returnCdf=False)
            else:
                cdo.enspctl(percentil, input=array_all_models, output=nc_ensmean_out, options='-f nc', force=False, returnCdf=False)  # Ensemble percentiles

            if index['do_anom']:
                nc_ensmean_out_medianOfAvg6190 = rcp_path + '/' + index['name'] + '_percent_50_ts_medianOfAvg6190.nc'
                cdo.ensmean(input=array_all_models_avg6190, output=nc_ensmean_out_medianOfAvg6190, options='-f nc', force=False, returnCdf=False)

                # find anomalie (this result is not really used)
                nc_avg_61_90 = nc_ensmean_out.replace('_ts.nc', '_avg_61_90.nc')
                nc_anomal = nc_ensmean_out.replace('_ts.nc', '_ts_anomal.nc')

                year_range = "-selyear,1961/1990"
                avg_61_90_val = cdo.timmean(input=year_range+" "+nc_ensmean_out, output=nc_avg_61_90, options='-f nc', force=False,
                                            returnCdf=True).variables[index['cdo_name']][0, 0, 0]

                cdo.subc(avg_61_90_val, input=nc_ensmean_out, output=nc_anomal)  # substract il file 61-90
                logger.debug(clean((nc_anomal)))

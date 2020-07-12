# This file contains the funcitons required for the actual index calculation (for each model)
# As there are different types of indices, several functions are required.


def selyear_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    For indexes that need a selyear to generate a timeseries, like sdii
    '''
    import shutil
    import os.path
    import pathlib
    from indices_misc import logger, clean

    index_cdo_function = getattr(cdo, index['cdo_fun'])  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug(clean(("Error, not an index from etccdi")))
        return

    first_year_file = ((nc_in.split("_"))[-2].split("-")[0])[0:4]
    last_year_file = ((nc_in.split("_"))[-2].split("-")[1])[0:4]

    # To avoid calculating indices again for the historical data
    if False and "rcp85" in nc_in:
        first_year = "2005"
    else:
        first_year = first_year_file

    nc_out_array = ""

    if first_year_file != "1861" or last_year_file != "2090":
        logger.debug(clean(("Error in first or last year "+first_year_file+"-"+last_year_file)))
        return

    nc_out_fldmean = (out_dir + '/' + pathlib.Path(nc_in).stem + "_" + index['name'] + "_ts.nc").replace(first_year_file, first_year)
    # Create nc files for field mean and year mean.
    if os.path.exists(nc_out_fldmean):  # False:
        logger.debug(clean(("%s already exists", nc_out_fldmean)))
        return

    pathlib.Path(out_dir + '/years/').mkdir(parents=True, exist_ok=True)

    add_params = ''
    if 'add_params' in index:
        add_params = index['add_params']

    # loop all years in the range and calculate the index
    for year in range(int(first_year), int(last_year_file)+1):
        cdo_selyear_command = "-selyear,"+str(year)
        nc_out = out_dir + '/years/' + pathlib.Path(nc_in).stem + "_" + index['name'] + str(year)+".nc"

        logger.debug(clean((nc_out)))
        index_cdo_function(add_params, input=cdo_selyear_command+" "+nc_in,
                           output=nc_out, options='-f nc', force=False, returnCdf=False)

        # add the out nc to the array
        nc_out_array = nc_out_array+" "+nc_out

    # after calculating index for each year, merge them.
    nc_out_merge = (out_dir + '/years/' + pathlib.Path(nc_in).stem + "_" + index['name'] + ".nc").replace(first_year_file, first_year)  # adapt the name to the actual first year used
    cdo.mergetime(input=nc_out_array, output=nc_out_merge, options='-f nc', force=False, returnCdf=False)

    # fldmean to obtain a timeseries
    cdo.fldmean(input="-setreftime,1850-01-01,00:00:00 "+nc_out_merge, output=nc_out_fldmean, options="-f nc", force=False, returnCdf=False)

    logger.debug(clean(("")))
    logger.debug(clean((nc_out_fldmean)))
    logger.debug(clean(("")))
    try:
        shutil.rmtree(out_dir + '/years/')
    except OSError as e:
        logger.debug(clean(("Error: %s" % (e.strerror))))


def direct_periods_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    For indices that give a single value for the timeperiod, like sdii
    Generate given index for the following 4 periods:
    Past        : 1861 1890
    Reference   : 1961 1990
    Present     : 1991 2020
    Future      : 2061 2090

    The index is calculated for seasons ANN DJF and JJA
    '''
    import pathlib
    from indices_misc import logger, clean
    from indices_misc import period_range_array, period_name_array
    from os import path

    index_cdo_function = getattr(cdo, index['cdo_fun'])  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug(clean(("Error, not an index from etccdi")))
        return -1

    if 'add_fun' in index:
        index_add_function = getattr(cdo, index['add_fun'])  # get the cdo function coressponding to the input index

        if index_add_function is None:
            logger.debug(clean(("Error, not an function from cdo")))
            return -1

    add_params = ''
    if 'add_params' in index:
        add_params = index['add_params']

    for season in index['seasons']:
        pathlib.Path(out_dir + '/' + season).mkdir(parents=True, exist_ok=True)
        cdo_season_command = "-select,season="+season
        for year_range, name in zip(period_range_array, period_name_array):
            cdo_year_command = "-selyear,"+year_range
            nc_out = out_dir + "/" + season + "/" + pathlib.Path(nc_in).stem + "_" + index['name'] + "_" + name + ".nc"
            if path.exists(nc_out):  # False:
                logger.debug(clean(("%s already exists", nc_out)))
                return

            logger.debug(clean((nc_out)))
            if 'add_fun' not in index:
                index_cdo_function(add_params, input=cdo_year_command+" "+cdo_season_command+" "+nc_in,
                                   output=nc_out, options='-f nc', force=False, returnCdf=False)
            else:
                cdo_function_command = '-'+index['cdo_fun']+','+add_params
                index_add_function(index['add_fun_params'], input=cdo_function_command+' '+cdo_year_command+" "+cdo_season_command+" "+nc_in,
                                   output=nc_out, options='-f nc', force=False, returnCdf=False)


def percentile_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    Calculate percentile indices.
    For temperature indices that require bootstrapping first calculates ydrunmin and ydrunmax (if not already generated)
    For precipitation indices just uses the timmin and timmax
    '''
    from indices_misc import logger, clean
    import pathlib

    index_cdo_function = getattr(cdo, index['cdo_fun'])  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug(clean(("Error, not an index from etccdi")))
        return -1

    nc_out_runmin = (out_dir + '/' + pathlib.Path(nc_in).stem + "_runmin.nc")
    nc_out_runmax = (out_dir + '/' + pathlib.Path(nc_in).stem + "_runmax.nc")
    nc_out_percentile = (out_dir + '/' + pathlib.Path(nc_in).stem + "_"+index['name']+".nc")

    windowDays = ""
    bootstrapping = "1961,1990"

    if index['isTemp']:
        windowDays = "5,"  # Number of timestamps required for Temp percentiles
        # Genreate runmin and runmax (if not already generated)
        cdo.ydrunmin(windowDays, input=nc_in, output=nc_out_runmin, options='-f nc', force=False, returnCdf=False)
        cdo.ydrunmax(windowDays, input=nc_in, output=nc_out_runmax, options='-f nc', force=False, returnCdf=False)
    else:
        # Genreate runmin and runmax (if not already generated)
        # timmin, timmax calculate the min and max in time (so the result is a point for each grid)
        # setrtomiss sets the values in the range to missing value. Because we are interested in days with precipitation larger than 1, wet-day precipitation (PR > 1 mm)
        # then set precipitation in range -50,1 to the missing value (to ignore it)
        cdo.timmin(input="-setrtomiss,-50,1 "+nc_in, output=nc_out_runmin, options='-f nc', force=False, returnCdf=False)
        cdo.timmax(input="-setrtomiss,-50,1 "+nc_in, output=nc_out_runmax, options='-f nc', force=False, returnCdf=False)

    logger.debug(clean((nc_out_runmin)))
    logger.debug(clean((nc_out_runmax)))
    logger.debug(clean((nc_out_percentile)))
    index_cdo_function(windowDays+bootstrapping, input=nc_in+" "+nc_out_runmin+" "+nc_out_runmax,
                       output=nc_out_percentile, options='-f nc', force=False, returnCdf=False)
    logger.debug(clean(("")))


def duration_percentile_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    Calculate histogram indices.
    This indices are calculated in three steps:
    1 - Calculate the ydrunmin and ydrunmax
    2 - Calculate the required percentile
    3 - Calculate the index
    '''
    from indices_misc import debug, clean
    import pathlib

    index_cdo_function = getattr(cdo, index['cdo_fun'])  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        debug(clean(("Error, not an index from etccdi")))
        return -1

    nc_out_runmin = (out_dir + '/' + pathlib.Path(nc_in).stem + "_ydrunmin.nc")
    nc_out_runmax = (out_dir + '/' + pathlib.Path(nc_in).stem + "_ydrunmax.nc")
    nc_out_th = (out_dir + '/' + pathlib.Path(nc_in).stem + "_thr"+index['percentile']+".nc")
    nc_out_index = (out_dir + '/' + pathlib.Path(nc_in).stem + "_"+index['name']+".nc")

    windowDays = "5"
    selyear = "-selyear,1961/1990 "
    readMethod = "circular"
    percentileMethod = "rtype8"

    # Genreate runmin and runmax in reference period (if not already generated)
    cdo.ydrunmin(windowDays, input=selyear+nc_in, output=nc_out_runmin, options='-f nc', force=False, returnCdf=False)
    cdo.ydrunmax(windowDays, input=selyear+nc_in, output=nc_out_runmax, options='-f nc', force=False, returnCdf=False)

    # calculate required percentile in ref period
    cdo.ydrunpctl(index['percentile'], windowDays, "rm="+readMethod, "pm="+percentileMethod,
                  input=selyear+nc_in + " " + nc_out_runmin + " " + nc_out_runmax, output=nc_out_th,
                  options='-f nc', force=False, returnCdf=False)

    # calculate index
    index_cdo_function(6, "freq=year", input=nc_in + " " + nc_out_th, output=nc_out_index, options='-f nc', force=False, returnCdf=False)

    debug(clean((nc_out_index)))
    print("")


def normal_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    Calculate "normal" indices, that generate a matrix out, without needing any additional input parameters
    '''
    from indices_misc import logger, clean
    import pathlib

    index_cdo_function = getattr(cdo, index['cdo_fun'])  # get the cdo function coressponding to the input index
    nc_out_normal = (out_dir + '/' + pathlib.Path(nc_in).stem + "_"+index['name']+".nc")

    add_params = ''
    add_command = ''
    if 'add_params' in index:
        add_params = index['add_params']
    if 'add_command' in index:
        add_command = index['add_command']

    logger.debug(clean((nc_out_normal)))
    index_cdo_function(add_params, input=add_command+nc_in, output=nc_out_normal, options='-f nc', force=False, returnCdf=False)


def delete_days(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    Delete wrongly generated days in rx5day index monthly
    '''
    from indices_misc import logger, clean
    from useful_functions import get_subfiles
    import pathlib
    from os import rename

    for file, file_path in get_subfiles(out_dir):
        if file.startswith("._"):
            continue  # does nothing
        elif file.endswith(index['name']+".nc"):  # if file ends with index.nc, it is the pure index file

            nc_out_days = out_dir + "/" + pathlib.Path(file_path).stem + "_withDays.nc"
            rename(file_path, nc_out_days)

            logger.debug(clean((file_path)))
            cdo.delete("day=17", input="-delete,month=6,hour=12 "+nc_out_days, output=file_path, options='-f nc', force=False, returnCdf=False)


def manual_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    Calculate indices manually
    '''

    from indices_misc import logger, clean
    import pathlib

    if nc_in2 is not None:  # index with two parameters
        nc_in += " "+nc_in2

    nc_out = (out_dir + '/' + pathlib.Path(nc_in).stem + "_"+index['name']+".nc")

    logger.debug(clean((nc_out)))
    cdo.chname(index['param'][0]+","+index['cdo_name'],  # change aprameter name
               input="-setattribute,"+index['param'][0]+"@long_name="+index['long_name']  # change parameter long name
               + index['cdo_fun'] + nc_in,  # the actual command
               output=nc_out, options='-f nc', force=False, returnCdf=False)


def gsl_index(cdo, index, out_dir, nc_in, nc_in2=None):
    '''
    For gsl index, which requires some special calculation
    '''
    from indices_misc import debug, clean
    import pathlib

    tasmin = nc_in
    tasmax = nc_in2

    nc_out_gsl = (out_dir + '/' + pathlib.Path(nc_in).stem + "_"+index['name']+".nc")

    debug(clean(nc_out_gsl))

    # For some reason, the etccdi operator gives error:  etccdi_gsl (Abort): Operator not callable by this name! Name is: etccdi_gsl
    # cdo.etccdi_gsl(input="-divc,2 -add " + tasmin + " " + tasmax + " -gtc,1 " + tasmax, output=nc_out_gsl, force=False, returnCdf=False)

    # use eca. Eca needs as second input a landmask. As the regions we are using are already in land, just produce a file with all 1s.
    cdo.eca_gsl(input="-divc,2 -add " + tasmin + " " + tasmax + " -addc,1 -mulc,0 -setmisstoc,1 -seltimestep,1 " + tasmax, output=nc_out_gsl, force=False, returnCdf=False)


def generate_periods(cdo, index, out_dir, nc_in=None, nc_in2=None):
    '''
    Generate a map of the index, for the required time periods, starting from matrix
    '''

    from indices_misc import logger, clean
    from indices_misc import period_range_array, period_name_array
    from useful_functions import get_subfiles
    import pathlib

    for season in index['seasons']:
        for year_range, name in zip(period_range_array, period_name_array):
            cdo_year_command = "-selyear,"+year_range
            for file, file_path in get_subfiles(out_dir):
                if file.startswith("._"):
                    continue  # does nothing
                elif file.endswith(index['name']+".nc"):  # if file ends with index.nc, it is the pure idex file, with matrix values (temp and field)
                    pathlib.Path(out_dir + "/" + season + "/").mkdir(parents=True, exist_ok=True)
                    nc_out = out_dir + "/" + season + "/" + pathlib.Path(file_path).stem + "_" + name + ".nc"
                    logger.debug(clean((nc_out)))
                    logger.debug(clean(("")))
                    cdo.timmean(input="-setreftime,1850-01-01,00:00:00 "+cdo_year_command + " " + file_path, output=nc_out, options='-f nc', force=False, returnCdf=False)


def generate_ts(cdo, index, out_dir, nc_in=None, nc_in2=None):
    '''
    Generate timeseries of the index, for the whole area, starting from matrix
    '''

    from indices_misc import logger, clean
    from useful_functions import get_subfiles
    import pathlib

    for file, file_path in get_subfiles(out_dir):
        if file.startswith("._"):
            continue  # does nothing
        elif file.endswith(index['name']+".nc"):  # if file ends with index.nc, it is the pure idex file, with matrix values (temp and field)
            nc_out = out_dir + "/" + pathlib.Path(file_path).stem + "_ts.nc"
            logger.debug(clean((nc_out)))
            logger.debug(clean(("")))
            cdo.fldmean(input="-setreftime,1850-01-01,00:00:00 "+file_path, output=nc_out, options='-f nc', force=False, returnCdf=False)

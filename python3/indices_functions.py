import logging
from cdo import *


def selyear_index(cdo, index_in, param_in, nc_in=None, out_dir_in=None, first_year_in=None):
    '''
    For indexes that need a selyear to generate a timeseries, like sdii
    '''
    import shutil
    import os.path
    import pathlib

    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        logger.debug("Error, output dir is was not specified")
        return -1

    # if a first year is given, start from there, otherwise, start from the first year on the file name
    first_year_file = ((nc_in.split("_"))[-2].split("-")[0])[0:4]
    first_year = first_year_in
    if first_year is None:
        first_year = first_year_file

    last_year = ((nc_in.split("_"))[-2].split("-")[1])[0:4]
    nc_out_array = ""
    if first_year_file != "1861" or last_year != "2090":
        logger.debug("Error in first or last year "+first_year_file+"-"+last_year)
        return

    nc_out_fldmean = (out_dir_in + '/' + pathlib.Path(nc_in).stem + "_" + index_in + "_ts.nc").replace(first_year_file, first_year)
    # Create nc files for field mean and year mean.
    if os.path.exists(nc_out_fldmean):  # False:
        logger.debug("%s already exists", nc_out_fldmean)
        return

    pathlib.Path(out_dir_in + '/years/').mkdir(parents=True, exist_ok=True)

    for year in range(int(first_year), int(last_year)+1):
        cdo_selyear_command = "-selyear,"+str(year)
        nc_out = out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_" + index_in + str(year)+".nc"
        # try:
        logger.debug(nc_out)
        # force to False so if the file already exists is not overwritten
        index_cdo_function(input=cdo_selyear_command+" "+nc_in,
                           output=nc_out, options='-f nc', force=False, returnCdf=False)
        nc_out_array = nc_out_array+" "+nc_out
        # except CDOException:
        #    logger.debug("CDO Exception")
    # try:
    nc_out_merge = (out_dir_in + '/years/' + pathlib.Path(nc_in).stem + "_" + index_in + ".nc").replace(first_year_file, first_year)  # adapt the name to the actual first year used
    cdo.mergetime(input=nc_out_array, output=nc_out_merge, options='-f nc', force=False, returnCdf=False)
    cdo.fldmean(input="-setreftime,1850-01-01,00:00:00 "+nc_out_merge, output=nc_out_fldmean, options="-f nc", force=False, returnCdf=False)

    logger.debug("")
    logger.debug(nc_out_fldmean)
    logger.debug("")
    try:
        shutil.rmtree(out_dir_in + '/years/')
    except OSError as e:
        logger.debug("Error: %s" % (e.strerror))

    except CDOException:
        logger.debug("CDO Exception")


def direct_periods_index(cdo, index_in, param_in, nc_in=None, out_dir_in=None):
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

    index_cdo_function = getattr(cdo, "etccdi_"+index_in)  # get the cdo function coressponding to the input index

    if index_cdo_function is None:
        logger.debug("Error, not an index from etccdi")
        return -1

    if out_dir_in is None:
        logger.debug("Error, output dir  was not specified")
        return -1
    if nc_in is None:
        logger.debug("Error, nc_in was not specified")
        return -1

    for season in seasons:
        pathlib.Path(out_dir_in + '/' + season).mkdir(parents=True, exist_ok=True)
        cdo_season_command = sel_season+season
        for year_range, name in zip(year_range_array, period_name_array):
            cdo_year_command = sel_year_range+year_range
            nc_out = out_dir_in + "/" + season + "/" + pathlib.Path(nc_in).stem + "_" + index_in + "_" + name + ".nc"

            logger.debug(nc_out)
            try:
                # force to False so if the file already exists is not overwritten
                index_cdo_function(input=cdo_year_command+" "+cdo_season_command+" "+nc_in,
                                   output=nc_out, options='-f nc', force=False, returnCdf=False)
            except CDOException:
                logger.debug("CDO error")  # lik


logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

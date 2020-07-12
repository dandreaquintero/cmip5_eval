import logging


def clean(message=None):
    if message is None:
        return
    return message.replace('/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/', '').replace('indices/', '')


# Logger functionality format
logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
debug = logger.debug


# Here you should define the paths where the historical+rcp files are stored, for each parameter #
rcp_paths = {
    'rcp45': {
        'pr': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp45_pr_daily_converted',
        'tasmin': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp45_tasmax_tasmin_daily_converted',
        'tasmax': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp45_tasmax_tasmin_daily_converted'
    },

    'rcp85': {
        'pr': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp85_pr_daily_converted',
        'tasmin': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp85_tasmax_tasmin_daily_converted',
        'tasmax': '/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/histo_rcp85_tasmax_tasmin_daily_converted'
    }
}
# Path to store the output
indices_output_dir = "/Users/danielaquintero/Documents/tesis/cmip5_eval/nc_files/indices/"
indices_graphs_out_dir = "/Users/danielaquintero/Documents/tesis/tesis_latex/gfx/indices/"


# Define the periods for which the maps will be calculated an their names in the output files.
# reference should go first, to calculate the subs
period_range_array = ["1961/1990",           "1861/1890",      "1991/2020",         "2061/2090"]           # cdo command format
period_name_array = ["reference_1961-1990",  "past_1861-1890", "present_1991-2020", "future_2061-2090"]    # filenames
period_title_array = ["1961 - 1990",         "1861 - 1890",    "1991 - 2020",       "2061 - 2090"]         # maps title

# Boxes for plotmap
boxDict = {
    "Andes":  [282, 289, 0, 9.5],  # long1, long2, lat1, lat2
    "Alpine": [5.5, 15, 44, 47.5]
}

figsize = {
    "Andes": (4, 5.7),
    "Alpine": (4, 4.5)
}

paral = {
    "Andes": [0.5, 9],
    "Alpine": [43.8, 48.6]
}

merid = {
    "Andes": [282.5, 288.8],
    "Alpine": [5, 15]
}

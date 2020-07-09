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

# # Colors for indices
# color_zero = ['snow', 'snow']
# prec_colors_neg = ['snow', 'papayawhip', 'lightsalmon', 'lightcoral', 'salmon', 'tomato', 'orangered', 'red', 'darkred']
# prec_colors_pos = ['snow', 'lightcyan', 'lightskyblue', 'paleturquoise', 'turquoise', 'lightseagreen', 'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue',
#                    'midnightblue', 'indigo']
#
# temp_colors_neg = ['snow', 'paleturquoise', 'lightskyblue', 'skyblue', 'turquoise', 'deepskyblue', 'dodgerblue', 'blue', 'mediumblue']  # 'darkblue', 'midnightblue']
# temp_colors_pos = ['snow', 'yellow', 'gold', 'orange', 'darkorange', 'coral', 'tomato', 'red', 'darkred']

# bounds = [-30, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300]                     # for r95p
# bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]                         # for tx90p
# bounds = [-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]        # for tx90p RCP85
# bounds = [-60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10]              # FD
# bounds = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]                       # R20mm
# bounds = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]                       # CDD
# bounds = [-30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90]                         # for SU

# # bounds and colors for indices
# # bounds = [-0.8,           -0.7,         -0.6,       -0.5,      -0.4,   # 18 for sdii
# #           -0.3,           -0.2,         -0.1,          0,       0.1,
# #           0.2,             0.3,          0.4,        0.5,       0.6,
# #           0.7,             0.8,            1]
#
# colors = ['navy', 'blue', 'mediumblue', 'dodgerblue', 'deepskyblue', 'lightskyblue',                           # for tx90p  RCP45
#           'lightblue', 'moccasin', 'yellow', 'gold', 'orange', 'darkorange',
#           'coral', 'tomato', 'red', 'darkred']
#
# colors = ['mediumturquoise', 'paleturquoise', 'lightcyan', 'snow', 'lemonchiffon', 'yellow', 'gold', 'orange',   # FOR TX90P RCP85
#           'darkorange', 'lightcoral', 'coral', 'tomato', 'orangered', 'red', 'firebrick', 'crimson', 'darkviolet', 'purple', 'indigo']
#
# colors = ['darkred', 'firebrick', 'red', 'orangered', 'tomato', 'salmon', 'coral', 'darkorange', 'orange', 'gold', 'yellow', 'lemonchiffon', 'snow',  # FD
#           'paleturquoise', 'mediumturquoise', 'turquoise']
#
# colors = ['orangered', 'tomato', 'salmon', 'lightcoral',                                                        # for r20mm
#           'lightsalmon', 'snow', 'paleturquoise', 'lightskyblue', 'skyblue', 'turquoise',
#           'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue', 'midnightblue']
#
# colors = ['red', 'orangered', 'tomato', 'salmon', 'lightcoral', 'snow', 'lightskyblue', 'turquoise',             #CDD
#           'deepskyblue', 'dodgerblue', 'blue', 'mediumblue', 'darkblue', 'midnightblue']
#
# colors = ['mediumblue', 'deepskyblue', 'lightskyblue', 'snow', 'moccasin', 'yellow', 'gold', 'orange', 'darkorange',
#           'coral', 'salmon', 'tomato', 'red', 'darkred']

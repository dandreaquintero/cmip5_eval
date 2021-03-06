# this file contains the possible indices and their information
# the key is the standard index name (as in etccdi)

from indices_loop_functions import selyear_index, direct_periods_index, percentile_index, duration_percentile_index, normal_index, delete_days, manual_index
from indices_loop_functions import gsl_index, generate_periods, generate_ts
from indices_merge_functions import merge_periods, merge_ts

indices = {

    'fd': {
        'name': 'fd',
        'cdo_name': 'fdETCCDI',
        'description': '1. number of frost days: annual count of days when tn (daily minimum temperature) < 0oc.',
        'short_desc': 'Frost Days (FD)',
        'param': ['tasmin'],

        'cdo_fun': 'etccdi_fd',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'setrtomiss': ' -setrtomiss,-50,1 ',
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_neg',
        'units': 'Days',
        'ignore': ['Andes'],
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'endn',
        'legend': 'lower left',

        'glob_rcp45': -9,
        'glob_rcp85': -20,
        'glob_avg6190': 61,
    },



    'su': {
        'name': 'su',
        'cdo_name': 'suETCCDI',
        'description': '2. number of summer days: annual count of days when tx (daily maximum temperature) > 25oc.',
        'short_desc': 'Summer Days (SU)',
        'param': ['tasmax'],

        'cdo_fun': 'etccdi_su',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'setrtomiss': ' -setrtomiss,-50,1 ',
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 30,
        'glob_rcp85': 50,
        'glob_avg6190': 117,
    },



    'id': {
        'name': 'id',
        'cdo_name': 'idETCCDI',
        'description': '3. number of icing days: annual count of days when tx (daily maximum temperature) < 0oc.',
        'short_desc': 'Icing Days (ID)',
        'param': ['tasmax'],

        'cdo_fun': 'etccdi_id',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'setrtomiss': ' -setrtomiss,-50,1 ',
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_neg',
        'units': 'Days',
        'ignore': ['Andes'],
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'endn',

        'glob_rcp45': -7.8,
        'glob_rcp85': -14,
        'glob_avg6190': 47,
    },



    'tr': {
        'name': 'tr',
        'cdo_name': 'trETCCDI',
        'description': '4. number of tropical nights: annual count of days when tn (daily minimum temperature) > 20oc.',
        'short_desc': 'Tropical Nigths (TR)',
        'param': ['tasmin'],

        'cdo_fun': 'etccdi_tr',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'setrtomiss': ' -setrtomiss,-50,1 ',
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 21,
        'glob_rcp85': 40,
        'glob_avg6190': 150,
    },



    'gsl': {
        'name': 'gsl',
        'cdo_name': 'thermal_growing_season_length',
        'description': '5. growing season length: annual (1st jan to 31st dec in northern hemisphere (nh), 1st july to 30th june in southern hemisphere (sh)) count'\
                       'between first span of at least 6 days with daily mean temperature tg>5oc and first span after july 1st (jan 1st in sh) of 6 days with tg<5oc.',
        'short_desc': 'Growing Season Length (GSL)',
        'param': ['tasmin', 'tasmax'],

        'ignore': ['Andes'],
        'seasons': ['ANN'],
        'loop_functions': [gsl_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 10.5,
        'glob_rcp85': 18,
        'glob_avg6190': 284,
    },



    'txx': {
        'name': 'txx',
        'cdo_name': 'txxETCCDI',
        'description': '6. monthly maximum value of daily maximum temperature.',
        'short_desc': 'Monthy Maximum of TX (TXx)',
        'param': ['tasmax'],

        'cdo_fun': '  -chunit,K,C -subc,273.15  -monmax ',
        'long_name': '\"Monthly maximum value of daily maximum temperature\"',
        'seasons': ['ANN'],
        'do_month': True,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',
    },
    'txxy': {
        'name': 'txxy',
        'cdo_name': 'txxyETCCDI',
        'description': '6. annual maximum value of daily maximum temperature.',
        'short_desc': 'Warmest Day in the year (TXx)',
        'param': ['tasmax'],

        'cdo_fun': '  -chunit,K,C -subc,273.15  -yearmax ',
        'long_name': '\"Annual maximum value of daily maximum temperature\"',
        'seasons': ['ANN'],
        'do_month': False,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',

        'glob_rcp45': 2,
        'glob_rcp85': 4.0,

        'limit_barplot': [0, 8.5]
    },



    'tnx': {
        'name': 'tnx',
        'cdo_name': 'tnxETCCDI',
        'description': '7. monthly maximum value of daily minimum temperature.',
        'short_desc': 'Monthly Maximum of TN (TNx)',
        'param': ['tasmin'],

        'cdo_fun': '  -chunit,K,C -subc,273.15  -monmax ',
        'long_name': '\"Monthly maximum value of daily minimum temperature\"',
        'seasons': ['ANN'],
        'do_month': True,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',
    },
    'tnxy': {
        'name': 'tnxy',
        'cdo_name': 'tnxyETCCDI',
        'description': '7. annual maximum value of daily minimum temperature.',
        'short_desc': 'Warmest Night in the year (TNx)',
        'param': ['tasmin'],

        'cdo_fun': '  -chunit,K,C -subc,273.15  -yearmax ',
        'long_name': '\"Annual maximum value of daily minimum temperature\"',
        'seasons': ['ANN'],
        'do_month': False,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',

        'glob_rcp45': 2,
        'glob_rcp85': 4.1,

        'limit_barplot': [0, 8.5]
    },



    'txn': {
        'name': 'txn',
        'cdo_name': 'txnETCCDI',
        'description': '8. monthly minimum value of daily maximum temperature.',
        'short_desc': 'Monthly Minimum of TX (TXn)',
        'param': ['tasmax'],

        'cdo_fun': ' -chunit,K,C -subc,273.15 -monmin ',
        'long_name': '\"Monthly minimum value of daily maximum temperature\"',
        'seasons': ['ANN'],
        'do_month': True,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',
    },
    'txny': {
        'name': 'txny',
        'cdo_name': 'txnyETCCDI',
        'description': '8. annual minimum value of daily maximum temperature.',
        'short_desc': 'Coldest Day in the year (TXn)',
        'param': ['tasmax'],

        'cdo_fun': ' -chunit,K,C -subc,273.15 -yearmin ',
        'long_name': '\"Annual minimum value of daily maximum temperature\"',
        'seasons': ['ANN'],
        'do_month': False,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',

        'glob_rcp45': 2.5,
        'glob_rcp85': 5.0,

        'limit_barplot': [0, 8.5]
    },



    'tnn': {
        'name': 'tnn',
        'cdo_name': 'tnnETCCDI',
        'description': '9.  monthly minimum value of daily minimum temperature.',
        'short_desc': 'Monthly Minumum of TN (TNn)',
        'param': ['tasmin'],

        'cdo_fun': ' -chunit,K,C -subc,273.15 -monmin ',
        'long_name': '\"Monthly minimum value of daily minimum temperature\"',
        'seasons': ['ANN'],
        'do_month': True,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',
    },
    'tnny': {
        'name': 'tnny',
        'cdo_name': 'tnnyETCCDI',
        'description': '9.  annual minimum value of daily minimum temperature.',
        'short_desc': 'Coldest Night in the year (TNn)',
        'param': ['tasmin'],

        'cdo_fun': ' -chunit,K,C -subc,273.15 -yearmin ',
        'long_name': '\"Annual minimum value of daily minimum temperature\"',
        'seasons': ['ANN'],
        'do_month': False,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'min_perc_rel': 1,
        'max_perc_rel': 99,
        'datatip': 'end',

        'glob_rcp45': 2.8,
        'glob_rcp85': 5.5,

        'limit_barplot': [0, 8.5]
    },



    'tn10p': {
        'name': 'tn10p',
        'cdo_name': 'tn10pETCCDI',
        'description': '10. percentage of days when tn < 10th percentile.',
        'short_desc': 'Cold Nights (TN10p)',
        'param': ['tasmin'],

        'cdo_fun': 'etccdi_tn10p',
        'seasons': ['ANN'],
        'isTemp': True,
        'loop_functions': [percentile_index, generate_periods, generate_ts],

        'do_anom': False,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 10,
        'colorbar': 'temp_neg',
        'units': 'Exceedance Rate [%]',
        'limits': [0, 50],
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',

        'glob_rcp45': 1.0,
        'glob_rcp85': 0.1,
    },



    'tx10p': {
        'name': 'tx10p',
        'cdo_name': 'tx10pETCCDI',
        'description': '11. percentage of days when tx < 10th percentile.',
        'short_desc': 'Cold Days (TX10p)',
        'param': ['tasmax'],

        'cdo_fun': 'etccdi_tx10p',
        'seasons': ['ANN'],
        'isTemp': True,
        'loop_functions': [percentile_index, generate_periods, generate_ts],

        'do_anom': False,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 10,
        'colorbar': 'temp_neg',
        'units': 'Exceedance Rate [%]',
        'limits': [0, 50],
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',

        'glob_rcp45': 1.25,
        'glob_rcp85': 0.5,
    },



    'tn90p': {
        'name': 'tn90p',
        'cdo_name': 'tn90pETCCDI',
        'description': '12. percentage of days when tn > 90th percentile.',
        'short_desc': 'Warm Nights (TN90p)',
        'param': ['tasmin'],

        'cdo_fun': 'etccdi_tn90p',
        'seasons': ['ANN'],
        'isTemp': True,
        'loop_functions': [percentile_index, generate_periods, generate_ts],

        'do_anom': False,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 10,
        'colorbar': 'temp_pos',
        'units': 'Exceedance Rate [%]',
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',

        'glob_rcp45': 49,
        'glob_rcp85': 69,

        'limit_barplot': [10, 100]
    },



    'tx90p': {
        'name': 'tx90p',
        'cdo_name': 'tx90pETCCDI',
        'description': '13. percentage of days when tx > 90th percentile.',
        'short_desc': 'Warm Days (TX90p)',
        'param': ['tasmax'],

        'cdo_fun': 'etccdi_tx90p',
        'seasons': ['ANN'],
        'isTemp': True,
        'loop_functions': [percentile_index, generate_periods, generate_ts],

        'do_anom': False,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 10,
        'colorbar': 'temp_pos',
        'units': 'Exceedance Rate [%]',
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',

        'glob_rcp45': 47,
        'glob_rcp85': 67,

        'limit_barplot': [10, 100]
    },



    'wsdi': {
        'name': 'wsdi',
        'cdo_name': 'wsdiETCCDI',
        'description': '14. warm spell duration index: annual count of days with at least 6 consecutive days when tx > 90th percentile.',
        'short_desc': 'Warm Spell Duration (WSDI)',
        'param': ['tasmax'],

        'cdo_fun': 'etccdi_wsdi',
        'seasons': ['ANN'],
        'percentile': '90',
        'loop_functions': [duration_percentile_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 158,
        'glob_rcp85': 250,
        'glob_avg6190': 8,
    },
    'wsdieca': {
        'name': 'wsdieca',
        'cdo_name': 'warm_spell_days_index_wrt_90th_percentile_of_reference_period',
        'description': '14. warm spell duration index: annual count of days with at least 6 consecutive days when tx > 90th percentile.',
        'short_desc': 'Warm Spell Duration (WSDI)',
        'param': ['tasmax'],

        'cdo_fun': 'eca_hwfi',
        'seasons': ['ANN'],
        'percentile': '90',
        'ignore': [['HadGEM2-ES', 'rcp45'], ['HadGEM2-ES', 'rcp85'], ['HadGEM2-CC', 'rcp45'], ['HadGEM2-CC', 'rcp85'], ['HadGEM2-AO', 'rcp45'], ['HadGEM2-AO', 'rcp85']],
        'loop_functions': [duration_percentile_index, generate_periods],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 158,
        'glob_rcp85': 250,
        'glob_avg6190': 8,
    },



    'csdi': {
        'name': 'csdi',
        'cdo_name': 'csdiETCCDI',
        'description': '15. cold spell duration index: annual count of days with at least 6 consecutive days when tn < 10th percentile.',
        'short_desc': 'Cold Spell Duration (CSDI)',
        'param': ['tasmin'],

        'cdo_fun': 'etccdi_csdi',
        'seasons': ['ANN'],
        'percentile': '10',
        'loop_functions': [duration_percentile_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_neg',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'endn',

        'glob_rcp45': -7,
        'glob_rcp85': -7,
        'glob_avg6190': 7,
    },
    'csdieca': {
        'name': 'csdieca',
        'cdo_name': 'cold_spell_days_index_wrt_10th_percentile_of_reference_period',
        'description': '15. cold spell duration index: annual count of days with at least 6 consecutive days when tn < 10th percentile.',
        'short_desc': 'Cold Spell Duration (CSDI)',
        'param': ['tasmin'],

        'cdo_fun': 'eca_cwfi',
        'seasons': ['ANN'],
        'percentile': '10',
        'ignore': [['HadGEM2-ES', 'rcp45'], ['HadGEM2-ES', 'rcp85'], ['HadGEM2-CC', 'rcp45'], ['HadGEM2-CC', 'rcp85'], ['HadGEM2-AO', 'rcp45'], ['HadGEM2-AO', 'rcp85']],
        'loop_functions': [duration_percentile_index, generate_periods],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'temp_neg',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'endn',

        'glob_rcp45': -7,
        'glob_rcp85': -7,
        'glob_avg6190': 7,
    },

    'dtr': {
        'name': 'dtr',
        'cdo_name': 'dtrETCCDI',
        'description': '16. daily temperature range: monthly mean difference between tx and tn.',
        'short_desc': 'Daily Temperature Range (DTR)',
        'param': ['tasmax', 'tasmin'],

        'cdo_fun': ' -chunit,K,C -monmean -sub  ',
        'long_name': '\"Monthly mean difference between Tx and Tn.\"',
        'seasons': ['ANN'],
        'do_month': True,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',
    },
    'dtry': {
        'name': 'dtry',
        'cdo_name': 'dtryETCCDI',
        'description': '16. daily temperature range: annual mean difference between tx and tn.',
        'short_desc': 'Daily Temperature Range (DTR)',
        'param': ['tasmax', 'tasmin'],

        'cdo_fun': ' -chunit,K,C -yearmean -sub  ',
        'long_name': '\"Annual mean difference between Tx and Tn.\"',
        'seasons': ['ANN'],
        'do_month': False,
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': False,
        'hline': 0,
        'colorbar': 'temp_pos',
        'units': 'Temperature [°C]',
        'min_perc': 1,
        'max_perc': 99,
        'datatip': 'end',
        'glob_rcp45': -0.09,
        'glob_rcp85': -0.18,
    },


    'rx1day': {
        'name': 'rx1day',
        'cdo_name': 'rx1dayETCCDI',
        'description': '17. monthly maximum 1-day precipitation.',
        'short_desc': 'Max. 1-day Precipitation (RX5day)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_rx1day',
        'add_params': '50,freq=month',
        'do_month': True,
        'seasons': ['ANN'],
        'loop_functions': [normal_index, delete_days, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

    },
    'rx1dayy': {
        'name': 'rx1dayy',
        'cdo_name': 'rx1dayETCCDI',
        'description': '17. annual maximum 1-day precipitation.',
        'short_desc': 'Max. 1-day Precipitation (RX1day)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_rx1day',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 4.2,
        'glob_rcp85': 9.2,
        'glob_avg6190': 40.5,

        'limit_barplot': [-5, 45]
    },



    'rx5day': {
        'name': 'rx5day',
        'cdo_name': 'rx5dayETCCDI',
        'description': '18. monthly maximum consecutive 5-day precipitation.',
        'short_desc': 'Max. 5-day Precipitation (RX5day)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_rx5day',
        'add_command': '-runsum,5 ',
        'add_params': '50,freq=month',
        'do_month': True,
        'seasons': ['ANN'],
        'loop_functions': [normal_index, delete_days, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',
    },
    'rx5dayy': {
        'name': 'rx5dayy',
        'cdo_name': 'rx5dayETCCDI',
        'description': '18. annual maximum consecutive 5-day precipitation.',
        'short_desc': 'Max. 5-day Precipitation (RX5day)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_rx5day',
        'add_command': '-runsum,5 ',
        'do_month': False,
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 7.7,
        'glob_rcp85': 15,
        'glob_avg6190': 91.5,

        'limit_barplot': [-5, 45]
    },




    'sdii': {
        'name': 'sdii',
        'cdo_name': 'sdiiETCCDI',
        'description': '19. simple pricipitation intensity index.',
        'short_desc': 'Simple Daily Intensity (SDII)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_sdii',
        'seasons': ['ANN', 'DJF', 'JJA', 'AM'],
        'loop_functions': [selyear_index, direct_periods_index],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation Intensity [mm/day]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 0.33,
        'glob_rcp85': 0.62,
        'glob_avg6190': 6.17,

        'limit_barplot': [-13, 20]
    },



    'r10mm': {
        'name': 'r10mm',
        'cdo_name': 'r10mmETCCDI',
        'description': '20. annual count of days when prcp≥ 10mm.',
        'short_desc': 'Heavy Precipitation Days (R10mm)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_r10mm',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'ignore': [['BCC-CSM1.1', 'rcp45']],
        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 1.5,
        'glob_rcp85': 2.5,
        'glob_avg6190': 29.25,

        'limit_barplot': [-12, 60],
        'legendb': 'upper left',
        'titlepad': 10
    },



    'r20mm': {
        'name': 'r20mm',
        'cdo_name': 'r20mmETCCDI',
        'description': '21. annual count of days when prcp≥ 20mm.',
        'short_desc': 'Very Heavy Precipitation Days (R20mm)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_r20mm',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'ignore': [['BCC-CSM1.1', 'rcp45'], ['GISS-E2-H', 'rcp85']],
        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 0.95,
        'glob_rcp85': 1.6,
        'glob_avg6190': 8.8,

        'limit_barplot': [-12, 60],
        'legendb': 'upper left',
        'titlepad': 10
    },



    'r30mm': {
        'name': 'r30mm',
        'cdo_name': 'precipitation_days_index_per_time_period',
        'description': '22. annual count of days when prcp≥ nnmm, nn is a user defined threshold = 30',
        'short_desc': 'Extremely Heavy Precipitation Days (R30mm)',
        'param': ['pr'],

        'cdo_fun': 'eca_pd',
        'add_params': '30',
        'add_fun': 'divc',  # the output is not normalized per year
        'add_fun_params': '30',  # to nomralize, divide by the number of years (30)
        'seasons': ['ANN'],
        'ignore': [['BCC-CSM1.1', 'rcp45']],
        'loop_functions': [selyear_index, direct_periods_index],  # div_timeperiod],

        'do_anom': True,
        'setrtomiss': ' -setrtomiss,-50,1 ',
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',
    },



    'r1mm': {
        'name': 'r1mm',
        'cdo_name': 'r1mmETCCDI',
        'description': '22. annual count of days when prcp≥ nnmm, nn is a user defined threshold = 1mm',
        'short_desc': 'Wet Days (R1mm)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_r1mm',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': -0.5,
        'glob_rcp85': -2.4,
        'glob_avg6190': 149.5,
    },



    'cdd': {
        'name': 'cdd',
        'cdo_name': 'cddETCCDI',
        'description': '23. maximum length of dry spell, maximum number of consecutive days with rr < 1mm.',
        'short_desc': 'Consecutive Dry Days (CDD)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_cdd',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_neg',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 1.25,
        'glob_rcp85': 3.3,
        'glob_avg6190': 46,

        'limit_barplot': [-30, 50],
        'legendb': 'upper left',
        'titlepad': 10
    },



    'cwd': {
        'name': 'cwd',
        'cdo_name': 'cwdETCCDI',
        'description': '24. maximum length of wet spell, maximum number of consecutive days with rr ≥ 1mm.',
        'short_desc': 'Consecutive Wet Days (CWD)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_cwd',
        'seasons': ['ANN'],
        'loop_functions': [normal_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Days',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 0.28,
        'glob_rcp85': 0.15,
        'glob_avg6190': 20.64,

        'limit_barplot': [-30, 50],
        'legendb': 'upper left',
        'titlepad': 10
    },



    'r95p': {
        'name': "r95p",
        'cdo_name': 'r95pETCCDI',
        'description': '25.  annual total prcp when rr > 95p.',
        'short_desc': 'Precipitation from Very Wet Days (R95p)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_r95p',
        'seasons': ['ANN'],
        'isTemp': False,
        'loop_functions': [percentile_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 50,
        'glob_rcp85': 100,
        'glob_avg6190': 219,

        'limit_barplot': [-5, 148]
    },



    'r99p': {
        'name': "r99p",
        'cdo_name': 'r99pETCCDI',
        'description': '26. annual total prcp when rr > 99p.',
        'short_desc': 'Precipitation from Extremely Wet Days (R99p)',
        'param': ['pr'],

        'cdo_fun': 'etccdi_r99p',
        'seasons': ['ANN'],
        'isTemp': False,
        'loop_functions': [percentile_index, generate_periods, generate_ts],


        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 29,
        'glob_rcp85': 65,
        'glob_avg6190': 67,

        'limit_barplot': [-5, 148]
    },



    'prcptot': {
        'name': 'prcptot',
        'cdo_name': 'prcptotETCCDI',
        'description': '27. annual total precipitation in wet days.',
        'short_desc': ' Total Precipitation in Wet Days (PRCPTOT)',
        'param': ['pr'],

        'cdo_fun': ' -yearsum -setrtomiss,-50,1 ',
        'long_name': '\"Annual total precipitation in wet days\"',
        'seasons': ['ANN'],
        'ignore': [['BCC-CSM1.1', 'rcp45']],
        'loop_functions': [manual_index, generate_periods, generate_ts],

        'do_anom': True,
        'merge_functions': [merge_periods, merge_ts],

        'do_rel': True,
        'hline': 0,
        'colorbar': 'prec_pos',
        'units': 'Precipitation [mm/yr]',
        'min_perc': 15,
        'max_perc': 85,
        'min_perc_rel': 25,
        'max_perc_rel': 75,
        'datatip': 'end',

        'glob_rcp45': 42,
        'glob_rcp85': 75,
        'glob_avg6190': 1012,

        'limit_barplot': [-13, 20]
    }
}

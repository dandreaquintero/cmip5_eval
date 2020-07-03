# This file contains the possible indices and their information
# The key is the standard index name (as in etccdi)

from indices_functions import selyear_index, direct_periods_index

indices = {

    'FD': {
        'description': '1. Number of frost days: Annual count of days when TN (daily minimum temperature) < 0oC.',
        'param': ['tasmin'],
    },

    'SU': {
        'description': '2. Number of summer days: Annual count of days when TX (daily maximum temperature) > 25oC.',
        'param': ['tasmax'],
    },

    'ID': {
        'description': '3. Number of icing days: Annual count of days when TX (daily maximum temperature) < 0oC.',
        'param': ['tasmax'],
    },

    'TR': {
        'description': '4. Number of tropical nights: Annual count of days when TN (daily minimum temperature) > 20oC.',
        'param': ['tasmin'],
    },

    'GSL': {
        'description': '5. Growing season length: Annual (1st Jan to 31st Dec in Northern Hemisphere (NH), 1st July to 30th June in Southern Hemisphere (SH)) count'\
                       'between first span of at least 6 days with daily mean temperature TG>5oC and first span after July 1st (Jan 1st in SH) of 6 days with TG<5oC.',
        'param': ['tasmin', 'tasmax'],
    },

    'TXx': {
        'description': '6. Monthly maximum value of daily maximum temperature.',
        'param': ['tasmax'],
    },

    'TNx': {
        'description': '7. Monthly maximum value of daily minimum temperature.',
        'param': ['tasmin'],
    },

    'TXn': {
        'description': '8. Monthly minimum value of daily maximum temperature.',
        'param': ['tasmax'],
    },

    'TNn': {
        'description': '9.  Monthly minimum value of daily minimum temperature.',
        'param': ['tasmin'],
    },

    'TN10p': {
        'description': '10. Percentage of days when TN < 10th percentile.',
        'param': ['tasmin'],
    },

    'TX10p': {
        'description': '11. Percentage of days when TX < 10th percentile.',
        'param': ['tasmax'],
    },

    'TN90p': {
        'description': '12. Percentage of days when TN > 90th percentile.',
        'param': ['tasmin'],
    },

    'TX90p': {
        'description': '13. Percentage of days when TX > 90th percentile.',
        'param': ['tasmax'],
    },

    'WSDI': {
        'description': '14. Warm speel duration index: Annual count of days with at least 6 consecutive days when TX > 90th percentile.',
        'param': ['tasmax'],
    },

    'CSDI': {
        'description': '15. Cold speel duration index: Annual count of days with at least 6 consecutive days when TN < 10th percentile.',
        'param': ['tasmin'],
    },

    'DTR': {
        'description': '16. Daily temperature range: Monthly mean difference between TX and TN.',
        'param': ['tasmin', 'tasmax'],
    },

    'Rx1day': {
        'description': '17. Monthly maximum 1-day precipitation.',
        'param': ['pr'],
    },

    'Rx5day': {
        'description': '18. Monthly maximum consecutive 5-day precipitation.',
        'param': ['pr'],
    },

    'SDII': {
        'description': '19. Simple pricipitation intensity index.',
        'param': ['pr'],
        'loop_functions': [selyear_index, direct_periods_index],
    },

    'R10mm': {
        'description': '20. Annual count of days when PRCP≥ 10mm.',
        'param': ['pr'],
    },

    'R20mm': {
        'description': '21. Annual count of days when PRCP≥ 20mm.',
        'param': ['pr'],
    },

    'Rnnmm': {
        'description': '22. Annual count of days when PRCP≥ nnmm, nn is a user defined threshold.',
        'param': ['pr'],
    },

    'CDD': {
        'description': '23. Maximum length of dry spell, maximum number of consecutive days with RR < 1mm.',
        'param': ['pr'],
    },

    'CWD': {
        'description': '24. Maximum length of wet spell, maximum number of consecutive days with RR ≥ 1mm.',
        'param': ['pr'],
    },

    'R95pTOT': {
        'description': '25.  Annual total PRCP when RR > 95p.',
        'param': ['pr'],
    },

    'R99pTOT': {
        'description': '26. Annual total PRCP when RR > 99p.',
        'param': ['pr'],
    },

    'PRCPTOT': {
        'description': '27. Annual total precipitation in wet days.',
        'param': ['pr'],
    }
}

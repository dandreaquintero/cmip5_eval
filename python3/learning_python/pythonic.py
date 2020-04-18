# from netCDF4 import Dataset, num2date
# import pandas as pd
# import matplotlib.pyplot as plt
# # from matplotlib.dates import DateFormatter, DayLocator
# from matplotlib.dates import DateFormatter, DayLocator, HourLocator
#
# # Read in some data
# data = Dataset('../model-gfs.nc', 'r')
# print(data.variables.keys())
#
# # Convert the array of time numbers to datetimes
# time_var = data['time']
# time = num2date(time_var[:], time_var.units).squeeze()  # squeeze is reshape the array and remove all sizes one dimensions

# # Time vs temperature_isobaric, wich was taken from 1000mb
# fig, ax = plt.subplots(1, 1, figsize=(12, 6))
# ax.plot(time, data.variables['Temperature_isobaric'][:].squeeze(), 'r-', linewidth=2)
# # add X/Y axis labels with a bigger font
# label_font = dict(size=16)
# ax.set_xlabel('Forest time (UTC)', fontdict=label_font)
# ax.set_ylabel('Temperature', fontdict=label_font)
#
# # Set the X-axis to do a major ticks on the days and label them like 'jul 20'
#
# ax.xaxis.set_major_locator(DayLocator())
# ax.xaxis.set_major_formatter(DateFormatter('%b %d'))  # %b: month and %d: day of the month
#
# # Set up minor ticks with the hours 6, 12, 18 written as '12Z'
# ax.xaxis.set_minor_locator(HourLocator(range(6, 24, 6)))  # 6, 12, 18 va cada 6h
# ax.xaxis.set_minor_formatter(DateFormatter('%HZ'))  # %H: hour (24-hour clock), put the hour value with a Z
#
# # Highlight the major x-axis grid lines with a thicker, dashed linestyle
# ax.grid(axis='x', linestyle='--', color='#666699', linewidth=1.0)
# ax.grid(which='minor', axis='x')
# ax.grid(axis='y')
# plt.show()
#
#
# # ###################### CONTAINER AND ITERATIONS ###########################
# # Python's built in lists and tuples facilitate easy ways of looping over groups of data.
# # One useful utility is zip, which iterates multiples lists at the same times
# # and goves tuples of the elements.
#
# vals = [1, 2, 3, 4]
# names = ['one', 'two', 'three', 'four']
# z = list(zip(names, vals))
# for v, name in zip(names, vals):
#     print(z)
#
# # Zip can also be used to unzip, using the ability of Python to pass a sequence
# # as a set of positional arguments
# list(zip(*z))   # [('one, 'two', 'three', 'four'), (1, 2, 3, 4)]
#
# # another useful part of the container is unpacking, which allows assingment
# # directly from a container
# one, two, three, four = vals
# print(three)
#
# # This same funcionality enables multiple return values from useful_functions
# import math
# def polar_to_cartesian(r, th):
#     x = r* math.cos(th)
#     y = r * math.sin(th)
#     return x, y
#
#
# X, Y = polar_to_cartesian(2, math.pi/3)
#
# # You can put those together and iterate over multiple lists, and unmpack items
# # into indivdual variables
# for n, v in zip(names, vals):
# print('%s == %d' % (n, v))

# LET'S ADD RELATIVE_HUMIDITY_ISOBARIC to our plot on a new subplot.
# but we need to do this in a loop without duplicating code. to do so we need:
# - a list of variables to plot
# - a ways to convert the variables from the file to an axis label_font
# - a list of plot formats.


# # This is just to keep the different cells in the notebook from rehashing This
# def set_defaults(ax):   # ax is the Parameters
#     # set the x-axis to do a major ticks on the days and label them like 'Jul 20'
#     from matplotlib.dates import DateFormatter, DayLocator, HourLocator
#     ax.xaxis.set_major_locator(DayLocator())
#     ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
#
#     # set up minor ticks with the hours 6, 12, 18 written as '18Z'
#     ax.xaxis.set_minor_locator(HourLocator(range(6, 24, 6)))  # 6, 12, 18 va cada 6h
#     ax.xaxis.set_minor_formatter(DateFormatter('%HZ'))  # %H: hour (24-hour clock), put the hour value with a Z
#
#     # Highlight the major x-axis grid lines with a thicker, dashed linestyle
#     ax.grid(axis='x', linestyle='--', color='#666699', linewidth=1.0)
#     ax.grid(which='minor', axis='x')
#     ax.grid(axis='y')
#     ax.set_xlabel('Forest time (UTC)', fontdict=dict(size=16))
#
#
# # This creates a figures and 2 subplots (axes is a lists axes objects)
# fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # 1 row and 2 columns

# What should we loop over?
# for var_name, ax in zip(['Temperature_isobaric', 'Relative_humidity_isobaric'], axes):   # create a list with a variable we want to plot
#     ax.plot(time, data.variables[var_name][:].squeeze())
#     set_defaults(ax)
#     ax.set_title(var_name)

# What should we loop over?
# variables = ['Temperature_isobaric', 'Relative_humidity_isobaric']
# linestyle = ['r-', 'g--']

# for var_name, ax, linestyle in zip(variables, axes, linestyle):  # create a list with a variable we want to plot
#     ax.plot(time, data.variables[var_name][:].squeeze(), linestyle)
#     set_defaults(ax)
#     ax.set_title(var_name)

# # What should we loop over?
# variables = ['Temperature_isobaric', 'Relative_humidity_isobaric']
# plot_styles = {'Temperature_isobaric': dict(color='red', linestyle='dashed', linewidth='2.0'),
#                'Relative_humidity_isobaric': dict(color='green')}
#
# for var_name, ax in zip(variables, axes):  # variables[:2] silice the first 2 variables, if there are more than 2 in the variables
#     style = plot_styles[var_name]
#     ax.plot(time, data.variables[var_name][:].squeeze(), **style)  # **style because is in a dictionary
#     set_defaults(ax)
#     ax.set_title(var_name)
#
#
# plt.show()

# ######################## DICTIONARIES #################################
# Powerful language feature that allow you to create arbitrary mappings btw two
# sets of things (key-> value). They can be used, certainly, but the give
# programmers they ability to create data structures on the fly.
# Of course, the values can themselves be dictionaries:

# states = dict(Colorado={'abbreviation': 'CO', 'capitol': 'Denver', 'notes': 'Home!'},
#               Oklahoma={'abbreviation': 'OK', 'capitol': 'Oklahoma City', 'flat': True},
#               Kansas={'abbreviation': 'KS', 'capitol': 'Topeka', 'flat': True})
# print(states['Oklahoma']['abbreviation'])

# ################### ARGS AND KWARGS #####################
# Within a function call, we can also set optional arguments and keyword
# arguments (abbreviated args and kwargs in Python). Args are used to pass a
# variable length list of non-keyword arguments. This means that args don't have
# a specific keyword they are attached to, and are used in the order provided.
# Kwargs are arguments that are attached to specific keywords, and therefore have
# a specific use within a function.

# Dentro de una llamada a la función, también podemos establecer argumentos
# opcionales y argumentos de palabras clave (args y kwargs abreviados en Python)
# Los args se utilizan para pasar una lista de longitud variable de argumentos
# que no son palabras clave. Esto significa que los args no tienen una palabra
# clave específica a la que se adjuntan, y se utilizan en el orden previsto.
# Los kwargs son argumentos que se adjuntan a palabras clave específicas, y por
# lo tanto tienen un uso específico dentro de una función.


# ##################################### METPY ##############################
# MetPy is a modern meteorological open-source toolkit for Python. It is a
# maintained project of Unidata to serve the academic meteorological community.
# MetPy consists of three major areas of functionality:
# - Plots
# - Calculations
# - File I/O

# ################## UPPER AIR DATA PLOTTING WITH METPY ##################
# set up PLOTTING
from IPython.display import display_data   # display figures
# Downloading: We're going to read text data from the University of Wyoming's upper air data archive
from datetime import datetime
from io import BytesIO, StringIO
from urllib.request import urlopen
# Open the remote URL as a file-like object
dt = datetime(1999, 5, 4, 0)
site = '72357'
url = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST'
       '&YEAR={0.year}&MONTH={0.month:02d}&FROM={0.day:02d}{0.hour:02d}'
       '&TO={0.day:02d}{0.hour:02d}&STNM={1}').format(dt, site)
fobj = urlopen(url)
data = fobj.read()

# Since the archive text format is embedded in HTML, look for the <PRE> tags
data_start = data.find(b'<PRE>')
data_end = data.find(b'</PRE>')

# Wrap the data in a file-like object
text = BytesIO(data[data_start:data_end])

# Now we use Numpy's text-file parsing utility ( usamos la utilidad de análisis de archivos de texto de Numpy):
import numpy as np
p, T, Td, direc, spd = np.genfromtxt(text, usecols=(0, 2, 3, 6, 7),  # I want those columns of data
                                     skip_header=6, unpack=True)  # I want to skip some of the header lines.

# add units to the data arrays
from metpy.units import units
p = p*units.mbar  # take the pressure and attack on millibar
T = T*units.degC  # dewpoint
Td = spd*units
direc = direc*units.deg

# # So what good do units do? (de qué sirven las unidades?):
# length = 8 * units.feet
# print(length * length)
#
# distance = 10 * units.mile
# time = 15 * units.minute
# avg_speed = distance / time
# print(avg_speed)
# print(avg_speed.to_base_units())  # put in the base units (m/s)
# print(avg_speed.to('mph'))        # put in mph

# # It also lets us avoid worrying about the exact units of arguments to
# # calculation functions:
# from metpy.calc import saturation_vapor_pressure
# e = saturation_vapor_pressure(Td)
# es = saturation_vapor_pressure(T)
# rh = e / es   # relative humidity
# print(e)   # in millibar
# print(es)  # in millibar
# print(rh)  # dimensionless

# Convert wind speed and direction to components
from metpy.calc import get_wind_components
u, v = get_wind_components(spd, direc)

################## PLOTTING ON A SKEW-T logP ######################
import matplotlib.pyplot as plt
from metpy.plots import SkewT

# create a new figure. The dimensions here gove a good aspect ratio
fig = plt.figure(figsize=(7, 9))
skew = SkewT(fig)              # passing the figure, use skewT

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')           # pressure and temperature in red
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)
skew.ax.set_ylim(1000, 100)    # Y limits from 1000 in the botton to 100 millibars to the top
skew.ax.set_xlim(-40, 60)      # X limits

# Add the relevant special lines\n",
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

plt.show()

# Calculate LCL height and plot as black dot\n",
from metpy.calc import lcl, dry_lapse
from metpy.units import units, concatenate
l = lcl(p[0], T[0], Td[0])     # we can calculate the lcl level from the starting p, T, Td
lcl_temp = dry_lapse(concatenate((p[0], l)), T[0])[-1].to('degC')  # Temperature of the lcl using the dry lapse
skew.plot(l, lcl_temp, 'ko', markerfacecolor='black') # plot the lcl level on the temperature with a black circle (ko) filled

# Calculate full parcel profile and add to plot as black line\n",
from metpy.calc import parcel_profile
prof = parcel_profile(p, T[0], Td[0]).to('degC')
skew.plot(p, prof, 'k', linewidth=2)

# Example of coloring area between profiles
skew.ax.fill_betweenx(p, T, prof, where=T>= prof, facecolor='blue', alpha=0.4)
skew.ax.fill_betweenx(p, T, prof, where=T< prof, facecolor='red', alpha=0.4)

# # An example of a slanted line at constant T -- in this case the 0 isotherm
level = skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)   # highligh the 0 degree isoterm

from metpy.plots import Hodograpgh
fig, ax = plt.subplot(1, 1)
hodo = Hodograph(ax)
hodo.plot(u,v)
hodo.add_grid()

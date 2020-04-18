from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
# def get_gridlines(ax, which):
#         '''
#         Parameters:
#             ax : ax.xaxis or ax.yaxis instance
#
#             which : 'major' or 'minor'
#         Returns:
#             The grid lines as a list of Line2D instance
#
#         '''
#
#         if which == 'major':
#             ticks = ax.get_major_ticks()
#         if which == 'minor':
#             ticks = ax.get_minor_ticks()
#
#         return cbook.silent_list('Line2D gridline',
#                                  [tick.gridline for tick in ticks])


r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r

ax = plt.subplot(111, projection='polar')
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

y_tick_labels = [-100, -10, 0, 10]
ax.set_yticklabels(y_tick_labels)
ind = y_tick_labels.index(0)  # find index of value 0

gridlines = ax.yaxis.get_gridlines()
gridlines[ind].set_color("k")
gridlines[ind].set_linewidth(2.5)

plt.show()

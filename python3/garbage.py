# # def bounds_colors(index, min, max):
# #
# #     from indices_misc import logger, prec_colors_pos, prec_colors_neg, temp_colors_pos, temp_colors_neg
# #     import numpy as np
# #
# #     if index['colorbar'] == 'temp_pos':
# #         colors_zero2max = temp_colors_pos
# #         colors_min2zero = temp_colors_neg[::-1]
# #     elif index['colorbar'] == 'temp_neg':
# #         colors_zero2max = temp_colors_neg
# #         colors_min2zero = temp_colors_pos[::-1]
# #     elif index['colorbar'] == 'prec_pos':
# #         colors_zero2max = prec_colors_pos
# #         colors_min2zero = prec_colors_neg[::-1]
# #     elif index['colorbar'] == 'prec_neg':
# #         colors_zero2max = prec_colors_neg
# #         colors_min2zero = prec_colors_pos[::-1]
# #
# #     zero = index['hline']
# #
# #     # max = np.amax(param)
# #     # min = np.amin(param)
# #     zero2max = max - zero
# #     min2zero = zero - min
# #
# #     if zero2max > min2zero:
# #         bounds_zero2max, step = np.linspace(zero, max, num=len(colors_zero2max) + 1, retstep=True)
# #         bounds_min2zero = np.arange(min, zero, step)
# #         bounds_zero2max = bounds_zero2max[1:]
# #
# #     if min2zero > zero2max:
# #         bounds_min2zero, step = np.linspace(min, zero, num=len(colors_min2zero), retstep=True, endpoint=False)
# #         bounds_zero2max = np.arange(zero, max, step)
# #         bounds_zero2max = np.append(bounds_zero2max[1:], (bounds_zero2max[-1]+step))
# #     # debug(min)
# #     # debug(max)
# #     # debug(bounds_min2zero)
# #     # debug(bounds_zero2max)
# #     bounds_min2zero = bounds_min2zero.tolist()
# #     bounds_zero2max = bounds_zero2max.tolist()
# #
# #     colors = colors_min2zero[len(colors_min2zero)-len(bounds_min2zero):]
# #     colors.extend(colors_zero2max[0:len(bounds_zero2max)])
# #     debug(colors)
# #
# #     bounds = bounds_min2zero
# #     bounds.extend([zero])
# #     bounds.extend(bounds_zero2max)
# #     debug(bounds)
# #
# #     bounds_float = bounds
# #     if max > 10:
# #         bounds = [round(bound) for bound in bounds_float]
# #
# #     return [bounds, colors]
#
#
#
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib.collections import LineCollection
# # from matplotlib.colors import ListedColormap, BoundaryNorm
# #
# # x = np.linspace(0, 3 * np.pi, 500)
# # y = np.sin(x)
# # dydx = np.cos(0.5 * (x[:-1] + x[1:]))  # first derivative
# #
# # # Create a set of line segments so that we can color them individually
# # # This creates the points as a N x 1 x 2 array so that we can stack points
# # # together easily to get the segments. The segments array for line collection
# # # needs to be (numlines) x (points per line) x 2 (for x and y)
# # points = np.array([x, y]).T.reshape(-1, 1, 2)
# # segments = np.concatenate([points[:-1], points[1:]], axis=1)
# #
# # fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
# #
# # # Create a continuous norm to map from data points to colors
# # norm = plt.Normalize(dydx.min(), dydx.max())
# # lc = LineCollection(segments, cmap='viridis', norm=norm)
# # # Set the values used for colormapping
# # lc.set_array(dydx)
# # lc.set_linewidth(2)
# # line = axs[0].add_collection(lc)
# # fig.colorbar(line, ax=axs[0])
# #
# # # Use a boundary norm instead
# # cmap = ListedColormap(['r', 'g', 'b'])
# # norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
# # lc = LineCollection(segments, cmap=cmap, norm=norm)
# # lc.set_array(dydx)
# # lc.set_linewidth(2)
# # line = axs[1].add_collection(lc)
# # fig.colorbar(line, ax=axs[1])
# #
# # axs[0].set_xlim(x.min(), x.max())
# # axs[0].set_ylim(-1.1, 1.1)
# # plt.show()
#
#
# # import matplotlib.pyplot as plt
# # import numpy as np
# #
# #
# # x = np.linspace(0, 10, 1000)
# # I = np.sin(x) * np.cos(x[:, np.newaxis])
# #
# # # make noise in 1% of the image pixels
# # speckles = (np.random.random(I.shape) < 0.01)
# # I[speckles] = np.random.normal(0, 3, np.count_nonzero(speckles))
# #
# # plt.figure(figsize=(10, 3.5))
# #
# # plt.subplot(1, 2, 1)
# # plt.imshow(I, cmap='RdBu')
# # plt.colorbar(extend='both')
# # plt.clim(-1, 1)
# #
# # plt.subplot(1, 2, 2)
# # plt.imshow(I, cmap='coolwarm')
# # plt.colorbar(extend='both')
# # plt.clim(-1, 2)
# #
# # plt.show()
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
#
# # data = np.random.normal(.4, 2, (10, 10))
# #
# # two_slope_norm = mcolors.TwoSlopeNorm(vmin = -7,
# #                                       vmax = 28,
# #                                       vcenter = 0)
# #
# # plt.imshow(data, cmap = plt.cm.RdBu,
# #            norm = two_slope_norm)
# #
# #
# #
# # plt.colorbar(extend='both')
# # plt.show()
#
#
# #plt.figure(facecolor='w',figsize=(5,4))
# # generate random data
# x = np.random.randint(0,200,(11,11))
# dmin,dmax = 0,200
# two_slope_norm = mcolors.TwoSlopeNorm(vmin = dmin,
#                                       vmax = dmax,
#                                       vcenter = 50)
#
# fig, (ax, cax) = plt.subplots(nrows=2,figsize=(4,5),
#                   gridspec_kw={"height_ratios":[1, 0.2]})
#
# im = ax.imshow(x, cmap=plt.cm.RdBu, norm=two_slope_norm,  aspect='auto')#, vmin=dmin,vmax=dmax)
#
# # create the colorbar
# # the aspect of the colorbar is set to 'equal', we have to set it to 'auto',
# # otherwise twinx() will do weird stuff.
# # ref: Draw colorbar with twin scales - stack overflow -
# # URL: https://stackoverflow.com/questions/27151098/draw-colorbar-with-twin-scales
# cbar = fig.colorbar(im, cax=cax, orientation='horizontal', aspect='auto')
# pos = cbar.ax.get_position()
# ax1 = cbar.ax
#
# ax.axis('scaled')
# # create a second axis and specify ticks based on the relation between the first axis and second aces
# ax2 = ax1.twiny()
# ax2.set_xlim([0,400])
# # newlabel = [300,325,350,375,400,425,450] # labels of the ticklabels: the position in the new axis
# # k2degc = lambda t: t-273.15 # convert function: from Kelvin to Degree Celsius
# # newpos   = [k2degc(t) for t in newlabel]   # position of the ticklabels in the old axis
# # ax2.set_yticks(newpos)
# # ax2.set_yticklabels(newlabel)
#
# # resize the colorbar
# #pos.y0 -= 0.10
# pos.y1 -= 0.09
#
# #ax1.set_aspect('auto')
#
# # arrange and adjust the position of each axis, ticks, and ticklabels
# ax1.set_position(pos)
# ax2.set_position(pos)
# ax1.xaxis.set_ticks_position('top') # set the position of the first axis to right
# ax1.xaxis.set_label_position('top') # set the position of the fitst axis to right
# ax1.set_xlabel(u'Temperature [\u2103]')
# ax2.xaxis.set_ticks_position('bottom') # set the position of the second axis to right
# ax2.xaxis.set_label_position('bottom') # set the position of the second axis to right
# # ax2.spines['left'].set_position(('outward', 50)) # adjust the position of the second axis
# ax2.set_xlabel('Temperature [K]')
#
# plt.show()
# #plt.tight_layout()
# # # Save the figure
# # # plt.savefig('color_ticks_right_left.png', bbox_inches='tight', pad_inches=0.02, dpi=150)



# second axes for relative
# cbar = fig.colorbar(cs, cax=cax, orientation='horizontal')
# ax1 = cbar.ax
# ax1.set_xlabel(str.capitalize(param_units), fontweight='bold')
# pos = ax1.get_position()
# ax2 = ax1.twiny()
# ax2.set_xlim([0, 400])
#
# pos.y1 -= 0.03
#
# ax1.set_position(pos)
# ax2.set_position(pos)
# ax1.xaxis.set_ticks_position('top')
# ax1.xaxis.set_label_position('top')
# ax2.xaxis.set_ticks_position('bottom')
# ax2.xaxis.set_label_position('bottom')
# ax2.set_xlabel('Relative change [%]', fontweight='bold')



# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import matplotlib.cbook as cbook
#
#
# class MidpointNormalize(colors.Normalize):
#     def __init__(self, vmin=None, vmax=None, vcenter=None, clip=False):
#         self.vcenter = vcenter
#         colors.Normalize.__init__(self, vmin, vmax, clip)
#
#     def __call__(self, value, clip=None):
#         # I'm ignoring masked values and all kinds of edge cases to make a
#         # simple example...
#         x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
#         return np.ma.masked_array(np.interp(value, x, y))
#
#
# filename = cbook.get_sample_data('topobathy.npz', asfileobj=False)
# with np.load(filename) as dem:
#     topo = dem['topo']
#     longitude = dem['longitude']
#     latitude = dem['latitude']
#
# #fig, ax = plt.subplots()
# # make a colormap that has land and ocean clearly delineated and of the
# # same length (256 + 256)
# colors_red = plt.cm.Spectral(np.linspace(0, 0.5, 256))
# colors_blue = plt.cm.Spectral(np.linspace(0.66, 1, 256))
# colors_white_red = plt.cm.afmhot(np.linspace(0.8, 1, 40))
# colors_white_blue = plt.cm.Greens(np.linspace(0, 0.3, 20))
# all_colors = np.vstack((colors_red, colors_white_red, colors_white_blue, colors_blue))
# custom_red_blue_map = colors.LinearSegmentedColormap.from_list('custom_red_blue_map', all_colors)
#
# # make the norm:  Note the center is offset so that the land has more
# # dynamic range:
# # divnorm = colors.TwoSlopeNorm(vmin=-500., vcenter=0, vmax=4000)
# #
# # pcm = ax.pcolormesh(longitude, latitude, topo, rasterized=True, norm=divnorm,
# #     cmap=terrain_map,)
# # # Simple geographic plot, set aspect ratio beecause distance between lines of
# # # longitude depends on latitude.
# # ax.set_aspect(1 / np.cos(np.deg2rad(49)))
# # fig.colorbar(pcm, shrink=0.6)
# # plt.show()
#
#
# fig, ax = plt.subplots()
# midnorm = colors.TwoSlopeNorm(vmin=-4000., vcenter=0, vmax=4000)
#
# pcm = ax.pcolormesh(longitude, latitude, topo, rasterized=True, norm=midnorm,
#     cmap = custom_red_blue_map)
# ax.set_aspect(1 / np.cos(np.deg2rad(49)))
# fig.colorbar(pcm, shrink=0.6, extend='both')
# plt.show()


import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.basemap import Basemap


# Define the map boundaries lat/lon

## Map in cylindrical projection (data points may apear skewed)
m = Basemap(resolution='i',projection='cyl',\
    llcrnrlon=282,llcrnrlat=0,\
    urcrnrlon=289,urcrnrlat=9,)


map_list = [
# 'ESRI_Imagery_World_2D',    # 0
# 'ESRI_StreetMap_World_2D',  # 1
# 'NatGeo_World_Map',         # 2
# 'NGS_Topo_US_2D',           # 3
# #'Ocean_Basemap',            # 4
# 'USA_Topo_Maps',            # 5
# 'World_Imagery',            # 6
# 'World_Physical_Map',       # 7     Still blurry
# 'World_Shaded_Relief',      # 8
# 'World_Street_Map',         # 9
'World_Terrain_Base',       # 10
'World_Topo_Map'            # 11
]

for maps in map_list:
    plt.figure(figsize=[10,20])
    ## Instead of using WRF terrain fields you can get a high resolution image from ESRI
    m.arcgisimage(service=maps, xpixels = 3500, dpi=500, verbose= True)
    m.drawstates()
    plt.show()
    plt.title(maps)

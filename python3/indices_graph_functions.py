# This file contains the funcitons to graph the basemaps and timeseries
# Only two functions are required, as the merge should be the same for all indices, with some small variations


def plot_basemap_regions(index, nc_in, png_name_in, region_in, title, min, max, poly_in=False):
    '''

    '''
    from netCDF4 import Dataset
    import numpy as np

    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    import matplotlib.colors as mcolors
    from matplotlib import ticker

    from indices_misc import debug, clean, boxDict, figsize, paral, merid

    box = boxDict[region_in]  # long1, long2, lat1, lat2

    fh = Dataset(nc_in, 'r')

    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    param = fh.variables[index['cdo_name']][0:, :, :]

    fh.close()

    margin = 2
    lon_center = box[0]+(box[1]-box[0])/2
    lat_center = box[2]+(box[3]-box[2])/2

    # fig, (ax, cax) = plt.subplots(nrows=2, figsize=figsize[region_in], gridspec_kw={"height_ratios": [1, 0.1]})
    fig, ax = plt.subplots(nrows=1, figsize=figsize[region_in])

    ax.set_title(title, fontweight='bold', fontsize=10)
    m = Basemap(ax=ax, projection='cass', resolution='l',
                llcrnrlon=box[0]-margin, urcrnrlon=box[1]+margin,
                llcrnrlat=box[2]-margin, urcrnrlat=box[3]+margin,
                lon_0=lon_center, lat_0=lat_center)

    lons_dim = len(lons.shape)
    if 2 == lons_dim:
        lon = lons
        lat = lats
    elif 1 == lons_dim:
        lon, lat = np.meshgrid(lons, lats)
    else:
        print("Error in lon lat array dimension: %d" % lons_dim)

    xi, yi = m(lon, lat)

    # ------ COLORBAR -------
    # 1 - Define some nice colors for temp / prec representation
    colors_red = plt.cm.Spectral(np.linspace(0, 0.5, 256))        # nice yellow to red
    colors_white_red = plt.cm.afmhot(np.linspace(0.8, 1, 30))     # nice white to yellow
    colors_blue = plt.cm.seismic(np.linspace(0, 0.5, 286)[::-1])  # nice white to blue

    all_colors_rb = np.vstack((colors_red, colors_white_red, colors_blue))  # put them together (at this point it is symetric)
    all_colors_br = all_colors_rb[::-1]  # The inverted version for blue to red

    # Choose if you want blue to red or red to blue based on the index
    if index['colorbar'] in ['temp_pos', 'prec_neg']:
        all_colors = all_colors_br
    elif index['colorbar'] in ['temp_neg', 'prec_pos']:
        all_colors = all_colors_rb

    hline = index['hline']  # just to avoid typing
    # the TwoSlopeNorm requires that the parameters are ordered: min center max
    if not (min < hline and max > hline):
        if (min >= hline):
            min = hline - 1
        else:
            max = hline+1

    # now that we know the parameters are ordered, we can make the color bar non-symetric, according to the min/max ratio
    center = min+(max-min)/2

    if abs(max-hline) > abs(hline-min):  # if more pos than neg:
        start = int(round(286*(1-abs(hline-min)/abs(max-hline))))  # calculate the amount of neg we can have, considering 286 is the max
        all_colors_short = all_colors[start:]
    else:  # if more neg than pos
        end = int(round(286*(abs(max-hline)/abs(hline-min))))  # calculate the amount of pos we can have
        all_colors_short = all_colors[:286+end]

    # Finally set the colormap
    two_slope_norm = mcolors.TwoSlopeNorm(vmin=min, vmax=max, vcenter=center)
    color_map = mcolors.LinearSegmentedColormap.from_list('custom_map', all_colors_short)

    # plot
    cs = m.pcolor(xi, yi, np.squeeze(param), alpha=0.7, cmap=color_map, norm=two_slope_norm)
    # Add Colorbar to figure
    cbar = m.colorbar(cs, location='bottom', extend='both', pad='7%')

    if 'rel' in nc_in:
        cbar.set_label('Relative Change [%]', fontsize=9)
    else:
        cbar.set_label(index['units'], fontsize=9)

    cbar.ax.set_xticklabels(cbar.ax.get_xticklabels(), rotation=45, fontsize=8)
    tick_locator = ticker.MaxNLocator(nbins=10)
    cbar.locator = tick_locator
    cbar.update_ticks()

    # Add Grid Lines
    m.drawparallels(paral[region_in], labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(merid[region_in], labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, and Country Boundaries and topo map
    m.drawcoastlines()
    m.drawcountries(color='k')
    m.shadedrelief(alpha=1)

    plt.savefig(png_name_in, dpi=200)
    debug(clean((png_name_in)))
    # plt.show()
    plt.close()


def annot_max(index, x, y, text, color, num, ax=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime as dt  # Python standard library datetime  module

    div = 3
    if 'datatip' not in index:
        return
    if index['datatip'] == 'min':
        xmax = x[np.argmin(y)]
        ymax = y.min()
    elif index['datatip'] == 'max':
        xmax = x[np.argmax(y)]
        ymax = y.max()
    elif index['datatip'] == 'end':
        xmax = x[-1]
        ymax = y[-1]
    elif index['datatip'] == 'endn':
        xmax = x[-1]
        ymax = y[-1]
        div = 7
        num = 1 if num == 2 else 2
    else:
        return

    text = text+"{:.1f}".format(ymax)
    if not ax:
        ax = plt.gca()
    ylim = ax.get_ylim()[1]
    bbox_props = dict(boxstyle="round,pad=0.3", fc=color, ec="k", lw=0.72, zorder=7)
    arrowprops = dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=90", alpha=0.5, zorder=6)
    kw = dict(xycoords='data',   # extcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top", zorder=5, fontsize=9)
    ann = ax.annotate(text, xy=(xmax, ymax), xytext=(dt.datetime(2120, 1, 1), ymax+num*(ylim-ymax)/div), **kw)
    return ann


def annot_avg(text, index):
    import matplotlib.pyplot as plt
    import datetime as dt  # Python standard library datetime  module

    if text is None:
        return
    ax = plt.gca()
    ylim = ax.get_ylim()[1]
    if 'datatip' not in index:
        return
    if index['datatip'] == 'endn':
        ylim = ax.get_ylim()[0]

    bbox_props = dict(boxstyle="round,pad=0.3", fc='lavender', ec="k", lw=0.72, zorder=7)
    kw = dict(xycoords='data',   # extcoords="axes fraction",
              bbox=bbox_props, ha="right", va="top", zorder=5, fontsize=9)
    ann = ax.annotate(text, xy=(dt.datetime(1990, 1, 1), 0), xytext=(dt.datetime(2120, 1, 1), ylim), **kw)
    return ann


def plot_time_series(index, file_path_in_array, models_plot_array=None, region=None, png_name_in=None, min=None, max=None, avg6190=None):
    '''
    plot_time_series ...
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as date_plt
    import datetime as dt  # Python standard library datetime  module
    from netcdftime import utime
    from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/

    from useful_functions import moving_average

    from bisect import bisect_left
    from indices_misc import debug, clean
    import pathlib

    show_each = False
    # if 'Alpine' in file_path_in_array[0]:
    #     return

    date_fill = None
    rcp45_p25_fill = None
    rcp45_p75_fill = None

    rcp85_p25_fill = None
    rcp85_p75_fill = None

    histo_date_fill = None
    histo_rcp45_p25_fill = None
    histo_rcp45_p75_fill = None

    histo_rcp85_p25_fill = None
    histo_rcp85_p75_fill = None

    days_2006 = 57160.5  # 2006 value in time:units = "days since 1850-1-1 00:00:00" ; time:calendar = "standard" ;'
    half_window = 0  # half of the window for the smoothing, in years
    half_window2 = 5  # half of the window for the smoothing, in years

    fig, ax = plt.subplots(figsize=(15, 6))

    if 'do_month' in index and index['do_month']:
        # half_window = half_window*12  # for months
        # half_window2 = half_window2*12  # for months
        half_window = 6  # 1years

    # date [x:-y], where x+y = window - 1
    window = half_window * 2
    date_start = half_window
    date_end = half_window - 1

    window2 = half_window2 * 2
    date_start2 = half_window2
    date_end2 = half_window2 - 1

    to_annotate = []

    #  plot all models, in low alpha, in the background (zorder=1)
    if models_plot_array is not None:
        for model_plot in models_plot_array:
            data_in = Dataset(model_plot, mode='r')

            time = data_in.variables['time'][:]
            param = data_in.variables[index['cdo_name']][:]

            # create time vector
            time_uni = data_in.variables['time'].units
            time_cal = data_in.variables['time'].calendar

            cdftime = utime(time_uni, calendar=time_cal)
            date = [cdftime.num2date(t) for t in time]

            index_2006 = bisect_left(time, days_2006)

            param_scaled_smoothed = moving_average(arr=param[:, 0, 0], win=window)

            if 'rcp45' in model_plot:
                plt.plot(date[date_start: index_2006],  param_scaled_smoothed[:index_2006-date_start],   'k', alpha=0.01, zorder=1)
                plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_scaled_smoothed[index_2006-1-date_end-1:], 'g', alpha=0.02, zorder=1)
            elif 'rcp85' in model_plot:
                plt.plot(date[date_start: index_2006],  param_scaled_smoothed[:index_2006-date_start],   'k', alpha=0.01, zorder=1)
                plt.plot(date[index_2006-1: -date_end if window > 0 else None], param_scaled_smoothed[index_2006-1-date_end-1:], 'r', alpha=0.02, zorder=1)

    # plot median, in foreground (zorder = 4), and collect data for the shadows
    for file_path_in in file_path_in_array:

        debug(clean((file_path_in)))

        data_in = Dataset(file_path_in, mode='r')

        time = data_in.variables['time'][:]
        param = data_in.variables[index['cdo_name']][:]

        # create time vector
        time_uni = data_in.variables['time'].units
        time_cal = data_in.variables['time'].calendar

        cdftime = utime(time_uni, calendar=time_cal)
        date = [cdftime.num2date(t) for t in time]

        # ############# A plot of Maximum precipitation ##############

        index_2006 = bisect_left(time, days_2006)

        param_smoothed = moving_average(arr=param[:, 0, 0], win=window)
        param_smoothed2 = moving_average(arr=param[:, 0, 0], win=window2)

        if "25" in file_path_in and "rcp45" in file_path_in:
            rcp45_p25_fill = param_smoothed[index_2006-1-date_end-1:]
            histo_rcp45_p25_fill = param_smoothed[:index_2006-date_start]
            # plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'palegreen', zorder=4)
            # plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],  'silver', zorder=4)

        elif "75" in file_path_in and "rcp45" in file_path_in:
            rcp45_p75_fill = param_smoothed[index_2006-1-date_end-1:]
            date_fill = date[index_2006-1:-date_end if window > 0 else None]
            histo_rcp45_p75_fill = param_smoothed[:index_2006-date_start]
            histo_date_fill = date[date_start:index_2006]
            # plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'palegreen', zorder=4)
            # plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],  'silver', zorder=4)

        elif "rcp45" in file_path_in:
            plt.plot(date[index_2006-1: -date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'g', zorder=4, alpha=0.3)  # label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
            plt.plot(date[index_2006-1: -date_end2 if window2 > 0 else None], param_smoothed2[index_2006-1-date_end2-1:], 'g', label="RCP45", zorder=5)
            to_annotate.append([date[index_2006-1: -date_end2 if window2 > 0 else None], param_smoothed2[index_2006-1-date_end2-1:], 'palegreen', 1])
            if show_each:
                plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],   'k', zorder=4, label=pathlib.Path(file_path_in).stem.split("45")[0]) #.split("_histo")[0])
            else:
                plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],   'k', zorder=4, alpha=0.15)
                plt.plot(date[date_start2: index_2006],  param_smoothed2[:index_2006-date_start2],  'k', zorder=4, label="Historical")

        if "25" in file_path_in and "rcp85" in file_path_in:
            rcp85_p25_fill = param_smoothed[index_2006-1-date_end-1:]
            histo_rcp85_p25_fill = param_smoothed[:index_2006-date_start]
            # plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'lightsalmon', zorder=4)
            # plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],  'silver', zorder=4)

        elif "75" in file_path_in and "rcp85" in file_path_in:
            rcp85_p75_fill = param_smoothed[index_2006-1-date_end-1:]
            date_fill = date[index_2006-1:-date_end if window > 0 else None]
            histo_rcp85_p75_fill = param_smoothed[:index_2006-date_start]
            histo_date_fill = date[date_start:index_2006]
            # plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'lightsalmon', zorder=4)
            # plt.plot(date[date_start: index_2006],  param_smoothed[:index_2006-date_start],  'silver', zorder=4)

        elif "rcp85" in file_path_in:
            plt.plot(date[index_2006-1:-date_end if window > 0 else None], param_smoothed[index_2006-1-date_end-1:], 'r', zorder=4, alpha=0.3)  # label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
            plt.plot(date[index_2006-1: -date_end2 if window2 > 0 else None], param_smoothed2[index_2006-1-date_end2-1:], 'r', label="RCP45", zorder=5)
            to_annotate.append([date[index_2006-1: -date_end2 if window2 > 0 else None], param_smoothed2[index_2006-1-date_end2-1:], 'lightsalmon', 2])
            if show_each:
                plt.plot(date[date_start:index_2006],  param_smoothed[:index_2006-date_start],   'k', zorder=4, label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
            else:
                plt.plot(date[date_start:index_2006],  param_smoothed[:index_2006-date_start],   'k', zorder=4, alpha=0.15)  # label=pathlib.Path(file_path_in).stem.split("45")[0])#.split("_histo")[0])
        data_in.close()

        if show_each:
            plt.legend()  # loc=(0, 0), fontsize=7, frameon=True, ncol=11,  bbox_to_anchor=(0, -0.5))  # Legend for smoothed
            plt.tight_layout(rect=[0, 0, 1, 1])
            # add horizontal line
            plt.axhline(y=index['hline'], color='k')
            # highligth 1961 to 1990 range
            plt.axvspan(dt.datetime(1961, 1, 1), dt.datetime(1990, 12, 30), color='b', alpha=0.1)
            plt.grid(b=True, linestyle='--', linewidth=1)
            plt.show()

    # Ends loop, plot shading, zorder=2 for white, zorder=3 for green and red
    if rcp45_p25_fill is not None:
        plt.fill_between(date_fill, rcp45_p25_fill, rcp45_p75_fill,
                         facecolor="g",    # The fill color
                         # color='',       # The outline color
                         alpha=0.2, zorder=3)        # Transparency of the fill
        plt.fill_between(date_fill, rcp45_p25_fill, rcp45_p75_fill,
                         facecolor="white",    # The fill color
                         # color='',       # The outline color
                         zorder=2)

    if rcp85_p25_fill is not None:
        plt.fill_between(date_fill, rcp85_p25_fill, rcp85_p75_fill,
                         facecolor="r",    # The fill color
                         # color='',       # The outline color
                         alpha=0.2, zorder=3)        # Transparency of the fill

        plt.fill_between(date_fill, rcp85_p25_fill, rcp85_p75_fill,
                         facecolor="white",    # The fill color
                         # color='',       # The outline color
                         zorder=2)        # Transparency of the fill

    if histo_rcp45_p25_fill is not None:
        plt.fill_between(histo_date_fill, histo_rcp45_p25_fill, histo_rcp45_p75_fill,
                         facecolor="silver",    # The fill color
                         # color='',       # The outline color
                         alpha=1, zorder=2)

    if histo_rcp85_p25_fill is not None:
        plt.fill_between(histo_date_fill, histo_rcp85_p25_fill, histo_rcp85_p75_fill,
                         facecolor="silver",   # The fill color
                         # color='',      # The outline color
                         alpha=1, zorder=2)       # Transparency of the fill

    # plt.tight_layout(rect=[0, 0, 1, 1])

    # add horizontal line at y=0

    plt.axhline(y=index['hline'], color='k', alpha=0.2, linestyle='--')
    # debug(clean((list(plt.yticks()[0]))))
    # plt.yticks(list(plt.yticks()[0]) + [index['hline']])
    if avg6190 is None or ('do_rel' in index and not index['do_rel']):
        ax.secondary_yaxis('right', functions=(lambda x: x, lambda x: x))
    else:
        secaxy = ax.secondary_yaxis('right', functions=(lambda x: (x*100)/abs(avg6190), lambda x: (x*abs(avg6190))/100))
        secaxy.set_ylabel('Relative change [%]', fontweight='bold')

    # if avg6190 is not None:
    #     plt.title(index['short_desc'].split('(')[1].split(')')[0]+" [1961:1990] = "+str(round(float(avg6190), 1))+"           ", loc='right', fontsize=10)

    # highligth periods
    plt.axvspan(dt.datetime(1961, 1, 1), dt.datetime(1990, 12, 30), color='b', alpha=0.05)
    plt.axvspan(dt.datetime(1861, 1, 1), dt.datetime(1890, 12, 30), color='k', alpha=0.05)
    plt.axvspan(dt.datetime(1991, 1, 1), dt.datetime(2020, 12, 30), color='k', alpha=0.05)
    plt.axvspan(dt.datetime(2061, 1, 1), dt.datetime(2090, 12, 30), color='k', alpha=0.05)
    plt.axvline(x=dt.datetime(2006, 1, 1), color='k', alpha=0.2, linestyle='--')

    plt.grid(linestyle='dotted', linewidth=1, axis='y', alpha=0.4)

    cdftime = utime(time_uni, calendar=time_cal)
    date = [cdftime.num2date(time[140])]
    dates = [dt.datetime(1861,  1,  1),
             dt.datetime(1890, 12, 30),
             dt.datetime(1961,  1,  1),
             dt.datetime(1990, 12, 30),
             dt.datetime(2006,  1,  1),
             dt.datetime(2020,  1,  1),
             dt.datetime(2061,  1,  1),
             dt.datetime(2090, 12, 30)]

    dates_plot = [date_plt.date2num(date) for date in dates]
    plt.xticks(dates_plot)
    # format the ticks
    years_fmt = date_plt.DateFormatter('%Y')
    ax.xaxis.set_major_formatter(years_fmt)
    plt.xlim(dt.datetime(1861,  1,  1), dt.datetime(2090,  1,  1))

    # plt.ticklabel_format(useOffset=True, axis='y')
    plt.title(index['short_desc'], fontweight='bold')
    if region is not None:
        plt.title("         "+region, loc='left', fontsize=10)

    leg_loc = 'upper left'
    if 'legend' in index:
        leg_loc = index['legend']
    plt.legend(loc=leg_loc, fancybox=True, facecolor='white')

    if 'do_month' in index and index['do_month']:
        plt.xlabel("Month", fontweight='bold')
    else:
        plt.xlabel("Year", fontweight='bold')

    plt.ylabel(index['units'], fontweight='bold')

    if png_name_in is None:
        plt.show()
    else:

        nice_name = index['short_desc'].split('(')[1].split(')')[0] + ' = '
        if avg6190 is not None:
            avg_name = (index['short_desc'].split('(')[1].split(')')[0]+" [1961:1990] = "+str(round(float(avg6190), 1)))
        else:
            avg_name = None

        debug(clean((png_name_in)))
        ann_list = []
        for [x, y, color, num] in to_annotate:
            ann_list.append(annot_max(index, x, y, nice_name, color, num))
        ann_list.append(annot_avg(avg_name, index))
        plt.savefig(png_name_in.replace('.png', '_ind.png'), dpi=150, bbox_inches="tight")

        for ann in ann_list:
            if ann is not None:
                ann.remove()

        if min is not None and max is not None:
            plt.ylim(min, max)

        ann_list = []
        for [x, y, color, num] in to_annotate:
            ann_list.append(annot_max(index, x, y, nice_name, color, num))
        ann_list.append(annot_avg(avg_name, index))

        plt.savefig(png_name_in, dpi=150, bbox_inches="tight")

        for ann in ann_list:
            if ann is not None:
                ann.remove()

        if 'limits' in index:
            plt.ylim(index['limits'][0], index['limits'][1])

            ann_list = []
            for [x, y, color, num] in to_annotate:
                ann_list.append(annot_max(index, x, y, nice_name, color, num))
            ann_list.append(annot_avg(avg_name, index))

            plt.savefig(png_name_in.replace('.png', '_lim_'+str(index['limits'][1])+'.png'), dpi=150, bbox_inches="tight")


def plot_bar(index, regions, glob45, glob85, png_name_in, rel=False):

    import matplotlib.pyplot as plt
    from math import copysign
    from indices_misc import debug, clean

    start = 0
    end = 4
    barSep = 0.55
    barWidth = 0.3
    startpos = [1.5, 2.5+(len(regions)+1)*barSep]  # position for RCP45 and RCP85 in a 0 to 3 line
    color = {'Global': 'lightgray', 'Alpine': 'papayawhip', 'Andes': 'paleturquoise'}

    texts = []
    pos = list(startpos)

    plt.figure()

    if glob45 is not None:
        bars = [glob45-index['hline'], glob85-index['hline']]

        plt.bar(pos, bars, width=barWidth, bottom=index['hline'], color=color['Global'], edgecolor='gray', capsize=2, label='Global')

        texts.append(plt.text(pos[0], glob45, str(round(float(glob45), 1)), zorder=4, ha='center', va='center', fontsize=9,
                     bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': -2, 'alpha': 0.5}))

        texts.append(plt.text(pos[1], glob85, str(round(float(glob85), 1)), zorder=4, ha='center', va='center', fontsize=9,
                     bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': -2, 'alpha': 0.5}))

        pos[0] += barSep+0.05
        pos[1] += barSep+0.05
        end += barSep

    for name, values in regions.items():
        bars = [values['rcp45']-index['hline'], values['rcp85']-index['hline']]
        errors = [[values['rcp45']-values['rcp45_25'], values['rcp85']-values['rcp85_25']],
                  [values['rcp45_75']-values['rcp45'], values['rcp85_75']-values['rcp85']]]

        plt.bar(pos, bars, width=barWidth, bottom=index['hline'], color=color[name], edgecolor='gray', yerr=errors, label=name,
                error_kw=dict(ecolor='gray', lw=1, capsize=3, capthick=1, alpha=0.5))

        texts.append(plt.text(pos[0], values['rcp45'], str(round(float(values['rcp45']), 1)), zorder=4, ha='center', va='center', fontsize=9,
                     bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': -2, 'alpha': 0.5}))
        texts.append(plt.text(pos[1], values['rcp85'], str(round(float(values['rcp85']), 1)), zorder=4, ha='center', va='center', fontsize=9,
                     bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': -2, 'alpha': 0.5}))

        pos[0] += barSep
        pos[1] += barSep
        end += barSep*2

    ax = plt.gca()

    correct = (ax.get_ylim()[1]-ax.get_ylim()[0])/25
    for text in texts:
        xtext, ytext = text.get_position()
        ytext -= index['hline']
        correct = copysign(correct, ytext)
        ytext = ytext+correct
        ytext += index['hline']
        text.set_position([xtext, ytext])
        if ytext < index['hline']:
            # ax.tick_params(axis="x", pad=-15)
            plt.legend(loc='lower left', fontsize=8)
            plt.title(index['short_desc'], fontweight='bold', pad=25)
        else:
            plt.legend(loc='upper left', fontsize=8)
            plt.title(index['short_desc'], fontweight='bold', pad=10)
    # ticks = [(pos[0]-startpos[0])/2.0 + startpos[0]-barSep/2, (pos[1]-startpos[1])/2.0 + startpos[1]-barSep/2]
    plt.text((pos[0]-startpos[0])/2.0 + startpos[0]-barSep/2, ax.get_ylim()[0]-abs(correct), 'RCP4.5', ha='center', va='top', fontweight='bold')
    plt.text((pos[1]-startpos[1])/2.0 + startpos[1]-barSep/2, ax.get_ylim()[0]-abs(correct), 'RCP8.5', ha='center', va='top', fontweight='bold')

    if rel:
        plt.ylabel('Relative Change [%]')
    else:
        plt.ylabel(index['units'])

    # spine left and bottom at zero. The x does not need ticks
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()
    ax.spines['bottom'].set_position(['data', index['hline']])
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('none')

    # kwargs = dict(fontweight='bold')
    # plt.xticks(ticks, ['RCP4.5', 'RCP8.5'], **kwargs)
    plt.xticks([])
    plt.xlim(start, end)
    # plt.show()
    debug(clean(png_name_in))
    plt.savefig(png_name_in, dpi=150, bbox_inches="tight")


def plot_bar_index(index, files, png_name_in, avg6190):

    from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
    from useful_functions import moving_average

    window = 10
    regions = {}
    regions_rel = {}

    for region in files:
        regions[region] = {'rcp45': None, 'rcp45_25': None, 'rcp45_75': None,
                           'rcp85': None, 'rcp85_25': None, 'rcp85_75': None}

        regions_rel[region] = {'rcp45': None, 'rcp45_25': None, 'rcp45_75': None,
                               'rcp85': None, 'rcp85_25': None, 'rcp85_75': None}

        for file_path_in in files[region]:
            data_in = Dataset(file_path_in, mode='r')
            param = data_in.variables[index['cdo_name']][:]
            param_smoothed = moving_average(arr=param[:, 0, 0], win=window)
            value = param_smoothed[-1]
            value_rel = value
            if index['do_rel']:
                value_rel = (value*100)/abs(avg6190[region])

            if "25" in file_path_in and "rcp45" in file_path_in:
                regions[region]['rcp45_25'] = value
                regions_rel[region]['rcp45_25'] = value_rel

            elif "75" in file_path_in and "rcp45" in file_path_in:
                regions[region]['rcp45_75'] = value
                regions_rel[region]['rcp45_75'] = value_rel

            elif "rcp45" in file_path_in:
                regions[region]['rcp45'] = value
                regions_rel[region]['rcp45'] = value_rel

            if "25" in file_path_in and "rcp85" in file_path_in:
                regions[region]['rcp85_25'] = value
                regions_rel[region]['rcp85_25'] = value_rel

            elif "75" in file_path_in and "rcp85" in file_path_in:
                regions[region]['rcp85_75'] = value
                regions_rel[region]['rcp85_75'] = value_rel

            elif "rcp85" in file_path_in:
                regions[region]['rcp85'] = value
                regions_rel[region]['rcp85'] = value_rel

    glob45 = None
    glob85 = None
    glob45_rel = None
    glob85_rel = None
    if 'glob_rcp45' in index:
        glob45 = index['glob_rcp45']
        glob85 = index['glob_rcp85']
        if index['do_rel']:
            glob45_rel = glob45*100/abs(index['glob_avg6190'])
            glob85_rel = glob85*100/abs(index['glob_avg6190'])

    plot_bar(index, regions, glob45, glob85, png_name_in)
    if index['do_rel']:
        plot_bar(index, regions_rel, glob45_rel, glob85_rel, png_name_in.replace('.png', '_rel.png'), rel=True)

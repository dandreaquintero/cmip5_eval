from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from useful_functions import draw_map


def draw_screen_poly(lats, lons, m):
    x, y = m(lons, lats )
    xy = zip(x, y)
    poly = Polygon(list(xy), fc=(1,0,0,0.3), ec=(0.8,0,0,1), lw=2 )
    plt.gca().add_patch(poly)


nc_file = "pr_Amon_MPI-ESM-P_historical_r1i1p1_185001-200512"
nc_dir = "../nc_files/"
model_dir = "cmip5_converted/MPI-ESM-P/pr/"

# Map Colombia
fig3 = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution='h',
            llcrnrlat=-3, urcrnrlat=13,
            llcrnrlon=281, urcrnrlon=285,)  # lower-left corner, upper-right corner

lat0 = 1
lat1 = 5

lon0 = 300-360
lon1 = 290-360
resolution = 5

lats = np.hstack((np.linspace( lat0, lat1, resolution ), np.linspace( lat1, lat0, resolution )))
lons = np.hstack((np.linspace( lon0, lon0, resolution ), np.linspace( lon1, lon1, resolution )))

print(lats)
print(lons)

m = Basemap(projection='ortho', lon_0=0)
m = Basemap(projection='ortho', lat_0=5, lon_0=-60, resolution='l')
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral', lake_color='aqua')
m.drawcoastlines()
# lats and longs are returned as a dictionary
m.drawparallels(np.linspace(-90, 90, 20))
m.drawmeridians(np.linspace(-180, 180, 20))

draw_screen_poly(lats, lons, m)

map = Basemap(projection='cyl')

draw_map(m, 1)

plt.show()

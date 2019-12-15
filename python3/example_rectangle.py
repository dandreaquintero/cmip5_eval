from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def draw_screen_poly(lats, lons, m):
    x, y = m(lons, lats)
    xy = zip(x, y)
    poly = Polygon(list(xy), fc=(1, 0, 0, 0.3), ec=(0.8, 0, 0, 1), lw=2)
    plt.gca().add_patch(poly)


lat0 = -3
lat1 = 13

lon0 = 281-360
lon1 = 294-360
resolution = 10

lats = np.hstack((np.linspace(lat0, lat1, resolution),
                  np.linspace(lat1, lat0, resolution)))

lons = np.hstack((np.linspace(lon0, lon0, resolution),
                  np.linspace(lon1, lon1, resolution)))

print(lats)
print(lons)

m = Basemap(projection='sinu', lon_0=0)
m = Basemap(projection='ortho', lat_0=5, lon_0=-60, resolution='l')
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral', lake_color='aqua')
m.drawcoastlines()
# lats and longs are returned as a dictionary
m.drawparallels(np.linspace(-90, 90, 20))
m.drawmeridians(np.linspace(-180, 180, 20))

draw_screen_poly(lats, lons, m)

plt.show()

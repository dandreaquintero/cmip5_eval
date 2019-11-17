import cartopy.crs as ccrs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

plt.show()

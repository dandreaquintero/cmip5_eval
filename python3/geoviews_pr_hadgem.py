import geoviews as gv
import geoviews.feature as gf
import xarray as xr
from cartopy import crs

gv.extension('bokeh', 'matplotlib')

(gf.ocean + gf.land + gf.ocean * gf.land * gf.coastline * gf.borders).opts(
    'Feature', projection=crs.Geostationary(), global_extent=True, height=325).cols(3)

# nc_file = "pr_Amon_HadGEM2AO_standardCal.nc"
# nc_dir = "../nc_files/"
# cmip5_std_dir = "cmip5_standardCal/"
# nc_in = nc_dir+cmip5_std_dir+nc_file  # Your filename
# dataset = gv.Dataset(xr.open_dataset(nc_in))
# ensemble = dataset.to(gv.Image, ['lon', 'lat'], 'pr')
#
# gv.output(ensemble.opts(cmap='viridis', colorbar=True, fig_size=200, backend='matplotlib') * gf.coastline(),
#           backend='matplotlib')

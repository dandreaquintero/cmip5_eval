# ******* SETUP ***********

# Installed python3 using brew
brew install python

# Installed python2 using brew
brew install python@2

# pip3 was installed with python3
# pip2 was installed with python2

# Installed virtualenv using pip3
pip3 install virtualenv

# Installed virtualenv using pip2
pip2 install virtualenv

# Created work directory and virtual venv3
mkdir python3
cd python3
python3 -m venv venv3 # or virtualenv --python=python3 venv3

# Created work directory and virtual venv2
mkdir python2
cd python2
virtualenv --python=python2 venv2

# Activate virtual env with:
source venv3/bin/activate
source venv2/bin/activate

#check python and pip are the venv3/venv2 versions with
python --version
pip --version

# Installed Required pacakges inside virtual env
pip install xarray dask netCDF4 bottleneck  #for parallel computing with dask
pip install matplotlib   #for plotting
pip install seaborn      #for better colour palet
pip install https://github.com/matplotlib/basemap/archive/master.zip #old version of cartopy
pip install cython
pip uninstall shapely; pip install --no-binary :all: shapely #otherwise cartopy crashes
pip install scipy
#pip install cartopy #fails because version issue of proj6

#https://github.com/SciTools/cartopy/pull/1289/commits
#enable installing with PROJ 6.0.0 #1289
pip install git+https://github.com/snowman2/cartopy.git@5e624fe
pip install geoviews
#reset DYLD_FALLBACK_LIBRARY_PATH that is set in .bash_profile as /opt/local/lib/gcc7/
#For something else (ncl?)

pip intall cdo # install cdo: climate data operators

export DYLD_FALLBACK_LIBRARY_PATH=$(HOME)/lib:/usr/local/lib:/lib:/usr/lib
export DYLD_FALLBACK_LIBRARY_PATH=#empty also works


#  ********* INSTRUCTIONS ********

# Activate virtual env with:
source venv3/bin/activate
source venv2/bin/activate

#execute
python test.py

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
source venv3/bin/activate  # source deactivate: to exist of the environment
source venv2/bin/activate  # to remove an envirm: brew env remove -n venv3

#check python and pip are the venv3/venv2 versions with
python --version
pip --version

# Install Required pacakges inside virtual env
pip install numpy
pip install xarray dask netCDF4 bottleneck  #for parallel computing with dask
pip install matplotlib   #for plotting
pip install seaborn      #for better colour palet
pip install https://github.com/matplotlib/basemap/archive/master.zip #old version of cartopy
pip install cython
pip uninstall shapely; pip install --no-binary :all: shapely #otherwise cartopy crashes
pip install scipy        #scientific function, integraters,interpolations
#pip install cartopy #fails because version issue of proj6

#https://github.com/SciTools/cartopy/pull/1289/commits
#enable installing with PROJ 6.0.0 #1289
pip install git+https://github.com/snowman2/cartopy.git@5e624fe
pip install geoviews
#reset DYLD_FALLBACK_LIBRARY_PATH that is set in .bash_profile as /opt/local/lib/gcc7/
#For something else (ncl?)

pip intall cdo # install cdo: climate data operators

pip install nc-time-axis
pip install netcdftime

#matplotlib backend:
#TkAgg works, but crashes when scrolling.
#Instead of solve, better to use QT5 (only for python3)
pip install PyQt5

#choose the backend in each script with:
import matplotlib
matplotlib.use('Qt5agg')
import matplotlib.pyplot as plt

#Or, easier edit file:
vim ~/.matplotlib/matplotlibrc
#and add for Qt5agg
backend: Qt5agg
#or
backend: TkAgg


export DYLD_FALLBACK_LIBRARY_PATH=$(HOME)/lib:/usr/local/lib:/lib:/usr/lib
export DYLD_FALLBACK_LIBRARY_PATH=#empty also works


#  ********* INSTRUCTIONS ********

# Activate virtual env with:
source venv3/bin/activate
source venv2/bin/activate

#execute
python test.py

# ******* DOCKER ******

# 1 start docker app from launcher
Docker

# 2 Mode to docker directory
cd Documents/tesis/climate4impact-portal

# 3 Start docker
docker run -v ~/impactspace:/impactspace -v /etc/hosts:/etc/hosts -v `pwd`/docker/c4i_config:/config/ -p 444:444 -e EXTERNAL_HOSTNAME:${HOSTNAME} -e EXTERNAL_ADDRESS_HTTPS="https://${HOSTNAME}:444/" -it c4i

# 4 Access from firefox to
https://localhost:444/impactportal/account/login.jsp
# Show other providers -> BADC/CEDA openID
# with credentials
user cc4idev
pass cc4idev123!


# ************** CONDA and cdo dev version **************

# follow official instructions to download conda (Miniconda bash script
# https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html
# make sure to downlaod the python3 version of the script
bash Miniconda3-latest-MacOSX-x86_64.sh

# create an env and install cdo dev: https://slides.com/wachsylon/cdoetccdi#/3
conda create --name cdoenv conda-forge/label/dev::cdo -c conda-forge

#activate env
conda activate cdoenv

#if in linux, install 
sudo apt-get install -y libgeos-dev
sudo apt-get install libproj-dev
sudo apt-get install libgeos++-dev
conda install -c conda-forge cartopy
#then if cdo is downgraded to the official release, intall the dev again:
conda install conda-forge/label/dev::cdo -c conda-forge

# pip install all the required packages (same as with brew)
pip install cdo
pip install xarray
pip install numpy
pip install dask netCDF4 bottleneck
pip install matplotlib
pip install seaborn
pip install https://github.com/matplotlib/basemap/archive/master.zip
pip install cython
pip uninstall shapely; pip install --no-binary :all: shapely
pip install scipy
pip install git+https://github.com/snowman2/cartopy.git@5e624fe
pip install geoviews
pip install nc-time-axis
pip install PyQt5

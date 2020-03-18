from exceptions import *
from dakota_file import DakotaFile
import numpy as np
import xarray as xr
import main
import os

my_netcdf = DakotaFile()

name = 'test_scan1'
var_type = 'scan'

# Make a dictionary of the needed data
lower_bounds  = np.array( [ 1.0, 3.0 ] )
upper_bounds  = np.array( [ 2.0, 4.0 ] )
partitions    = np.array( [ 1,   1   ] ) 

variable_dict = { 'lower_bounds' : lower_bounds, 'upper_bounds' : upper_bounds, 'partitions' : partitions }

my_netcdf.add_variable_from_dict( name, var_type, variable_dict )

name = 'test_scan2'
var_type = 'scan'

lower_bounds = 0.0
upper_bounds = 1.0
partitions   = 1

dataset = xr.Dataset( {'lower_bounds' : lower_bounds, 'upper_bounds' : upper_bounds, 'partitions' : partitions } )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

name = 'test_scan3'
var_type = 'scan'

variable_dict = { 'lower_bounds' : np.array(10), 'upper_bounds' : np.array(15), 'partitions' : np.array(1) }

my_netcdf.add_variable_from_dict( name, var_type, variable_dict )

filename = 'DAKOTA.nc'
my_netcdf.write(filename)



# This file serves creates an example netCDF file to demonstrate the tools
# for reading and writing parameter scan data. 

from exceptions import *
from dakota_file import DakotaFile
import numpy as np
import xarray as xr
import main
import os

# First create an instance of the dakota_netcdf class!
my_netcdf = DakotaFile()

# Unlike the Monte-Carlo sampling case we do not need any run settings
# so the add_settings function should not be called

# We need to add some parameter scan variables

# ------------------------------------------------------------------------
# WRITE EXAMPLE 1
# ------------------------------------------------------------------------

# The simplest way is to build a dictionary of needed variables and call
# the add_variable_from_dict function.

# Performing a parameter scan requires 3 variables. Upper and lower bounds
# and the number of partitions. 

# Give our variable a name!
name = 'test_scan1'

# Specify that the variable should be scanned
var_type = 'scan'

# Make a dictionary of the needed data
lower_bounds  = np.random.rand(4,3)
upper_bounds  = np.random.rand(4,3)
partitions    = np.random.randint(2,10,size=(4,3))

variable_dict = { 'lower_bounds' : lower_bounds, 'upper_bounds' : upper_bounds, 
                  'partitions' : partitions }

my_netcdf.add_variable_from_dict( name, var_type, variable_dict )

# -----------------------------------------------------------------------
# WRITE EXAMPLE 2
# -----------------------------------------------------------------------

# We can also add a variable by constructing an Xarray dataset
# To do this the data must be created as data arrays and then added to the dataset

# Create a name for this new variable
name = 'test_scan2'

var_type = 'scan'

lower_bounds1 = xr.DataArray(lower_bounds)
upper_bounds1 = xr.DataArray(upper_bounds) 
partitions1   = xr.DataArray(partitions)

dataset = xr.Dataset( {'lower_bounds' : lower_bounds1, 'upper_bounds' : upper_bounds1,
                       'partitions' : partitions1 } )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

# ----------------------------------------------------------------------
# WRITE EXAMPLE 3
# ----------------------------------------------------------------------

# One of the advantages of using a dataset is that one can also specify the dimensions
# and coordinates of variables. It may be convenient to have these available in the 
# interface script.

# Create a name for this new variable
name = 'test_scan3'

var_type = 'scan'

# Coordinates
x = np.array( [0.2,0.3,0.4,0.5,0.6] )
y = np.array( [2.5,3.5,4.5] )
z = np.array( [5.2,5.3] ) 

# Convert coordinates to data arrays
x = xr.DataArray(x,dims=['x'])
y = xr.DataArray(y,dims=['y'])
z = xr.DataArray(z,dims=['z'])

# Construct variable data arrays which include dimensions and coordinates
lower_bounds = np.random.rand(5,3,2)
lower_bounds = xr.DataArray(lower_bounds, coords=[x,y,z], dims=['x','y','z'])

upper_bounds = np.random.rand(5,3,2) + 2.0
upper_bounds = xr.DataArray(upper_bounds, coords=[x,y,z], dims=['x','y','z'])

partitions   = np.random.randint(2,10,size=(5,3,2))
partitions   = xr.DataArray(partitions,   coords=[x,y,z], dims=['x','y','z'])

dataset = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds,
                       'partitions':partitions}, attrs={'type':'scan'} )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

# -----------------------------------------------------------------------
# WRITE EXAMPLE 4
# -----------------------------------------------------------------------

# We can also add a variable by constructing an Xarray dataset directly from numpy
# arrays if coordinate information is not required

# Create a name for this new variable
name = 'test_scan4'

var_type = 'scan'

lower_bounds = 0.0
upper_bounds = 1.0
partitions   = 7

dataset = xr.Dataset( {'lower_bounds' : lower_bounds, 'upper_bounds' : upper_bounds,
                       'partitions' : partitions } )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

# ----------------------------------------------------------------------
# WRITE THE FILE
# ----------------------------------------------------------------------

filename = 'DAKOTA.nc'
my_netcdf.write(filename)

#=======================================================================
# READING EXAMPLES 
#=======================================================================

# To build an interface between DAKOTA and your code you will need to write something
# to read a netcdf file like the one just created and pass the new data to your code.
# The following examples demonstrate reading a netcdf.

# Create a new instance of the 
my_netcdf2 = DakotaFile()

filename = 'DAKOTA.nc'
my_netcdf2.read(filename)

# ----------------------------------------------------------------------
# READ EXAMPLE 1
# ----------------------------------------------------------------------

# We can read one of the variables in the netcdf file back into a dictionary of data
# We shall read test_scan2 which was originally written as a dataset

variable_dict = my_netcdf2.get_variable_as_dict('test_scan2')

print('Read Example 1:')
print()

for key, var in variable_dict.items():

    print( key+':' )
    print( var )
    print()

# After running DAKOTA the varied data for each variable should be available as the
# 'values' entry of that variable's dictionary: variable_dict['values']

# ----------------------------------------------------------------------
# READ EXAMPLE 2
# ----------------------------------------------------------------------

# We can also read a variable in the netcdf file back into a dataset
# If the coordinates were also written to the data arrays or the dataset itself
# these will also be available

dataset = my_netcdf2.get_variable_as_dataset('test_scan3')

print('Read Example 2:')
print()

for key in dataset:

    print( key+':' )
    print( dataset[key].dims )
    print( dataset[key].coords )
    print( dataset[key].data )
    print()

# After running DAKOTA the varied data for each variables should be available within the
# 'values' data array of the variables dataset: dataset['values'].data

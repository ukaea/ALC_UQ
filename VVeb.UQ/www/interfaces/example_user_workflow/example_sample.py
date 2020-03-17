# This file creates an example netcdf file in order to demonstrate the tools for reading and writing
# uncertain variable data.

# Include dakota folder
import sys
sys.path.insert(1, '/dakota_utils/')

import numpy as np
import xarray as xr
from dakota_file import DakotaFile

# First create an instance of the dakota_netcdf class!
my_netcdf = DakotaFile()

# Before doing anything else we need to configure how DAKOTA will run. This means passing
# a dictionary of settings. At present the following settings are needed:
# sample_type            - This can be 'random' for pure MC or 'lhs' for Latin Hypercube Sampling
# samples                - The number of samples to generate
# seed                   - The random number seed. Must be at least 1

settings = {'sample_type' : 'lhs',
            'samples'     : 4,
            'seed'        : 3947 }

my_netcdf.add_settings( settings )

# We need to add some uncertain variables...

# ------------------------------------------------------------------------
# WRITE EXAMPLE 1
# ------------------------------------------------------------------------

# The simplest way is to build a dictionary of needed variables and call
# the add_variable_from_dict function.

# We'll use a normal uncertain variable as an example. This requires two pieces
# of input data: means and standard deviations.

# Give our variable a name!
name = 'test_normal1'

# Specify the uncertainty distribution
var_type = 'normal'

# Make a dictionary of the needed data
means          = np.random.rand(4,3)
std_deviations = np.random.rand(4,3)

variable_dict = { 'means' : means, 'std_deviations' : std_deviations }

my_netcdf.add_variable_from_dict( name, var_type, variable_dict )

# -----------------------------------------------------------------------
# WRITE EXAMPLE 2
# -----------------------------------------------------------------------

# We can also add a variable by constructing an Xarray dataset
# To do this the data must be created as data arrays and then added to the dataset

# Create a name for this new variable
name = 'test_normal2'

var_type = 'normal'

means          = xr.DataArray(means)
std_deviations = xr.DataArray(std_deviations) 

dataset = xr.Dataset( {'means':means, 'std_deviations':std_deviations } )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

# ----------------------------------------------------------------------
# WRITE EXAMPLE 3
# ----------------------------------------------------------------------

# One of the advantages of using a dataset is that one can also specify the dimensions
# and coordinates of variables. It may be convenient to have these available in the 
# interface script.

# Create a name for this new variable
name = 'test_normal3'

var_type = 'normal'

# Coordinates
times     = np.array( [1,2,3,4] )
positions = np.array( [1,2,3] )

# Convert coordinates to data arrays
times     = xr.DataArray(times,dims=['time'])
positions = xr.DataArray(positions,dims=['position'])

# Construct variable data arrays which include dimensions and coordinates
means          = xr.DataArray(means,          dims=['time','position'], coords=[times,positions])
std_deviations = xr.DataArray(std_deviations, dims=['time','position'], coords=[times,positions]) 

dataset = xr.Dataset( {'means':means, 'std_deviations':std_deviations } )

my_netcdf.add_variable_from_dataset( name, var_type, dataset )

# ----------------------------------------------------------------------
# WRITE EXAMPLE 4
# ----------------------------------------------------------------------

# Here is an example with a 1D uniform variable using a dictionary. A uniform uncertain
# variable needs lower and upper bounds

# Give our variable a name!
name = 'test_uniform'

# Specify the uncertainty distribution
var_type = 'uniform'

# Make a dictionary of the needed data
lower_bounds = np.random.rand(6) * 0.5 
upper_bounds = np.random.rand(6) * 0.5 + 1.0

variable_dict = { 'lower_bounds' : lower_bounds, 'upper_bounds' : upper_bounds }

my_netcdf.add_variable_from_dict( name, var_type, variable_dict )

# ----------------------------------------------------------------------
# WRITE EXAMPLE 5
# ----------------------------------------------------------------------

# Here is an example with a 3D expo variable using a dataset. An exponential uncertain
# variable only needs one parameter named betas

# Give our variable a name!
name = 'test_exponential'

# Specify the uncertainty distribution
var_type = 'exponential'

# Make a dictionary of the needed data
betas = np.random.rand(5,3,2)

# Coordinates
x = np.random.rand(5)
y = np.random.rand(3)
z = np.random.rand(2)

# Convert coordinates to data arrays
x = xr.DataArray(x,dims=['x'])
y = xr.DataArray(y,dims=['y'])
z = xr.DataArray(z,dims=['z'])

# Convert betas to a data array
betas = xr.DataArray(betas, dims=['x','y','z'], coords=[x,y,z]) 

dataset = xr.Dataset( {'betas':betas } )

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

# Create a new instance of the netcdf file 
my_netcdf2 = DakotaFile()

filename = 'DAKOTA.nc'
my_netcdf2.read(filename)

# ----------------------------------------------------------------------
# READ EXAMPLE 1
# ----------------------------------------------------------------------

# We can read one of the variables in the netcdf file back into a dictionary of data
# We shall read test_normal2 which was originally written as a dataset

variable_dict = my_netcdf2.get_variable_as_dict('test_normal2')

print('Read Example 1:')
print()

for key, var in variable_dict.items():

    print( key+':' )
    print( type(var) )
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

dataset = my_netcdf2.get_variable_as_dataset('test_exponential')

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

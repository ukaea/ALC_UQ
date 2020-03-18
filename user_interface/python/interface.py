#-*-Python-*-
# Created by buchanj at 19 Aug 2019  13:37

"""
This script is the interface script called by DAKOTA. It reads the DAKOTA
parameters file and writes the varied data back to a copy of the
user input file which can then be passed to the simulation code.

Once the simulation code has executed it recovers the output file, writes a
dummy DAKOTA response file and exits.
"""
import dakota.interfacing as di
import xarray as xr
import numpy as np
import os
import sys

from dakota_file import DakotaFile
from copy import deepcopy
from definitions import *

# Set a default value for the iteration number
iteration = -1

try:

    # Get input file name and type
    if len(sys.argv) < 5:
        print( 'ERROR: Insufficient number of arguments passed to function!')
        print( 'Interface.py expects : parameters file, results file, input file name, input file type')
        raise Exception 

    file_name = sys.argv[3]
    file_type = sys.argv[4]

    # Get DAKOTA parameters
    params, results = di.read_parameters_file()
    
    # Get Iteration number
    iteration = params.eval_num

    # Read original user input file
    # If it is a netcdf We will append the values drawn from each distribution to the original datasets
    # If it is a csv we will simply make a new csv with a single column of varied data values

    user_file = DakotaFile( file_type=file_type )
    user_file.read( file_name )

    # Loop over uncertain variables and reconstruct data arrays
    for key in user_file.uncertain.keys():

        # Get the dataset for this variable
        dataset = user_file.get_variable_as_dataset(key)

        # Get the type of this variable
        var_type = dataset.attrs['type']

        # Get one of the required entries
        var_name = allowed_variable_types[var_type]['required'][0]
        
        var = dataset[var_name]

        # Add new values variable to data array
        dataset['values'] = deepcopy(var)

        if var_type != 'scan_correlated':

            # Get size and shape of the data array
            size  = var.size
            shape = var.shape

            data  = np.zeros( size )

            for i in range( size ):
                
                dakota_var = key+'_'+str(i)
                data[i]    = params[dakota_var]

            values_data = data.reshape( shape )

        else:

            scale_factor = params[key]

            lower_bounds = dataset.data_vars['lower_bounds']
            upper_bounds = dataset.data_vars['upper_bounds']

            values_data = lower_bounds.data + scale_factor * ( upper_bounds.data - lower_bounds.data )

        # Add data to values data array
        dataset.data_vars['values'].data = values_data

    # Remove input file in run directory
    os.system( 'rm ' + file_name )

    # Write new input file
    user_file.write( file_name )

except Exception as inst:

    print('======================================')
    print('ITERATION '+str(iteration)+' FAILED!')
    print()
    print(inst)

    results.fail()
    results.write()

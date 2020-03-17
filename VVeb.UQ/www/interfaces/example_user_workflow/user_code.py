# Include dakota folder
import sys
sys.path.insert(1, '/dakota_utils/')

import numpy as np
import xarray as xr
import exceptions
from dakota_file import DakotaFile

# Create a new instance of the 
my_netcdf = DakotaFile()

filename = 'DAKOTA.nc'
my_netcdf.read(filename)

# We can read one of the variables in the netcdf file back into a dictionary of data
# We shall read test_normal2 which was originally written as a dataset

variable_dict = my_netcdf.get_variable_as_dict('test_normal2')

if 'values' in variable_dict.keys():

    values = variable_dict['values']
    results = values.sum()
    
    file_out = open('DAKOTA_OUTPUT.dat','w')
    file_out.write('Sum of values is:')
    file_out.write(str(results))
    file_out.close()

else:

    print('ERROR: values entry missing from variable dict!')
    raise Exception

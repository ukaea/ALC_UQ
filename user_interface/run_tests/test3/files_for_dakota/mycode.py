import numpy as np
import xarray as xr
import exceptions
from dakota_file import DakotaFile

my_netcdf = DakotaFile()

filename = 'DAKOTA.nc'
my_netcdf.read(filename)

variable_dict1 = my_netcdf.get_variable_as_dict('test_scan1')
variable_dict2 = my_netcdf.get_variable_as_dict('test_scan2')
variable_dict3 = my_netcdf.get_variable_as_dict('test_scan3')

file_out = open('DAKOTA_OUTPUT.dat','w')

file_out.write('test_scan1:\n')

values = variable_dict1['values']
file_out.write( str(values[0])+' '+str(values[1])+'\n' )

values = variable_dict2['values']
file_out.write( str(values)+'\n' )

values = variable_dict3['values']
file_out.write( str(values)+'\n' )

file_out.close()
    

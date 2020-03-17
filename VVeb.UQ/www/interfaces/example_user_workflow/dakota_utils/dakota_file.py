# A class for interacting with the DAKOTA user input file

# NETCDF FILES ----------------------------------------------------------------
# The netcdf file is expected to have a group for each variable. 
# The groups should contain an attribute 'type' specifying the uncertainty type
# as well as variables corresponding to the required dakota inputs for that type

# These groups are read in as xarray Datasets and stored in a dictionary
#------------------------------------------------------------------------------

# At present the system is set up not to return outputs to DAKOTA but to collate the 
# outputs of the code for each iteration manually. Consequenty it is not necessary to know
# what outputs are expected a priori and only 1 scalar response function is declared.
# If this changes, an output group could be added to this file with empty data.
# So long as the dimensions are known this can be used to declare response functions. 

import os
import numpy as np
import xarray as xr
from netCDF4 import Dataset
from exceptions import *
from definitions import *

class DakotaFile:

    def __init__(self):

        # Dictionary of uncertain variables
        self.uncertain = {}

        # This will contain the DAKOTA run settings
        # These will be stored as attributes of the root group of the netcdf file
        # Consequently this should be a dataset with attributes
        self.settings = None

    # Check that the data contained in the class is consistent
    def check(self):

        scan_vars = [ 'scan', 'scan_correlated' ]

        is_scan = False
        is_mc   = False

        for key, dataset in self.uncertain.items():

            if dataset.attrs['type'] in scan_vars:
                is_scan = True
            else:
                is_mc = True

        if is_scan and is_mc:
            raise FileConsistencyError('Both sampling and parameter scan variables are present.')

        if ( not is_scan ) and ( not is_mc ):
            raise FileConsistencyError('Neither sampling or parameter scan variables are present.')

        if is_mc:

            if self.settings is None:
                raise FileConsistencyError('Sampling run configuration data is missing.\n' \
                                           +'Please use add_settings to add run confuration settings.')

            if 'samples' not in self.settings.attrs:
                raise FileConsistencyError('Run configuration data should at least specify ' \
                                           +'the number of samples to produce.')

    # Top level read and write functions - for now just wrappers to read_netcdf and write_netcdf ---

    def read(self, filename, file_format='netcdf' ):

        if file_format.lower() == 'netcdf':
            self.read_netcdf(filename)
        else:
            raise FileConsistencyError('Unknown File Format Selected.')

    def write(self, filename, file_format='netcdf'):

        if file_format.lower() == 'netcdf':
            self.write_netcdf(filename)
        else:
            raise FileConsistencyError('Unknown File Format Selected.')

    # Tools for reading and writing NetCDF files ---------------------------------------------------

    # Read a netcdf file in the expected format
    def read_netcdf(self, filename):

        try:
            root_group = Dataset(filename)
        except:
            print('ERROR: Could not read input netCDF file : '+filename)
            raise

        # Settings stored as attributes of the root group
        self.settings = xr.open_dataset(filename)

        # Read variable datasets into dictionaries
        for key in root_group.groups.keys():

            self.uncertain[key] = xr.open_dataset(filename, group=key)

        root_group.close()

    # Writes a netcdf file in the expected format using the datasets stored in the class
    def write_netcdf(self, filename):

        # First check that the data is consistent
        self.check()

        # Remove the file if it already exists
        if os.path.isfile(filename):
            os.remove(filename)

        if self.settings is not None:
            self.settings.to_netcdf(filename, mode='w')

        for key in self.uncertain.keys():

            if os.path.isfile(filename):
                self.uncertain[key].to_netcdf(filename, group=key, mode='a')
            else:
                self.uncertain[key].to_netcdf(filename, group=key, mode='w')

    # ----------------------------------------------------------------------------------------------

    # Write variables blocks to dakota - dakotafile is an instance of the dakota class
    def write_dakota_input(self, dakotafile):

        # First check that the data is consistent
        self.check()

        # Add uncertain variables
        for key in self.uncertain.keys():

            dakotafile.add_variable(key,self.uncertain[key])

        # Update settings 
        if self.settings is not None:
            dakotafile.update_settings(self.settings)

    # Write output variables to dakota responses object
    # This assumes the variable names are of the form 'varname_index'
    def write_dakota_output(self,results):

        # Results.responses() yields the Response objects.
        for i, r in enumerate(results.responses()):

            if not r.asv.function:
                continue

            # Signal name
            signal = results.descriptors[i]

            # Need to separate out key and index
            words = signal.split('_')
            key = '_'.join(words[:-1])
    
            try:
                index = int(words[-1])-1
            except:
                raise DakotaResultsError("Output variable "+signal+" does not conform to 'varname_index' format")
                
            if key not in self.uncertain or index >= len( self.uncertain[key].data.flatten() ):
                raise DakotaResultsError('Cannot find required signal '+signal)
                
            # This should also work for profiles - it just treats the profile as a 1D array.
            r.function = self.uncertain[key].data.flatten()[index]

    # Tools for preparing a new DAKOTA user input file from scratch ======================================================

    # Pass a dictionary of signals to be formed into a dataset

    # var_type is the distribution the signal is to be drawn from (e.g. normal, lognormal..)
    # name is the name of the variable - This will be the name of a group in the netcdf file
    # variable_dict is a dictionary of numpy arrays for the required/optional data for that uncertainty type (means, std_deviations etc)

    def add_variable_from_dict( self, name, var_type, variable_dict ):

        # Check variable with this name not already in file
        if name in self.uncertain:
            raise VariableError( 'Variable '+name+' is already present in the file!')

        # Check uncertainty type is valid
        if var_type not in allowed_variable_types:
            raise VariableError('Unknown uncertain variable type: '+var_type+' for variable '+name)

        data_arrays = {}

        # Check variables in dictionary are known and have correct properties

        shape = None
        for key, var in variable_dict.items():

            if not isinstance( var, np.ndarray ):
                raise VariableError('Variable '+name+':'+key+' is not a numpy ndarray.')
 
            if not (key in allowed_variable_types[var_type]['required'] or \
                    key in allowed_variable_types[var_type]['optional'] ):
                raise VariableError( key+' is not a required or optional variable for uncertainty type '+var_type)

            if shape is not None and var.shape != shape:
                raise VariableError( 'Variable '+name+' does not have consistently shaped data')
            shape = var.shape

            da = xr.DataArray(var)
            data_arrays[key] = da

        # Check all required variables are present
        for key in allowed_variable_types[var_type]['required']:

            if key not in data_arrays:
                raise VariableError('Required variable '+key+' for uncertainty type '+var_type+' not present in '+name+'.')

        self.uncertain[name] = xr.Dataset( data_arrays, attrs={'type':var_type} )

    def get_variable_as_dict( self, name ):

        dataset = self.uncertain[name]

        data_arrays = {}
        for key in dataset:

            data_arrays[key] = np.array(dataset[key].data)

        return data_arrays

    def add_variable_from_dataset( self, name, var_type, dataset ):

        # Check variable with this name not already in file
        if name in self.uncertain:
            raise VariableError( 'Variable '+name+' is already present in the file!')

        # Check uncertainty type is valid
        if var_type not in allowed_variable_types:
            raise VariableError('Unknown uncertain variable type: '+var_type+' for variable '+name)

        dims = None
        for key in dataset:
 
            if not (key in allowed_variable_types[var_type]['required'] or \
                    key in allowed_variable_types[var_type]['optional'] ):
                raise VariableError( key+' is not a required or optional variable for uncertainty type '+var_type)

            if dims is not None and dataset[key].dims != dims:
                raise VariableError( 'Variable '+name+' does not have consistent dimensions')
            dims = dataset[key].dims

        dataset.attrs['type'] = var_type
        self.uncertain[name] = dataset

    def get_variable_as_dataset( self, name ):

        return self.uncertain[name]
    
    def add_settings( self, settings ):

        if not isinstance( settings, dict ):
            raise SettingsError('Settings object passed to add_settings should be a dictionary of DAKOTA settings and values.')

        if self.settings is None:
            self.settings = xr.Dataset()

        for key, value in settings.items():

            if key in allowed_settings:
                self.settings.attrs[key] = value
            else:
                raise SettingsError('Unknown DAKOTA setting passed to add_settings.')

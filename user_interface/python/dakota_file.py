# A class for interacting with the DAKOTA user input file

# NETCDF FILES ----------------------------------------------------------------
# The netcdf file is expected to have a group for each variable. 
# The groups should contain an attribute 'type' specifying the uncertainty type
# as well as variables corresponding to the required dakota inputs for that type
#
# These groups are read in as xarray Datasets and stored in a dictionary
#------------------------------------------------------------------------------

# CSV FILES -------------------------------------------------------------------
# The CSV file is expected to have a top line containing either MC or SCAN to
# indicate the type of run to be performed. If performing a monte-carlo run (MC)
# the second line must contain the number of samples to run and can optionally then 
# include the random number seed and the sampling type: lhs (default) or mc.
# Following this the file must contain 2 columns containing the means and standard
# deviations of a set of normal uncertain variables.
# For a parameter scan run the file should contain 3 columns of lower and upper bounds
# and numbers of partitions to use.
# -----------------------------------------------------------------------------

# At present the system is set up not to return outputs to DAKOTA but to collate the 
# outputs of the code for each iteration manually. Consequenty it is not necessary to know
# what outputs are expected a priori and only 1 scalar response function is declared.
# If this changes, an output group could be added to this file with empty data.
# So long as the dimensions are known this can be used to declare response functions. 

import os
import numpy as np
import xarray as xr
import csv
from netCDF4 import Dataset
from exceptions import *
from definitions import *

class DakotaFile:

    def __init__(self, file_type='netcdf'):

        # Dictionary of uncertain variables
        self.uncertain = {}

        # This will contain the DAKOTA run settings
        # These will be stored as attributes of the root group of the netcdf file
        # Consequently this should be a dataset with attributes
        self.settings = None

        self.file_type = file_type

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

            if 'sample_type' not in self.settings.attrs:
                print('No sample type set. Defaulting to Latin Hypercube Sampling.')
                self.settings.attrs['sample_type'] = 'lhs'

            if 'samples' not in self.settings.attrs and self.settings.attrs['sample_type'] is not 'pce':
                raise FileConsistencyError('Run configuration data should at least specify ' \
                                           +'the number of samples to produce.')

            if 'poly_order' not in self.settings.attrs and self.settings.attrs['sample_type'] is 'pce':
                print('No polynomial order set for polynomial chaos expansion. Defaulting to 4')
                self.settings.attrs['poly_order'] = 4

    # Top level read and write functions - for now just wrappers to read_netcdf and write_netcdf ---

    def read(self, filename):

        if self.file_type.lower() == 'netcdf' or self.file_type.lower() == 'n':
            self.read_netcdf(filename)
        elif self.file_type.lower() == 'csv' or self.file_type.lower() == 'c':
            self.read_csv(filename)
        else:
            raise FileConsistencyError('Unknown File Format Selected.')

    def write(self, filename):

        if self.file_type.lower() == 'netcdf' or self.file_type.lower() == 'n':
            self.write_netcdf(filename)
        elif self.file_type.lower() == 'csv' or self.file_type.lower() == 'c':
            self.write_csv(filename)
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

    # Tools for reading and writing CSV files ------------------------------------------------------

    # Read a CSV file. The first line should be either MC or SCAN indicating the type of run to be performed.
    # If the run type is MC (for monte-carlo sampling) the second line should contain the number of samples to be run
    # and then optionally the random number seed to use and the sampling type to employ. 
    # The other lines are all data lines. If using MC there should be two columns for data and errors, if performing
    # paraneter scans there should be 3 columns for lower bounds, upper bounds and partitions. 

    def read_csv(self, filename):

        # Arrays for use when performing Monte-Carlo Sampling
        means = []
        sds   = []

        # Arrays for use when performing parameter scans
        lower_bounds = []
        upper_bounds = []
        partitions   = []

        try:

            with open(filename) as csv_file:
                
                csv_reader = csv.reader(csv_file,delimiter=',')

                row_count = 0

                for row in csv_reader:

                    # Try and protect against empty lines and whitespace
                    if len(row) == 0 or ( len(row) == 1 and row[0].strip() == '' ):
                        continue

                    if row_count == 0:
                        
                        # Monte Carlo / Scan
                        run_type = row[0].strip().upper()

                        if run_type != 'MC' and run_type != 'SCAN':
                            raise CSVError('Unknown run type given. Allowed types are MC for pure monte-carlo \n \
                            sampling or SCAN for parameter scans.')

                    elif row_count == 1 and run_type == 'MC':

                        # Settings Line
                        settings = {}
                        
                        # Should at least contain number of samples
                        settings['samples'] = int(row[0])

                        # May contain random number seed
                        if len(row) > 1:
                            settings['seed'] = int(row[1])
                        else:
                            settings['seed'] = 1

                        # May specify sampling type
                        if len(row) > 2:
                            settings['sample_type'] = row[2].strip().lower()
                        else:
                            settings['sample_type'] = 'lhs'

                        # If using PCE sampling interpret the samples variable as a polynomial order instead of the number of samples
                        # Slightly hacky but the easiest way to support PCE in the CSV format. In this case the seed variable
                        # is redundant and can be set to any value
                        if settings['sample_type'] == 'pce':
                            settings['poly_order'] = settings['samples']
                            settings['samples']    = 0

                        self.add_settings( settings )

                    elif run_type.upper() == 'MC':

                        # Pure MC sampling

                        if len(row) != 2:
                            raise CSVError('Incorrectly formatted line in CSV file. Sampling files must have 2 columns.')
                            
                        means.append( float(row[0]) )
                        sds.append(   float(row[1]) )

                    else:
                        
                        # Parameter Scan

                        if len(row) != 3:
                            raise CSVError('Incorrectly formatted line in CSV file. Parameter scan files must have 3 columns.')
    
                        lower_bounds.append( float(row[0]) )
                        upper_bounds.append( float(row[1]) )
                        partitions.append(     int(row[2]) )

                    row_count = row_count + 1

        except:

            print('ERROR: Could not read input CSV file : '+filename)
            raise

        if run_type.upper() == 'MC':

            variable_dict = { 'means' : np.array(means), 'std_deviations' : np.array(sds) }
            
            self.add_variable_from_dict( 'vars', 'normal', variable_dict )

        else:

            variable_dict = { 'lower_bounds' : np.array(lower_bounds), 
                              'upper_bounds' : np.array(upper_bounds), 
                              'partitions'   : np.array(partitions) }
            
            self.add_variable_from_dict( 'vars', 'scan', variable_dict )


    # Writes a csv file of varied data in the correct order
    def write_csv(self, filename):

        # Remove the file if it already exists
        if os.path.isfile(filename):
            os.remove(filename)

        with open(filename, mode='w') as csv_file:

            if 'vars' in self.uncertain:

                # Write out variables
                for value in list( self.uncertain['vars']['values'].data ):
                        
                    csv_file.write( str(value)+'\n' )

            else:

                raise CSVError('Variable data missing from output.')

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
                try:
                    var = np.array(var)
                except:
                    raise VariableError('Variable '+name+':'+key+' is not a numpy ndarray and cannot be turned into one.')
 
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

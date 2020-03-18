import numpy as np
import xarray as xr
from container import Container
from definitions import *
from exceptions import *

# Defines a DAKOTA class which is used to write a DAKOTA input file

# The structure of the file is captured by declaring each line as a container
# with a parent line and children. This tree structure allows each line to know
# how indented in the file it should be.

class DakotaClass:

    def __init__(self):

        # Construct template input file =============================================
        dakota = Container('dakota')

        # Model block ---------------------------------
        model  = Container('model', dakota)
        single = Container('single', model)

        # Environment block ---------------------------
        env      = Container('environment', dakota)
        tab      = Container('tabular_data', env)
        tab_data = Container('tabular_data_file', tab, attribute="'DAKOTA.dat'")

        # Method block --------------------------------
        method   = Container('method', dakota)

        # Interface block -----------------------------
        interface = Container('interface', dakota)
        analysis  = Container('analysis_drivers', interface, attribute="'python interface.py'")
        failure   = Container('failure_capture', analysis)
        recover   = Container('recover', failure, attribute=1)
        fork      = Container('fork', analysis)
        params    = Container('parameters_file', fork, attribute="'dakota_params'")
        results   = Container('results_file', fork, attribute="'dakota_results'")
        work_dir  = Container('work_directory', fork)
        named     = Container('named', work_dir, attribute="'workdir_VVebUQ'")
        dir_tag   = Container('directory_tag', work_dir)
        dir_save  = Container('directory_save', work_dir)
        file_save = Container('file_save', work_dir)

        copy_file = "'files_for_dakota/*'"
        copy_file = Container('copy_files', work_dir, attribute=copy_file) # Copy netcdf file into work directory

        asynch    = Container('asynchronous', interface)
        concurcy  = Container('evaluation_concurrency', asynch, attribute=1)

        # Variables block -----------------------------
        variables = Container('variables', dakota)

        # Responses block -----------------------------
        # There is one response function with 0 indicating success and 1 indicating failure
        responses = Container('responses', dakota)
        functions = Container('response_functions', responses, attribute=1, equals=False)
        res_desc  = Container('descriptors', responses, attribute="'Failed'", equals=False)
        gradients = Container('no_gradients', responses)
        hessians  = Container('no_hessians', responses)

        self.dakota = dakota

    # Write the DAKOTA input file based on the DAKOTA class.
    def write_input_file(self, filename):

        handle = open(filename,'w+')
        self.dakota.write_all(handle)
        handle.close()

    # Loop over dataset attributes and update settings based on dataset attributes
    # Only needed when using sampling
    def update_settings(self, dataset):

        # Check if any of the allowed settings are in the dataset. If not return
        if not any( x in allowed_settings for x in dataset.attrs ):
            return

        # Check if needed containers are present
        sampling = self.dakota.get('sampling')

        # Add default MC sampling containers
        if sampling is None:
            method   = self.dakota.get('method')
            sampling = Container('sampling', method)
            stype    = Container('sample_type', sampling, attribute='lhs', equals=False)
            samples  = Container('samples', sampling, attribute=0)
            seed     = Container('seed', sampling, attribute=1)

        for key, value in dataset.attrs.items():

            if key in allowed_settings:

                self.dakota.set_attribute(key,value)

    # Member functions for adding different kinds of response function ---------------------------------------------
    def add_field_response(self, N, name):

        responses = self.dakota.get('responses')

        if responses.get_attribute('response_functions') == 0:

            # Add required children
            responses.set_attribute('response_functions',1)
            functions   = responses.get('response_functions')
            descriptors = Container( 'descriptors',     responses, attribute=["'" + name + "'"], equals=False )
            fields      = Container( 'field_responses', functions, attribute=1,                  equals=False )
            lengths     = Container( 'lengths',         fields,    attribute=[N],                equals=False )

        else:

            responses.append_attribute('descriptors', "'"+name+"'")
            responses.set_attribute('response_functions', responses.get_attribute('response_functions')+1 )
            responses.set_attribute('field_responses',    responses.get_attribute('field_responses')+1 )
            responses.append_attribute('lengths', N)

    # TOOLS FOR ADDING VARIABLES TO DAKOTA INPUT FILE ================================================================

    # Checks that information in a new variable is sensible
    def check_variable(self, name, dataset):

        # Check object passed is an xarray dataset
        if not isinstance(dataset,xr.Dataset):
            raise DatasetError('Object passed to dakota_class:add_variable is not an xarray.Dataset.')
        
        # Check attribute specifying type of uncertainty is present
        if 'type' not in dataset.attrs:
            raise DatasetError('Dataset passed to dakota_class:add_variable has no type attribute.')

        uncertainty_type = dataset.attrs['type'].lower()

        # Check type of variable is supported
        if uncertainty_type not in allowed_variable_types:
            raise DatasetError('Dataset passed to dakota_class:add_variable has unknown uncertainty type.') 

        size = None
        for key in allowed_variable_types[uncertainty_type]['required']:
               
            # Check all required data is present
            if key not in dataset:
                raise DatasetError('Dataset is missing required data '+str(key)+' for variable '+str(name) )

            var_data = dataset[key].data

            if var_data.size == 0:
                raise DatasetError('Dataset is missing required data '+str(key)+' for variable '+str(name) )

            # Check all provided data has the same size
            if size is not None and var_data.size != size:
                raise DatasetError('Data for variable '+str(name)+' does not all have the same size.')
            size = var_data.size

            # Check provided data does not contain NaNs
            if size > 1:
                val_nan  = [ np.isnan(xv) for xv in var_data ]
            else:
                val_nan = np.isnan(var_data)

            if np.any(val_nan):
                raise DatasetError( 'NAN values detected in data for variable '+str(name)+'('+key+')' )

        # If performing a corellated scan all partitions entries must be the same as the data will be varied together
        if uncertainty_type == 'scan_correlated':
            
            partitions = dataset['partitions'].data

            equal = np.all( [ x == partitions[0] for x in partitions ] )
            if not equal:
                 raise DatasetError('For correlated variables the number of partitions must be the same. ['+name+']' )

    # Top level function for adding a new uncertain variable based on a dataset
    # Dataset is an xarray dataset corresponding to a single uncertain variable
    def add_variable(self, name, dataset):
        
        # Check dataset is consistent
        self.check_variable(name, dataset)

        # Get the uncertainty type and call the appropriate function below
        uncertainty_type = dataset.attrs['type'].lower()

        if uncertainty_type == 'scan_correlated':
            self.add_correlated_scan_variable(name, dataset)

        elif uncertainty_type == 'scan':
            self.add_scan_variable(name, dataset)

        elif uncertainty_type == 'lognormal':
            self.add_lognormal_variable(name, dataset)

        else:
            self.add_common_variable(name, dataset)

    # Functions for adding specific types of variables ------------------------------------------------

    # Just a helper function for constructing commonly used data
    def get_types_and_descriptions(self, name, dataset):

        uncertainty_type        = dataset.attrs['type'].lower()
        dakota_uncertainty_type = allowed_variable_types[uncertainty_type]['name']

        nitems = dataset[ allowed_variable_types[uncertainty_type]['required'][0] ].data.size
        description = ["'" + name + '_' + str(x) + "'" for x in range(nitems) ]

        return uncertainty_type, dakota_uncertainty_type, nitems, description

    # Function for adding a new uncertain variable based on a dataset
    # This is the function for 'common' variables that follow the simple scheme of having a
    # set of variables under a block with the name of the variable type
    def add_common_variable(self, name, dataset):

        # Get the uncertainty type and the full DAKOTA name for it, number of entries and descriptions
        uncertainty_type, dakota_uncertainty_type, nitems, description = \
            self.get_types_and_descriptions(name,dataset)

        # Check if there are entries for this type of uncertain variable already
        uncertainty_block = self.dakota.get(dakota_uncertainty_type)

        new_block = False
        if uncertainty_block is None:

            new_block         = True
            variables         = self.dakota.get('variables')
            uncertainty_block = Container( dakota_uncertainty_type, variables, attribute=0 )

        for key in allowed_variable_types[uncertainty_type]['required']:

            var_data = dataset[key].data               

            if new_block:
                block = Container( key, uncertainty_block, attribute=list(var_data.flatten()), equals=False)
            else:
                uncertainty_block.append_attribute( key, list(var_data.flatten()) )

        uncertainty_block.attribute += nitems

        if new_block:
            desc = Container( 'descriptors', uncertainty_block, attribute=description, equals=False)
        else:
            uncertainty_block.append_attribute('descriptors',   description)

    # Function for adding a new lognormal uncertain variable based on a dataset
    # Lognormal is awkward as std_deviations is added as an entry underneath means rather than next to it.
    # Consequently this variable type is handle manually
    def add_lognormal_variable(self, name, dataset):

        # Get the uncertainty type and the full DAKOTA name for it, number of entries and descriptions
        uncertainty_type, dakota_uncertainty_type, nitems, description = \
            self.get_types_and_descriptions(name,dataset)

        # Check if there are entries for this type of uncertain variable already
        uncertainty_block = self.dakota.get(dakota_uncertainty_type)

        if uncertainty_block is None:

            variables         = self.dakota.get('variables')
            uncertainty_block = Container( dakota_uncertainty_type, variables, attribute=nitems )

            var_data = list( dataset['means'].data.flatten() )
            means             = Container( 'means', uncertainty_block, attribute=var_data, equals=False )

            var_data = list( dataset['std_deviations'].data.flatten() )
            sds               = Container( 'std_deviations', means, attribute=var_data, equals=False )

            desc              = Container( 'descriptors', uncertainty_block, attribute=description, equals=False)

        else:

            uncertainty_block.attribute += nitems

            var_data = list( dataset['means'].data.flatten() )
            uncertainty_block.append_attribute( 'means', var_data )

            var_data = list( dataset['std_deviations'].data.flatten() )
            uncertainty_block.append_attribute( 'std_deviations', var_data )

            uncertainty_block.append_attribute('descriptors',   description)

    # Add a parameter scan variables. Again this does not fit in the simple schema
    # as the partitions variable belongs in the method block not the variables block
    def add_scan_variable(self, name, dataset):

        # Get the uncertainty type and the full DAKOTA name for it, number of entries and descriptions
        uncertainty_type, dakota_uncertainty_type, nitems, description = \
            self.get_types_and_descriptions(name,dataset)

        # First handle the partitions section manually -------------------------------------
        partitions = self.dakota.get('partitions')

        var_data = list( dataset['partitions'].data.flatten() )

        if partitions is None:
            method     = self.dakota.get('method')
            multidim   = Container( 'multidim_parameter_study', method, equals=False )
            partitions = Container( 'partitions', multidim, attribute=var_data )
        else:
            partitions.append_attribute( 'partitions', var_data )

        # Now handle the variable data section ---------------------------------------------

        # Check if there are entries for this type of uncertain variable already
        uncertainty_block = self.dakota.get(dakota_uncertainty_type)

        new_block = False
        if uncertainty_block is None:

            new_block         = True
            variables         = self.dakota.get('variables')
            uncertainty_block = Container( dakota_uncertainty_type, variables, attribute=0 )

        for key in allowed_variable_types[uncertainty_type]['required']:

            if key == 'partitions':
                continue 

            var_data = dataset[key].data               

            if new_block:
                block = Container( key, uncertainty_block, attribute=list(var_data.flatten()), equals=False)
            else:
                uncertainty_block.append_attribute( key, list(var_data.flatten()) )

        uncertainty_block.attribute += nitems

        if new_block:
            desc = Container( 'descriptors', uncertainty_block, attribute=description, equals=False)
        else:
            uncertainty_block.append_attribute('descriptors',   description)

    # Add a correlated parameter scan variable.
    # As the variables are all varied in tandem only a single DAKOTA scan variable is needed
    def add_correlated_scan_variable(self, name, dataset):

        # Get the uncertainty type and the full DAKOTA name for it, number of entries and descriptions
        uncertainty_type, dakota_uncertainty_type, nitems, description = \
            self.get_types_and_descriptions(name,dataset)

        # First handle the partitions section manually -------------------------------------
        partitions = self.dakota.get('partitions')

        # These should all be the same - check_variable ensures this
        var_data = list( dataset['partitions'].data.flatten() )

        if partitions is None:
            method     = self.dakota.get('method')
            multidim   = Container( 'multidim_parameter_study', method, equals=False )
            partitions = Container( 'partitions', multidim, attribute=[ var_data[0] ] )
        else:
            partitions.append_attribute( 'partitions', var_data[0] )

        # Now handle the variable data section ---------------------------------------------

        # For a correlated scan we simply add a single variable that ranges between 0 and 1

        # Check if there are entries for this type of uncertain variable already
        uncertainty_block = self.dakota.get(dakota_uncertainty_type)

        if uncertainty_block is None:

            variables         = self.dakota.get('variables')
            uncertainty_block = Container( dakota_uncertainty_type, variables, attribute=1 )

            lower_bound       = Container( 'lower_bounds', uncertainty_block, attribute=[0.0], equals=False)
            upper_bound       = Container( 'upper_bounds', uncertainty_block, attribute=[1.0], equals=False)

            desc = Container( 'descriptors', uncertainty_block, attribute=["'"+name+"'"], equals=False)
        
        else:

            uncertainty_block.attribute += 1
            uncertainty_block.append_attribute( 'lower_bounds', [0.0] )
            uncertainty_block.append_attribute( 'upper_bounds', [1.0] )
            uncertainty_block.append_attribute( 'descriptors', ["'"+name+"'"] )

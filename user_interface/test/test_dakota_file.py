# Class of test functions for python scripts needed to run DAKOTA

from dakota_file import DakotaFile
from exceptions import *
import numpy as np
import xarray as xr
import unittest
import os
import csv

# Store some test data

# Settings
settings = { 'samples' : 50 }

# Coordinates
times = np.array( [1,2,3,4] )
times = xr.DataArray(times, dims=['time'])

positions = np.array( [1,2,3] )
positions = xr.DataArray(positions, dims=['position'])

labels = np.array( [ 'a', 'b', 'c', 'd', 'e', 'f' ] )
labels = xr.DataArray(labels, dims=['labels'])

# Data for normal uncertain variable
means = np.random.rand(4,3)
means = xr.DataArray(means, coords=[times,positions], dims=['time','position'])

sds = np.random.rand(4,3)
sds = xr.DataArray(sds,coords=[times,positions], dims=['time','position']) 

# Data for exponential uncertain variable
betas = np.random.rand(4,3)
betas = xr.DataArray(betas, coords=[times,positions], dims=['time','position'])

initial_points = np.random.rand(4,3)
initial_points = xr.DataArray(initial_points)

# Data for lognormal uncertain variable
lognormal_means = np.random.rand(6)
lognormal_means = xr.DataArray(lognormal_means, coords=[labels], dims=['labels'])

lognormal_sds = np.random.rand(6)
lognormal_sds = xr.DataArray(lognormal_sds, coords=[labels], dims=['labels'])

lower_bounds = np.random.rand(6)
lower_bounds = xr.DataArray(lower_bounds, coords=[labels], dims=['labels'])

upper_bounds = np.random.rand(6)
upper_bounds = xr.DataArray(upper_bounds, coords=[labels], dims=['labels'])

# Data for continuous design variable
partitions  = np.array( [3,4,5,3,4,5] )
partitions  = xr.DataArray(partitions, coords=[labels], dims=['labels'])

lower_bounds2 = np.random.rand(4,6)
lower_bounds2 = xr.DataArray(lower_bounds2, coords=[times, labels], dims=['time', 'labels'])

upper_bounds2 = np.random.rand(4,6)
upper_bounds2 = xr.DataArray(upper_bounds2, coords=[times, labels], dims=['time', 'labels'])

partitions2 = np.full( (4,6), 4 )
partitions2 = xr.DataArray(partitions2, coords=[times, labels], dims=['time', 'labels'])

# CSV tests -----------------------------------

csv_mc_correct=\
'''MC
4000, 23825
1, 0.12
3, 0.64
7, 0.74
0.32, 0.001'''

csv_mc_incorrect=\
'''MC
4000, 23825
1, 0.12
3
7, 0.74
0.32, 0.001'''

csv_no_type_fails=\
'''1, 0.12
3, 0.24
7, 0.74
0.32, 0.001'''

csv_scan_correct=\
'''SCAN
1,       4, 4
3,    6.82, 6
7,     837, 5 
0.32, 0.74, 47'''

csv_scan_incorrect=\
'''SCAN
1,       4, 4
3,    6.82
7,     837, 5 
0.32, 0.74, 47'''

class TestDakotaFile(unittest.TestCase):

    # Create a simple test netcdf with some data
    def test_write_a_netcdf(self):
        
        test_netcdf = DakotaFile()
        
        # Add some settings
        test_netcdf.add_settings( settings )
        
        test_netcdf.uncertain['test'] = xr.Dataset( {'means':means, 'std_deviations':sds }, attrs={'type':'normal'} )
        
        test_netcdf.write('test.nc')
        
        self.assertTrue( os.path.isfile('test.nc') )
    
    # Attempt to read first test netcdf and check data is correct
    def test_read_a_netcdf(self):

        # Write a file first
        test_netcdf = DakotaFile()
        
        # Add some settings
        test_netcdf.add_settings( settings )
    
        # Add a variable
        test_netcdf.uncertain['test'] = xr.Dataset( {'means':means, 'std_deviations':sds }, attrs={'type':'normal'} )
        
        # Write the file
        test_netcdf.write('test.nc')
    
        # Read the file into a new instance
        test_netcdf = DakotaFile()
        test_netcdf.read('test.nc')
        
        self.assertTrue( 'test' in test_netcdf.uncertain )
        self.assertEqual( test_netcdf.uncertain['test'].attrs['type'], 'normal' )
        self.assertEqual( np.sum( test_netcdf.uncertain['test'].data_vars['means'] - means ), 0.0 )
        self.assertEqual( np.sum( test_netcdf.uncertain['test'].data_vars['std_deviations'] - sds ), 0.0 )

    # Test the consistency check functionality on a properly configured file with uncertainty data
    def test_check_uncertainty_file(self):

        # Write a file first
        test_netcdf = DakotaFile()
        
        # Add some settings
        test_netcdf.add_settings( settings )
    
        # Add some variables
        test_netcdf.uncertain['test']  = xr.Dataset( {'means':means, 'std_deviations':sds }, 
                                                     attrs={'type':'normal'} )
        test_netcdf.uncertain['test2'] = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds }, 
                                                     attrs={'type':'uniform'} )
        test_netcdf.uncertain['test3'] = xr.Dataset( { 'betas' : betas, 'initial_point': initial_points }, 
                                                     attrs={'type':'exponential'} )

        test_netcdf.check()

    # Test the consistency check functionality on a properly configured file with parameter scan data
    def test_check_scan_file(self):

        # Write a file first
        test_netcdf = DakotaFile()

        # Add some variables
        test_netcdf.uncertain['test']  = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds, 
                                                      'partitions':partitions }, attrs={'type':'scan'} )

        test_netcdf.uncertain['test2']  = xr.Dataset( {'lower_bounds':lower_bounds2, 'upper_bounds':upper_bounds2, 
                                                      'partitions':partitions2 }, attrs={'type':'scan'} )

        test_netcdf.check()

    # Tests of tools for user creation of netcdf file ===============================================

    # Test functionality to add variables to a netcdf file from a dictionary
    def test_add_var_from_dict(self):

        test_netcdf = DakotaFile()

        # Add some settings
        test_netcdf.add_settings( settings )
        
        # A normal uncertain variable
        name          = 'test_normal'
        var_type      = 'normal'    
        variable_dict = { 'means' : means.data , 'std_deviations': sds.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
        
        # An exponential uncertain variable
        name          = 'test_exponential'
        var_type      = 'exponential'    
        variable_dict = { 'betas' : betas.data , 'initial_point': initial_points.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
    
        # A lognormal uncertain variable
        name          = 'test_lognormal'
        var_type      = 'lognormal'    
        variable_dict = { 'means' : lognormal_means.data , 'std_deviations': lognormal_sds.data,
                          'lower_bounds': lower_bounds.data, 'upper_bounds' : upper_bounds.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
        
        test_netcdf.write('test2.nc')
        self.assertTrue( os.path.isfile('test2.nc') )
        
        os.remove('test2.nc')

    def test_read_var_as_dict(self):

        test_netcdf = DakotaFile()

        # Add some settings
        test_netcdf.add_settings( settings )
        
        # A normal uncertain variable
        name          = 'test_normal'
        var_type      = 'normal'    
        variable_dict = { 'means' : means.data , 'std_deviations': sds.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
        
        # An exponential uncertain variable
        name          = 'test_exponential'
        var_type      = 'exponential'    
        variable_dict = { 'betas' : betas.data , 'initial_point': initial_points.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
    
        # A lognormal uncertain variable
        name          = 'test_lognormal'
        var_type      = 'lognormal'    
        variable_dict = { 'means' : lognormal_means.data , 'std_deviations': lognormal_sds.data,
                          'lower_bounds': lower_bounds.data, 'upper_bounds' : upper_bounds.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
        test_netcdf.write('test2.nc')

        test_netcdf = DakotaFile()
        test_netcdf.read('test2.nc')
        
        name = 'test_normal'
        variable_dict  = test_netcdf.get_variable_as_dict(name)
        
        self.assertEqual( np.sum( variable_dict['means'] - means ), 0.0 )
        self.assertEqual( np.sum( variable_dict['std_deviations'] - sds ), 0.0 )
        
        name = 'test_exponential'
        variable_dict = test_netcdf.get_variable_as_dict(name)
        
        self.assertEqual( np.sum( variable_dict['betas'] - betas ), 0.0 )
        self.assertEqual( np.sum( variable_dict['initial_point'] - initial_points ), 0.0 )
        
        name = 'test_lognormal'
        variable_dict = test_netcdf.get_variable_as_dict(name)
        
        self.assertEqual( np.sum( variable_dict['means'] - lognormal_means ), 0.0 )
        self.assertEqual( np.sum( variable_dict['lower_bounds'] - lower_bounds ), 0.0 )
        self.assertEqual( np.sum( variable_dict['upper_bounds'] - upper_bounds ), 0.0 )

        os.remove('test2.nc')

    def test_write_var_as_dataset(self):
    
        test_netcdf = DakotaFile()

        # Add some settings
        test_netcdf.add_settings( settings )

        # A uniform uncertain variable
        name     = 'test_uniform'
        var_type = 'uniform'    
        dataset  = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds } )
        
        test_netcdf.add_variable_from_dataset( name, var_type, dataset )
        
        test_netcdf.write('test3.nc')
        self.assertTrue( os.path.isfile('test3.nc') )
        os.remove('test3.nc')

    def test_read_var_as_dataset(self):

        # Write some data
        test_netcdf = DakotaFile()

        # Add some settings
        test_netcdf.add_settings( settings )

        # A uniform uncertain variable
        name     = 'test_uniform'
        var_type = 'uniform'    
        dataset  = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds } )
        
        test_netcdf.add_variable_from_dataset( name, var_type, dataset )
        
        test_netcdf.write('test3.nc')
    
        # Read the data
        test_netcdf = DakotaFile()
        test_netcdf.read('test3.nc')
        
        # A uniform uncertain variable
        name     = 'test_uniform'
        dataset  = test_netcdf.get_variable_as_dataset( name )
        
        self.assertEqual( np.sum( dataset['lower_bounds'] - lower_bounds ), 0.0 )
        self.assertEqual( np.sum( dataset['upper_bounds'] - upper_bounds ), 0.0 )
        
        os.remove('test3.nc')

    def test_mc_csv(self):

        with open('test.csv','w+') as test_file:
            test_file.write(csv_mc_correct)

        test_file = DakotaFile(file_type='csv')
        test_file.read('test.csv')

        self.assertEqual( test_file.settings.attrs['samples'], 4000 )
        self.assertEqual( test_file.settings.attrs['seed'],   23825 )
        self.assertEqual( test_file.uncertain['vars']['means'].data[1], 3 )
        self.assertEqual( test_file.uncertain['vars']['std_deviations'].data[2], 0.74 )

        os.remove('test.csv')

    def test_scan_csv(self):

        with open('test.csv','w+') as test_file:
            test_file.write(csv_scan_correct)

        test_file = DakotaFile(file_type='csv')
        test_file.read('test.csv')

        self.assertEqual( test_file.uncertain['vars']['lower_bounds'].data[1], 3 )
        self.assertEqual( test_file.uncertain['vars']['upper_bounds'].data[2], 837 )
        self.assertEqual( test_file.uncertain['vars']['partitions'].data[3], 47 )

        os.remove('test.csv')

    def test_write_csv(self):

        test_file = DakotaFile(file_type='csv')

        values = np.array([0,1,2,3,4,5])

        data_arrays = {}
        data_arrays['values'] = xr.DataArray(values)
        
        test_file.uncertain['vars'] = xr.Dataset( data_arrays, attrs={'type':'normal'} )

        test_file.write_csv('test.csv')

        with open('test.csv') as csv_file:

            csv_reader = csv.reader(csv_file,delimiter=',')
            row_count = 0

            for row in csv_reader:

                self.assertEqual( int(row[0]), row_count )
                row_count = row_count + 1

        os.remove('test.csv')

#############################################
# FAILURE TESTS
#############################################

    # Test the consistency check functionality on a badly configured file with both uncertainty data
    # and parameter scan data
    def test_check_inconsistent_file(self):

        # Write a file first
        test_netcdf = DakotaFile()
        
        # Add some settings
        test_netcdf.add_settings( settings )
    
        # Add some variables
        test_netcdf.uncertain['test']  = xr.Dataset( {'means':means, 'std_deviations':sds }, 
                                                     attrs={'type':'normal'} )
        test_netcdf.uncertain['test2'] = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds }, 
                                                     attrs={'type':'uniform'} )
        test_netcdf.uncertain['test3'] = xr.Dataset( { 'betas' : betas, 'initial_point': initial_points }, 
                                                     attrs={'type':'exponential'} )

        test_netcdf.uncertain['test4']  = xr.Dataset( {'lower_bounds':lower_bounds, 'upper_bounds':upper_bounds, 
                                                      'partitions':partitions }, attrs={'type':'scan'} )

        test_netcdf.uncertain['test5']  = xr.Dataset( {'lower_bounds':lower_bounds2, 'upper_bounds':upper_bounds2, 
                                                      'partitions':partitions2 }, attrs={'type':'scan'} )

        with self.assertRaises(FileConsistencyError):
            test_netcdf.check()

    def test_mc_file_without_settings(self):

        # Write a file first
        test_netcdf = DakotaFile()
 
        # Add some variables
        test_netcdf.uncertain['test']  = xr.Dataset( {'means':means, 'std_deviations':sds }, 
                                                     attrs={'type':'normal'} )

        with self.assertRaises(FileConsistencyError):
            test_netcdf.check()

    def test_mc_file_without_samples_in_settings(self):

        # Write a file first
        test_netcdf = DakotaFile()
 
        test_settings = { 'sample_type': 'lhs' }

        # Add some settings
        test_netcdf.add_settings( test_settings )

        # Add some variables
        test_netcdf.uncertain['test']  = xr.Dataset( {'means':means, 'std_deviations':sds }, 
                                                     attrs={'type':'normal'} )

        with self.assertRaises(FileConsistencyError):
            test_netcdf.check()

    # Test that adding the same variable twice throws an error
    def test_add_var_from_dict(self):

        test_netcdf = DakotaFile()

        # A normal uncertain variable
        name          = 'test_normal'
        var_type      = 'normal'    
        variable_dict = { 'means' : means.data , 'std_deviations': sds.data }
        
        test_netcdf.add_variable_from_dict( name, var_type, variable_dict )
        
        with self.assertRaises(VariableError):
            test_netcdf.add_variable_from_dict( name, var_type, variable_dict )

    def test_mc_csv_fails(self):

        with open('test.csv','w+') as test_file:
            test_file.write(csv_mc_incorrect)

        test_file = DakotaFile(file_type='csv')

        with self.assertRaises(CSVError):
            test_file.read('test.csv')

        os.remove('test.csv')

    def test_csv_no_type_fails(self):

        with open('test.csv','w+') as test_file:
            test_file.write(csv_no_type_fails)

        test_file = DakotaFile(file_type='csv')

        with self.assertRaises(CSVError):
            test_file.read('test.csv')

        os.remove('test.csv')

    def test_scan_csv_fails(self):

        with open('test.csv','w+') as test_file:
            test_file.write(csv_scan_incorrect)

        test_file = DakotaFile(file_type='csv')

        with self.assertRaises(CSVError):
            test_file.read('test.csv')

        os.remove('test.csv')

    def test_fail_write_csv(self):

        test_file = DakotaFile(file_type='csv')

        dataset1 = xr.Dataset( {'values': np.array([1]) } )
        dataset2 = xr.Dataset( {'values': np.array([2]) } )
        dataset3 = xr.Dataset( {'values': np.array([3]) } )
        
        test_file.add_variable_from_dataset( 'vars_0', 'normal', dataset1 )
        test_file.add_variable_from_dataset( 'vars_1', 'normal', dataset2 )
        test_file.add_variable_from_dataset( 'vars_3', 'normal', dataset3 )

        with self.assertRaises(CSVError):
            test_file.write_csv('test.csv')

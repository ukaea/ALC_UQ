from dakota_class import DakotaClass
from exceptions import *
import unittest
import xarray as xr
import numpy as np
import os

class TestDakotaClass(unittest.TestCase):

    # Try and create an instance of the dakota class
    def test_create_dakota_template(self):

        my_dakota = DakotaClass()
        
        self.assertEqual( my_dakota.dakota.get_attribute('evaluation_concurrency'), 1 )
        self.assertEqual( my_dakota.dakota.get_attribute('response_functions'), 1 )

    def test_add_run_settings(self):

        attrs = { 'sample_type':'sampling', 'seed':54 }
        
        new_settings = xr.Dataset(attrs=attrs)
        
        my_dakota = DakotaClass()
        my_dakota.update_settings(new_settings)
        
        self.assertEqual( my_dakota.dakota.get_attribute('sample_type').strip(), 'sampling' )
        self.assertEqual( my_dakota.dakota.get_attribute('seed'), 54 )

    def test_add_common_variable(self):

        attrs = { 'type':'normal' }
        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        means = xr.DataArray( data=means, dims='T' )
        sds   = xr.DataArray( data=sds,   dims='T' )
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds }, attrs=attrs )
        
        my_dakota = DakotaClass()
        my_dakota.add_variable('test_var', test_var)
        
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('means'), means ) )
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('std_deviations'), sds ) )

    def test_add_lognormal_variable(self):

        attrs = { 'type':'lognormal' }
        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        means = xr.DataArray( data=means, dims='T' )
        sds   = xr.DataArray( data=sds,   dims='T' )
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds }, attrs=attrs )
        
        my_dakota = DakotaClass()
        my_dakota.add_variable('test_var', test_var)
        
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('means'), means ) )
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('std_deviations'), sds ) )

    def test_add_scan_variable(self):

        attrs = { 'type':'scan' }
        lower = [ 0.1,0.2,0.3,0.4 ]
        upper = [ 1.0,2.0,3.0,4.0 ]
        partitions = [ 2,3,4,5 ]
       
        lower = xr.DataArray( data=lower, dims='T' )
        upper = xr.DataArray( data=upper, dims='T' )
        partitions = xr.DataArray( data=partitions, dims='T' )
        
        test_var = xr.Dataset( {'lower_bounds':lower, 'upper_bounds':upper, 'partitions':partitions }, attrs=attrs )
        
        my_dakota = DakotaClass()
        my_dakota.add_variable('test_var', test_var)
        
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('lower_bounds'), lower ) )
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('upper_bounds'), upper ) )

    def test_add_correlated_scan_variable(self):

        attrs = { 'type':'scan_correlated' }
        lower = [ 0.1,0.2,0.3,0.4 ]
        upper = [ 1.0,2.0,3.0,4.0 ]
        partitions = [ 4,4,4,4 ]

        lower = xr.DataArray( data=lower, dims='T' )
        upper = xr.DataArray( data=upper, dims='T' )
        partitions = xr.DataArray( data=partitions, dims='T' )
        
        test_var = xr.Dataset( {'lower_bounds':lower, 'upper_bounds':upper, 'partitions':partitions }, attrs=attrs )
        
        my_dakota = DakotaClass()
        my_dakota.add_variable('test_var', test_var)

        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('lower_bounds'), [0.0] ) )
        self.assertTrue( np.array_equal( my_dakota.dakota.get_attribute('upper_bounds'), [1.0] ) )

    def test_write_dakote_file(self):

        my_dakota = DakotaClass()
        my_dakota.write_input_file('test_dakota.dat')
        self.assertTrue( os.path.isfile('test_dakota.dat') )
        os.remove('test_dakota.dat')

######################################################
# FAILURE TESTS
######################################################

    def test_add_variable_not_dataset(self):

        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        test_var = {'means':means, 'std_deviations':sds }
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_variable_with_no_type(self):

        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        means = xr.DataArray( data=means, dims='T' )
        sds   = xr.DataArray( data=sds,   dims='T' )
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds } )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_variable_unknown_type(self):

        attrs = { 'type':'unknown' }
        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds }, attrs=attrs )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_variable_missing_data(self):

        attrs = { 'type':'normal' }
        means = [ 1.0,2.0,3.0,4.0 ]
        
        test_var = xr.Dataset( {'means':means}, attrs=attrs )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_variable_incompatible_data(self):

        attrs = { 'type':'normal' }
        means = [ 1.0,2.0,3.0,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4,0.5 ]
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds}, attrs=attrs )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_variable_with_nans(self):

        attrs = { 'type':'normal' }
        means = [ 1.0,2.0,np.nan,4.0 ]
        sds   = [ 0.1,0.2,0.3,0.4 ]
        
        test_var = xr.Dataset( {'means':means, 'std_deviations':sds}, attrs=attrs )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

    def test_add_correlated_scan_variable_with_inconsistent_partitions(self):

        attrs = { 'type':'scan_correlated' }
        lower = [ 0.1,0.2,0.3,0.4 ]
        upper = [ 1.0,2.0,3.0,4.0 ]
        partitions = [ 4,5,4,4 ]

        lower = xr.DataArray( data=lower, dims='T' )
        upper = xr.DataArray( data=upper, dims='T' )
        partitions = xr.DataArray( data=partitions, dims='T' )
        
        test_var = xr.Dataset( {'lower_bounds':lower, 'upper_bounds':upper, 'partitions':partitions }, attrs=attrs )
        
        my_dakota = DakotaClass()

        with self.assertRaises(DatasetError):
            my_dakota.add_variable('test_var', test_var)

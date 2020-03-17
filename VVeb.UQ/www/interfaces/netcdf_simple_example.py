# --- Modules
import numpy
import netCDF4

# --- First we write some data to a netcdf file
print('--------------------------')
print('--------------------------')
print('--------------------------')
print('Writing netcdf data\n')

# --- We will create 4 groups to be sampled: two 0D (scalar) groups, one 1D group, and one 3D groups
# --- Note, the only rules are:
# ---                           - all groups contain a "data" variable with corresponding "error" variable
# ---                           - each group contains an integer for the number of samples, named "n_samples"
netcdf_file = netCDF4.Dataset('netcdf_input.nc','w', format='NETCDF4')

# --- First 0D group
group1        = netcdf_file.createGroup('group-1')
g1_scalar     = group1.createVariable('data',  'f8')
g1_error      = group1.createVariable('error', 'f8')
g1_samples    = group1.createVariable('n_samples', 'i4')
g1_scalar[0]  = 3.5
g1_error[0]   = 0.3
g1_samples[0] = 7 

# --- Second 0D group
group2        = netcdf_file.createGroup('another_group')
g2_dim        = group2.createDimension('notneeded', 1)
g2_scalar     = group2.createVariable('data',  'f8', ('notneeded'))
g2_error      = group2.createVariable('error', 'f8', ('notneeded'))
g2_samples    = group2.createVariable('n_samples', 'i4')
g2_scalar[0]  = 2.75e3
g2_error[0]   = 2.3456
g2_samples[0] = 3 

# --- The 1D group
group3        = netcdf_file.createGroup('the_1D_group')
n_dim         = 127
g3_dim        = group3.createDimension('name-is-your-choice', n_dim)
g3_array      = group3.createVariable('data',  'f8', ('name-is-your-choice'))
g3_error      = group3.createVariable('error', 'f8', ('name-is-your-choice'))
g3_samples    = group3.createVariable('n_samples', 'i4')
g3_array[:]   = numpy.random.rand(n_dim)
g3_error[:]   = 0.02 * numpy.random.rand(n_dim)
g3_samples[0] = 10

# --- The 3D group
group4          = netcdf_file.createGroup('finally-the_3D_group')
n_dim1          = 23
n_dim2          = 76
n_dim3          = 5
g4_dim1         = group4.createDimension('first-dim', n_dim1)
g4_dim2         = group4.createDimension('dim-#2', n_dim2)
g4_dim3         = group4.createDimension('3rd_dimension', n_dim3)
g4_array        = group4.createVariable('data',  'f8', ('first-dim','dim-#2','3rd_dimension') )
g4_error        = group4.createVariable('error', 'f8', ('first-dim','dim-#2','3rd_dimension') )
g4_samples      = group4.createVariable('n_samples', 'i4')
g4_array[:,:,:] = numpy.random.rand(n_dim1,n_dim2,n_dim3)
g4_error[:,:,:] = 0.01 * numpy.random.rand(n_dim1,n_dim2,n_dim3)
g4_samples[0]   = 20

netcdf_file.close()













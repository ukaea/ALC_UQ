#!/bin/bash

# Link scripts needed by DAKOTA to run interface
cp ../../python/dakota_file.py files_for_dakota
cp ../../python/definitions.py files_for_dakota
cp ../../python/exceptions.py  files_for_dakota
cp ../../python/interface.py   files_for_dakota
cp ../../python/interface2.py  files_for_dakota

# Link scripts needed here to generate input files
cp ../../python/dakota_file.py . 
cp ../../python/container.py .
cp ../../python/dakota_class.py .
cp ../../python/definitions.py .
cp ../../python/exceptions.py .
cp ../../example_scripts/example_sample.py .
cp ../../python/main.py .

# Run example sample to create a netcdf file with some 'user' data in
python example_sample.py

# Run main.py to generate a DAKOTA input file
# We will run 4 aynchronous jobs
python main.py -d 'python interface_test.py dakota_params dakota_results DAKOTA.nc netcdf' -c 4

# Move netcdf file
mv DAKOTA.nc files_for_dakota

# Run DAKOTA with this input file
dakota DAKOTA.in > DAKOTA.tmp

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
cp ../../python/main.py .

# Here we start with a user created csv file already so no need to
# run an example script.

# Run main.py to generate a DAKOTA input file
# We will run 4 aynchronous jobs
python main.py -d 'python interface_test.py dakota_params dakota_results DAKOTA.csv csv' -c 4 -i files_for_dakota/DAKOTA.csv -t csv

# Run DAKOTA with this input file
dakota DAKOTA.in > DAKOTA.tmp

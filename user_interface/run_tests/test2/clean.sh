# Removes dakota files after a run

rm files_for_dakota/dakota_file.py
rm files_for_dakota/definitions.py
rm files_for_dakota/exceptions.py
rm files_for_dakota/interface.py
rm files_for_dakota/interface2.py

# Link scripts needed here to generate input files
rm dakota_file.py 
rm container.py
rm dakota_class.py
rm definitions.py
rm exceptions.py
rm example_sample.py
rm main.py

# Remove DAKOTA work directories
rm -r workdir_VVebUQ.1
rm -r workdir_VVebUQ.2
rm -r workdir_VVebUQ.3
rm -r workdir_VVebUQ.4

# Remove DAKOTA files
rm LHS_*
rm DAKOTA.tmp
rm dakota.rst
rm DAKOTA.dat
rm DAKOTA.in
rm files_for_dakota/DAKOTA.nc

rm -r __pycache__

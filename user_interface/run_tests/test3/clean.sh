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
rm main.py

# Remove DAKOTA work directories
rm -r workdir_VVebUQ.*

# Remove DAKOTA files
rm DAKOTA.tmp
rm dakota.rst
rm DAKOTA.dat
rm DAKOTA.in
rm files_for_dakota/DAKOTA.nc

rm -r __pycache__

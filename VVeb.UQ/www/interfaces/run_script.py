#!/usr/bin/python3
import os
import subprocess
import sys
import zipfile

# --- Dakota arguments (should be 2: input and ouput file names)
if (len(sys.argv) != 3):
    print('run_script: not enough arguments')
    sys.exit()

# --- Extract arguments
with open('arguments_for_dakota_script.txt') as args_file:
    data = args_file.read()
my_args = data.split(' ')
if (len(my_args) != 8):
    print('run_script: not enough arguments in arguments_for_dakota_script.txt')
    sys.exit()
container_name = my_args[0]
run_dir        = my_args[1]
image_name     = my_args[2]
filename       = my_args[3]
file_type      = my_args[4]
data_filename  = my_args[5]
dakota_dir     = my_args[6]
use_prominence = my_args[7]

# --- Preprocessing (ie. convert dakota params file back to netcdf)
cmd = 'python3 /dakota_user_interface/python/interface.py dakota_params dakota_results %s %s' % (filename, file_type)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()

# Create tarball of work directory
path   = os.getcwd()
my_dir = path.split('/')
my_dir = my_dir[len(my_dir)-1]

# --- Unzip data file if present
if ( (data_filename != 'none') and (data_filename != 'select_data_file') ):
    with zipfile.ZipFile(data_filename,"r") as zip_ref:
        zip_ref.extractall()

# --- If running with Prominence
if (use_prominence == 'use_prominence'):
    sys.exit()
# --- If running locally
else:
    # --- Run container for each dir
    cmd = 'docker container run --privileged --name ' + container_name + '_' + my_dir + ' -v ' + run_dir + '/' + my_dir + ':/tmp/work_dir/ -v ' + dakota_dir + ':/dakota_user_interface/ -d ' + image_name
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    # --- Get output to printout
    output = str(process.stdout.read(),'utf-8')
    cmd = 'printf "new container: ' + output + '" >> /VVebUQ_runs/terminal_output.txt'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

# --- Postprocessing (write fake output file to keep Dakota happy)
with open(sys.argv[2], 'w') as output_file:
    string = '%21s%17.15e f' % ("", 0.0)
    output_file.write(string)


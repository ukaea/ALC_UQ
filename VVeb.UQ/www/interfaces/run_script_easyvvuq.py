#!/usr/bin/env python3

import sys
import os
import json
import subprocess

sys.path.insert(1, '/VVebUQ_user_interface/python/')
from dakota_file import DakotaFile
from definitions import *

# Define a custom encoder to use to write varied data back to DakotaFile
class VVebUQ_Encoder:

    def encode(self, params, input_file, file_type ):

        # Read existing data file (need shapes)
        user_file = DakotaFile( file_type = file_type )
        user_file.read( input_file )

        # Format data in params into correct shapes and add values entries to file
        self.parse_data( user_file, params )
 
        # Write new data file with varied data in the target directory
        user_file.write( input_file )
        
    def parse_data( self, user_file, params ):

        # This is basically the same as in interface.py for DAKOTA

        # Loop over uncertain variables and reconstruct data arrays
        for key in user_file.uncertain.keys():

            # Get the dataset for this variable
            dataset = user_file.get_variable_as_dataset(key)

            # Get the type of this variable
            var_type = dataset.attrs['type']

            # Get one of the required entries
            var_name = allowed_variable_types[var_type]['required'][0]

            var = dataset[var_name]

            # Add new values variable to data array
            dataset['values'] = deepcopy(var)

            # Get size and shape of the data array
            size  = var.size
            shape = var.shape

            data  = np.zeros( size )

            for i in range( size ):

                varname = key+'_'+str(i)
                data[i] = params[varname]

            values_data = data.reshape( shape )

            # Add data to values data array
            dataset.data_vars['values'].data = values_data

# --- Function to execute command with interactive printout sent to web-terminal in real-time
def interactive_command(cmd,session_name):
    # --- Execute command
    try:
        cmd2 = 'printf "' + cmd + '" > /VVebUQ_runs/'+session_name+'/terminal_command.txt'
        process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    except  Exception as exc:
        print('Failed to execute command:\n%s' % (cmd))
        print('due to exception:', exc)
        sys.exit()
    # --- Get output to web-terminal printout
    try:
        output = str(process.stdout.read(),'utf-8')
        cmd2 = 'printf "new container: ' + output + '" >> /VVebUQ_runs/'+session_name+'/terminal_output.txt'
        process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    except  Exception as exc:
        print('Failed to print web-terminal output for command:\n%s' % (cmd))
        print('due to exception:', exc)
        sys.exit()

# ---------------
# --- Main script
# ---------------

# --- Input file should be 1st argument
if len(sys.argv) != 2:
    print('run_script_easyvvuq: not enough arguments')
    sys.exit()
json_input = sys.argv[1]
if not os.path.isfile(json_input):
    print('run_script_easyvvuq: input file does not exist')
    sys.exit()

# --- Get additional files into run-dir
cwd = os.getcwd()
work_dir = cwd.split('easyvvuq_campaign')[0]
cmd = 'cp '+work_dir+'files_for_easyvvuq/* .'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()

# --- Extract arguments from VVeb.UQ app
with open('arguments_for_vvuq_script.txt') as args_file:
    data = args_file.read()
my_args = data.strip().split(' ')
if (len(my_args) != 12):
    print('run_script: not enough arguments in arguments_for_vvuq_script.txt')
    sys.exit()
container_name = my_args[0]
run_dir        = my_args[1]
image_name     = my_args[2]
filename       = my_args[3]
file_type      = my_args[4]
data_filename  = my_args[5]
user_inter_dir = my_args[6]
use_prominence = my_args[7]
n_cpu          = my_args[8]
RAM            = my_args[9]
selected_vvuq  = my_args[10]
session_name   = my_args[11]

# --- Deal with the inputs
with open(json_input, "r") as f:
    inputs = json.load(f)
output_filename = inputs['outfile']
all_vars = []
for key in (inputs):
    if ("var" in key):
        all_vars.append(float(inputs[key]))

# Write the new parameter data back to the Dakota input file
encoder = VVebUQ_Encoder()
encoder.encode(inputs, filename, file_type)

# --- Unzip data file if present
if ( (data_filename != 'none') and (data_filename != 'select_data_file') ):
    interactive_command('unzip -u '+data_filename,session_name)

# --- Last I tried, easyVVUQ average didn't work unless result had at least two values
with open("easyvvuq_out.csv", 'w') as output_file:
    output_file.write("STEP,VALUE\n")
    output_file.write("0,"+str(0.1)+"\n")
    output_file.write("1,"+str(0.2)+"\n")
    output_file.write("2,"+str(0.3)+"\n")




#!/usr/bin/env python3

import sys
import os
import json
import subprocess

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

# --- Unzip data file if present
if ( (data_filename != 'none') and (data_filename != 'select_data_file') ):
    interactive_command('unzip -u '+data_filename,session_name)

# --- Last I tried, easyVVUQ average didn't work unless result had at least two values
with open("easyvvuq_out.csv", 'w') as output_file:
    output_file.write("STEP,VALUE\n")
    output_file.write("0,"+str(0.1)+"\n")
    output_file.write("1,"+str(0.2)+"\n")
    output_file.write("2,"+str(0.3)+"\n")




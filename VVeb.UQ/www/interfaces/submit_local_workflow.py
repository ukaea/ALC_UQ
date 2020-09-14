#!/usr/bin/python3
import os
import subprocess
import sys



# --- Function to execute command with interactive printout sent to web-terminal in real-time
def interactive_command(cmd):
    # --- Execute command
    try:
        cmd2 = 'printf "' + cmd + '" > /VVebUQ_runs/terminal_command.txt'
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
        cmd2 = 'printf "new container: ' + output + '" >> /VVebUQ_runs/terminal_output.txt'
        process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    except  Exception as exc:
        print('Failed to print web-terminal output for command:\n%s' % (cmd))
        print('due to exception:', exc)
        sys.exit()





# ---------------
# --- Main script
# ---------------



# --- Extract arguments
with open('arguments_for_dakota_script.txt') as args_file:
    data = args_file.read()
my_args = data.strip().split(' ')
if (len(my_args) != 9):
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
n_cpu          = my_args[8]

# --- Get all task-directories
try:
    cmd = 'ls |grep "workdir_VVebUQ"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    subdirs = str(process.stdout.read(),'utf-8')
    subdirs = subdirs.splitlines()
except  Exception as exc:
    print('Failed to execute command:\n%s' % (cmd))
    print('due to exception:', exc)
    sys.exit()

# --- Run container for each dir
for my_dir in subdirs:
    if (my_dir.strip() != ''):
        cmd = 'docker container run --privileged --name ' + container_name + '_' + my_dir + ' -v ' + run_dir + '/' + my_dir + ':/tmp/work_dir/ -v ' + dakota_dir + ':/dakota_user_interface/ -d ' + image_name
        interactive_command(cmd)






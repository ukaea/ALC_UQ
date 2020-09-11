#!/usr/bin/python3
import os
import subprocess
import sys
import json
import requests

# --- Function to execute command with interactive printout sent to web-terminal in real-time
def interactive_command(cmd):
    # --- Execute command
    try:
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



# --- Get the Prominence Session Token if it exists
def get_prominence_token():
    if os.path.isfile(os.path.expanduser('~/.prominence/token')):
        try:
            with open(os.path.expanduser('~/.prominence/token')) as json_data:
                data = json.load(json_data)
        except Exception as ex:
            print('Error trying to read token:', ex)
            return None

        if 'access_token' in data:
            token = data['access_token']
            return token
        else:
            print('The saved token file does not contain access_token')
            return None
    else:
        print('PROMINENCE token file ~/.prominence/token does not exist')
        return None




# --- Get a temporary URL from Prominence which can be used for uploading the run directory tarball
def get_prominence_upload_url(filename, headers):
    try:
        response = requests.post('%s/data/upload' % os.environ['PROMINENCE_URL'],
                                 json={'filename':os.path.basename(filename)},
                                 timeout=30,
                                 headers=headers)
    except requests.exceptions.RequestException as exc:
        print('Unable to get URL due to', exc)
        return None

    if response.status_code == 401:
        print('Authentication failed')

    if response.status_code == 201:
        if 'url' in response.json():
            return response.json()['url']

    return None




# ---------------
# --- Main script
# ---------------


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
my_run = my_dir[len(my_dir)-2]
my_dir = my_dir[len(my_dir)-1]

# --- Unzip data file if present
if ( (data_filename != 'none') and (data_filename != 'select_data_file') ):
    interactive_command('unzip -u '+data_filename)

# --- If running with Prominence
if (use_prominence == 'true'):
    # --- Get Prominence token to check session is valid
    token = get_prominence_token()
    headers = {'Authorization':'Bearer %s' % token}
    # --- Create tarball of directory
    tarball = my_run+'___'+my_dir+'.tar.gz'
    interactive_command('tar -cvzf '+tarball+' ../'+my_dir)
    # --- Get url from Prominence for this upload
    url = get_prominence_upload_url(tarball, headers)
    if (url is None):
        print('Prominence: Unable to obtain upload URL')
        sys.exit()
    # --- Upload zipped file to Prominence
    try:
        with open(tarball, 'rb') as file_obj:
            response = requests.put(url, data=file_obj, timeout=60)
    except Exception as exc:
        print('Prominence: Unable to upload tarball due to', exc)
        sys.exit()
    if (response.status_code != 200):
        print('Prominence: Unable to upload tarball due to status error: ', response.status_code)
        sys.exit()
    # --- Remove zipped file now that it's uploaded
    os.remove(tarball)
    # --- Create json file to define job for Prominence
    resources = {}
    resources['cpus'] = 1
    resources['memory'] = 1
    resources['disk'] = 10
    resources['nodes'] = 1
    resources['walltime'] = 3600
    task = {}
    task['cmd'] = ''
    task['image'] = image_name
    task['runtime'] = 'udocker'
    task['workdir'] = '/tmp/work_dir'
    artifact1 = {}
    artifact1['url'] = tarball
    artifact1['mountpoint'] = '%s:/tmp/work_dir' % my_dir
    artifact2 = {}
    artifact2['url'] = 'dakota_user_interface.tgz'
    artifact2['mountpoint'] = 'dakota_user_interface:/dakota_user_interface'
    job = {}
    job['name'] = '%s' % my_dir
    job['name'] = job['name'].replace('.', '_')
    job['tasks'] = [task]
    job['resources'] = resources
    job['artifacts'] = [artifact1,artifact2]
    job['outputDirs'] = [my_dir]
    with open('../%s.json' % my_dir, 'w') as outfile:
        json.dump(job, outfile)

# --- If running locally
else:
    # --- Run container for each dir
    cmd = 'docker container run --privileged --name ' + container_name + '_' + my_dir + ' -v ' + run_dir + '/' + my_dir + ':/tmp/work_dir/ -v ' + dakota_dir + ':/dakota_user_interface/ -d ' + image_name
    interactive_command(cmd)

# --- Postprocessing (write fake output file to keep Dakota happy)
with open(sys.argv[2], 'w') as output_file:
    string = '%21s%17.15e f' % ("", 0.0)
    output_file.write(string)






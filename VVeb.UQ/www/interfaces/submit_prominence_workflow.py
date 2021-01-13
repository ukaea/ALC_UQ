#!/usr/bin/python3
import os
import subprocess
import sys
import json
import requests

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



# --- Extract arguments
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

# --- Get paths
path   = os.getcwd()
my_run = path.split('/')
my_run = my_run[len(my_run)-1]

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

# --- Get Prominence token to check session is valid
token = get_prominence_token()
headers = {'Authorization':'Bearer %s' % token}

# --- Upload Dakota user interface
tarball = 'VVebUQ_user_interface.tgz'
interactive_command('tar -cvzf '+tarball+' /VVebUQ_user_interface',session_name)
# --- Get url from Prominence for this upload
url = get_prominence_upload_url(tarball, headers)
if (url is None):
    print('Prominence: Unable to obtain upload URL for VVebUQ_user_interface')
    sys.exit()
# --- Upload zipped file to Prominence
try:
    with open(tarball, 'rb') as file_obj:
        response = requests.put(url, data=file_obj, timeout=60)
except Exception as exc:
    print('Prominence: Unable to upload VVebUQ_user_interface tarball due to', exc)
    sys.exit()
if (response.status_code != 200):
    print('Prominence: Unable to upload VVebUQ_user_interface tarball due to status error: ', response.status_code)
    sys.exit()
# --- Remove zipped file now that it's uploaded
os.remove(tarball)

# --- Create .json job for each dir
for my_dir in subdirs:
    if (my_dir.strip() == ''): continue
    # --- Create tarball of directory
    tarball = my_run+'___'+my_dir+'.tar.gz'
    tarball_fullpath = my_dir+'/'+tarball
    interactive_command('cd '+my_dir+'; tar -cvzf '+tarball+' ../'+my_dir+'; cd --',session_name)
    # --- Get url from Prominence for this upload
    url = get_prominence_upload_url(tarball_fullpath, headers)
    if (url is None):
        print('Prominence: Unable to obtain upload URL')
        sys.exit()
    # --- Upload zipped file to Prominence
    try:
        with open(tarball_fullpath, 'rb') as file_obj:
            response = requests.put(url, data=file_obj, timeout=60)
    except Exception as exc:
        print('Prominence: Unable to upload tarball due to', exc)
        sys.exit()
    if (response.status_code != 200):
        print('Prominence: Unable to upload tarball due to status error: ', response.status_code)
        sys.exit()
    # --- Remove zipped file now that it's uploaded
    os.remove(tarball_fullpath)
    # --- Create json file to define job for Prominence
    resources = {}
    resources['cpus'] = int(n_cpu)
    resources['memory'] = int(RAM)
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
    artifact2['url'] = 'VVebUQ_user_interface.tgz'
    artifact2['mountpoint'] = 'VVebUQ_user_interface:/VVebUQ_user_interface'
    job = {}
    job['name'] = '%s' % my_dir
    job['name'] = job['name'].replace('.', '_')
    job['tasks'] = [task]
    job['resources'] = resources
    job['artifacts'] = [artifact1,artifact2]
    job['outputDirs'] = [my_dir]
    with open('%s.json' % my_dir, 'w') as outfile:
        json.dump(job, outfile)

# --- Create .json workflow containing all jobs
jobs = []
for my_dir in subdirs:
    if (my_dir.strip() == ''): continue
    with open(my_dir+'.json') as json_file:
        data = json.load(json_file)
        jobs.append(data)
workflow = {}
workflow['jobs'] = jobs
workflow['name'] = my_run
with open('prominence_workflow.json', 'w') as outfile:
    json.dump(workflow, outfile)

# --- Submit Workflow
cmd = 'prominence run prominence_workflow.json'
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
output = str(process.stdout.read(),'utf-8')
workflow_id = output.partition('Workflow created with id ')[2].strip()
with open('prominence_workflow_id.txt', 'w') as outfile:
    outfile.write(workflow_id)



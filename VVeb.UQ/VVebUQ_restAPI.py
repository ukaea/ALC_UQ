#!/usr/bin/python3
import os
import subprocess
import sys
import json
import requests


def clean_exit(message):
    print('VVebUQ_restAPI.py: %s' % (message))
    print('                   visit https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ_REST_API')
    print('                   for detailed instructions.')
    sys.exit()

def execute_command(cmd):
    print('>>> processing command:\n    '+cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    response = str(process.stdout.read(),'utf-8')
    print('>>> reply:\n    '+response)

# ---------------
# --- Main script
# ---------------


# --- List of valid actions
valid_actions = ["upload-input-file", \
                 "upload-data-file", \
                 "launch-run", \
                 "list-previous-runs", \
                 "list-run-data", \
                 "download-run-data", \
                 "download-run-selected-files", \
                 "stop-run", \
                 "purge-run"]

# --- Script arguments (should be the name of the .json file)
if (len(sys.argv) != 3):
    clean_exit('please provide a .json instructions file, or a JSON string.')

# --- Open .json instruction file and load data
input_type = sys.argv[1]
if (input_type == '-f'):
    filename = sys.argv[2]
    try:
        with open(filename) as json_file:
            instructions = json.load(json_file)
    except Exception as exc:
        clean_exit('Error loading json file:\n'+str(exc))
elif (input_type == '-s'):
    json_string = sys.argv[2]
    try:
        instructions = json.loads(json_string)
    except Exception as exc:
        clean_exit('Error loading json string:\n'+str(exc))
else:
    clean_exit('option is either -f (for instructions file) or -s (for instructions strong)')

# --- Get IP address and PORT of VVebUQ App
if (os.environ.get('VVEBUQ_IP_ADDRESS') is not None):
    VVebUQ_IP = os.environ['VVEBUQ_IP_ADDRESS']
else:
    clean_exit('please set the environment variable VVEBUQ_IP_ADDRESS')
if (os.environ.get('VVEBUQ_PORT') is not None):
    VVebUQ_PORT = os.environ['VVEBUQ_PORT']
else:
    print('Warning: Environment variable VVEBUQ_PORT not specified, using 8080 as default')
    VVebUQ_PORT = 8080

# --- Bas URL
baseurl = 'http://'+str(VVebUQ_IP)+':'+str(VVebUQ_PORT)

# --- Get the requested action
if (instructions["action"] is None):
    clean_exit('Your json file does not contain any action.')
else:
    if (instructions["action"] == ''):
        clean_exit('Your json file does not contain any action.')
    else:
        ACTION = instructions["action"]

# --- Check action is valid
if (ACTION not in valid_actions):
    clean_exit('please select a valid action')



# --- Dispatch to selected action


# --- upload-input-file
if (ACTION == 'upload-input-file'):
    if (instructions["filename"] is None):
        clean_exit('ACTION upload-input-file requires a filename.')
    else:
        if (instructions["filename"] == ''):
            clean_exit('ACTION upload-input-file requires a filename.')
        else:
            filename = instructions["filename"]
            if (not os.path.isfile(filename)):
                clean_exit('filename provided does not exist.')
            else:
                try:
                    url = baseurl+'/php/upload.php'
                    cmd = 'curl -F "fileToUpload[]=@'+filename+'" '+url
                    execute_command(cmd)
                except Exception as exc:
                    clean_exit('file upload failed due to\n'+str(exc))


# --- upload-data-file
if (ACTION == 'upload-data-file'):
    if (instructions["filename"] is None):
        clean_exit('ACTION upload-data-file requires a filename.')
    else:
        if (instructions["filename"] == ''):
            clean_exit('ACTION upload-data-file requires a filename.')
        else:
            filename = instructions["filename"]
            if (not os.path.isfile(filename)):
                clean_exit('filename provided does not exist.')
            else:
                try:
                    url = baseurl+'/php/upload_data_file.php'
                    cmd = 'curl -F "dataFileToUpload[]=@'+filename+'" '+url
                    execute_command(cmd)
                except Exception as exc:
                    clean_exit('file upload failed due to\n'+str(exc))


#valid_actions = ["upload-input-file", \
#                 "upload-data-file", \
#                 "launch-run", \
#                 "list-previous-runs", \
#                 "list-run-data", \
#                 "download-run-data", \
#                 "download-run-selected-files", \
#                 "stop-run", \
#                 "purge-run"]







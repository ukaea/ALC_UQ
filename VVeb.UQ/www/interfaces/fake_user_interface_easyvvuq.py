#!/usr/bin/python3
import os
import sys
import json


# --- Get inputs
run_script = ''
input_file = ''
easyvvuq_script = ''
file_type = ''
for i in range(len(sys.argv)-1):
    if (sys.argv[i].lower() == '-d'):
        run_script = sys.argv[i+1]
    if (sys.argv[i].lower() == '-i'):
        input_file = sys.argv[i+1]
    if (sys.argv[i].lower() == '-o'):
        easyvvuq_script = sys.argv[i+1]
    if (sys.argv[i].lower() == '-t'):
        file_type = sys.argv[i+1]
# --- Note: for now, only csv file-type accepted
if (file_type != 'csv'):
    print('fake_user_interface_easyvvuq.py: only csv file-type accepted')
    sys.exit()

# --- Check actual input file type
file_ext = input_file.split(".")
file_ext = file_ext[len(file_ext)-1]
if (file_ext.lower() != "csv"):
    print('fake_user_interface_easyvvuq.py: only csv file-type accepted, your file has extension: '+file_ext)
    print('fake_user_interface_easyvvuq.py: it needs to be a .csv file')
    sys.exit()

# --- Get data from input file, note: only MC method accepted for now
if not os.path.isfile(input_file):
    print('fake_user_interface_easyvvuq.py: input file does not exist')
    sys.exit()
with open(input_file) as file_tmp:
    method = file_tmp.readline().strip()
    if (method != 'MC'):
        print('fake_user_interface_easyvvuq.py: only MC method accepted')
        sys.exit()
    n_samples = int(file_tmp.readline())
all_vars = {}
out_vars = {}
variations = "{"
with open(input_file) as file_tmp:
    count = 0
    for line in file_tmp:
        count = count + 1
        if (count < 3): continue
        values = line.split(",")
        # Note: not sure if this is exact for this method, but J.Buchanan will know and do it properly in the real user-interface
        val_min = float(values[0]) - float(values[1])
        val_max = float(values[0]) + float(values[1])
        val_def = float(values[0]) 
        val_tmp = {"type": "float",
                   "min": val_min,
                   "max": val_max,
                   "default": val_def}
        val_name = "var"+str(count-2)
        all_vars[val_name] = val_tmp
        variations = variations+"\""+val_name+"\": cp.Uniform("+str(val_min)+","+str(val_max)+"),"
        out_vars[val_name] = "$"+val_name
variations = variations+"}"
out_vars["outfile"] = "$out_file"
all_vars["out_file"] = {}
all_vars["out_file"]["type"] = "string"
all_vars["out_file"]["default"] = "easyvvuq_out.csv"

run_script = "run_script = \'"+run_script+"\'\n"
parameters = "parameters = "+json.dumps(all_vars)+"\n"
variations = "variations = "+variations+"\n"
n_samples  = "n_samples  = "+str(n_samples)+"\n"

all_strings = run_script + parameters + variations + n_samples

with open('easyvvuq_main.sample') as file_tmp:
    file_string = file_tmp.read()
    file_string = file_string.replace('#REPLACE_INPUTS_HERE',all_strings)

with open(easyvvuq_script, 'w') as outfile:
    outfile.write(file_string)

with open('easyvvuq_input.template', 'w') as outfile:
    json.dump(out_vars,outfile)





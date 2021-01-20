
# FIX TO USE QUASI-MC, SC, PCE

#!/usr/bin/python3
import os
import sys
import json
import argparse
from dakota_file import DakotaFile

# Handle arguments
parser = argparse.ArgumentParser()

helpstr = "Name of the analysis driver to execute"
parser.add_argument("-d", "--driver", default='run_script_easyvvuq.py', help=helpstr)

helpstr = "Name of the input file to use"
parser.add_argument("-i", "--input", default='DAKOTA.nc', help=helpstr)

helpstr = "Type of input file. Currently supports netcdf (n) and csv (c)"
parser.add_argument("-t", "--type", default='netcdf', help=helpstr)

helpstr = "Name of the output file to create"
parser.add_argument("-o", "--output", default='easyvvuq_main.py', help=helpstr)

args = parser.parse_args()

# Read user provided file
user_file = DakotaFile( file_type = args.type )
user_file.read( args.input )

# If samples is present in settings this is a pure sampling run
# Otherwise it is some kind of scan (PCE/SC etc)
n_samples = 0
if 'samples' in user_file.settings:
    n_samples = user_file.settings['samples'] 

all_vars = {}
out_vars = {}

variations = "{"

for name, dataset in user_file.uncertain.items():

    # For now just accommodate uniform and normal distributions (should be straightforward to add more)
    if( dataset.attrs['type'] == 'uniform'):
        
        # Uniform distributed data
        minima = np.array(dataset['lower_bounds'].data).flatten()
        maxima = np.array(dataset['upper_bounds'].data).flatten()

        assert minima.size == maxima.size

        for i in range( minima.size ):

            val_name = name + '_' + str(i)

            val_min = float(minima[i])
            val_max = float(maxima[i])
            val_def = 0.5 * ( val_min + val_max ) 
            val_tmp = {"type": "float", "min": val_min, "max": val_max, "default": val_def}

            all_vars[val_name] = val_tmp
            variations = variations+"\""+val_name+"\": cp.Uniform("+str(val_min)+","+str(val_max)+"),"
            out_vars[val_name] = "$"+val_name

    elif( dataset.attrs['type'] == 'normal' ):

        # Normal distributed data
        means = np.array(dataset['means'].data).flatten()
        sds   = np.array(dataset['std_deviations'].data).flatten()

        assert means.size == sds.size

        for i in range( means.size ):

            val_name = name + '_' + str(i)

            val_mean = float(means[i])
            val_sd   = float(  sds[i])
            val_tmp = {"type": "float", "default": val_mean}

            all_vars[val_name] = val_tmp
            variations = variations+"\""+val_name+"\": cp.Normal(mu="+str(val_mean)+",sigma="+str(val_sd)+"),"
            out_vars[val_name] = "$"+val_name

    else:
        raise Exception("Unknown probability distribution selected. ABORTING!")

variations = variations+"}"

out_vars["outfile"]             = "$out_file"
all_vars["out_file"]            = {}
all_vars["out_file"]["type"]    = "string"
all_vars["out_file"]["default"] = "easyvvuq_out.csv"

run_script = "run_script = \'"+args.driver+"\'\n"
parameters = "parameters = "+json.dumps(all_vars)+"\n"
variations = "variations = "+variations+"\n"
n_samples  = "n_samples  = "+str(n_samples)+"\n"

all_strings = run_script + parameters + variations + n_samples

# Main sample opened here - inputs replaced from file!
with open('easyvvuq_main.sample') as file_tmp:
    file_string = file_tmp.read()
    file_string = file_string.replace('#REPLACE_INPUTS_HERE',all_strings)
    file_string = file_string.replace('#FILENAME#',args.input )
    file_string = file_string.replace('#FILETYPE#',args.type  )

with open(args.output, 'w') as outfile:
    outfile.write(file_string)

# GENERATES TEMPLATE FILE
with open('easyvvuq_input.template', 'w') as outfile:
    json.dump(out_vars,outfile)





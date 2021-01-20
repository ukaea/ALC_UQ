# Finalises the iteration by setting the failure flag to 0

import dakota.interfacing as di
import os

# Set a default value for the iteration number
iteration = -1

try:

    # Get DAKOTA parameters
    params, results = di.read_parameters_file()

    # Get Iteration number
    iteration = params.eval_num

    # Wait for dummy finished file to exist
    while( True ):

        if os.exists('FINISHED.TXT'):
            break
        else:
            time.sleep(20)

    # Return response indicating run was successful
    results['Failed'].function = 0

    # Write results file
    results.write()

except Exception as inst:

    print('======================================')
    print('ITERATION '+str(iteration)+' FAILED!')
    print()
    print(inst)

    results.fail()
    results.write()

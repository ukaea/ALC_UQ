import os
import sys

# This is the 'user code' called by DAKOTA in this example
# In a real case the call to mycode.py would be replaced by a call
# to the users containerised code.

arglist = ' '.join( sys.argv[1:5] )

# Run the first half of the interface script which reads the DAKOTA
# parameter file and makes a new netcdf with values appended.
os.system('python interface.py ' + arglist)

# Call the users containerised code (in this case a simple python script)
os.system('python mycode.py')

# Call the second half of the interface script which just sets the results
# value in the DAKOTA responses object finishing this iteration.
os.system('python interface2.py ' + arglist)

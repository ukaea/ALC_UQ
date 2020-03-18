import numpy as np
import xarray as xr
import exceptions
import csv

values  = []
results = 0

# Read the csv file
with open('DAKOTA.csv') as csv_file:
                
    csv_reader = csv.reader(csv_file,delimiter=',')

    for row in csv_reader:

        values.append( float(row[0]) )
        results = results + float(row[0])

values = [ str(x) for x in values ]
output_string = ' '.join(values)

with open('DAKOTA_OUTPUT.dat','w') as file_out:

    file_out.write('Varied values are: \n')
    file_out.write(output_string+'\n')

    file_out.write('Sum of values is: \n')
    file_out.write(str(results))
    file_out.close()

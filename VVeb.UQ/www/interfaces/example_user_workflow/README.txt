# Example of user workflow.
There are two ways of running using the app:
- using .csv text input files
- using .nc NETCDF files


# Using CSV format
Here are two examples of input files to feed to the app:
- input_mc.csv 
takes 37 Monte-Carlo samples from the 5 listed values (1st column) withing the corresponding errors (2nd column)
- input_scan.csv
samples scan of three variables (for three rows), between the lower bound (1st column) and the upper bound (2nd column), taking a given number of samples for each row (3rd column)


# Using NETCDF format
For a full description of how to generate and read NETDCF files, please follow instructions in:
https://github.com/ukaea/ALC_UQ/tree/master/user_interface


# Basic workflow
Typically, a code (eg. user_code.py) is embedded into a Docker image.
The user must provide the samples to be scanned by the app, this is done by uploading an input file to the app (eg. input_mc.csv).
Internally, the app will generate, for each individual run, a modified input_mc.csv, which the user_code.py needs to read.
The newly generated input_mc.csv file will simply contain a single column with the allocated values.

For example, if the input_mc.csv given to the app has 5 values to scan:
MC
37
0.1,0.001
1.2,0.2
1048.278464517,10.2
3.5e3,3.1e-1
0.5 , 0.1

then each new file generated at each run will look like
0.105
1.1
1044.27
3.5001e3
0.45

and in that particular case, there will be 37 runs with such files.
This means the user_code.py must expect the same number of values as those given to the app for sampling (here 5 values)

When running with NETCDF format, a similar method is used, but there the new generated file (for each run), will include an additional dataset called "values"









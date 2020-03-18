# Top level program for creation of DAKOTA input file based on a user provided input file 
# The user input file contains groups describing uncertain variables as well as top level
# attributes describing run configuration

# Note that while there are optional inputs to specify the name of the user netcdf file and
# the Dakota input file, the rest of the infrastructure still currently expects these to be
# named DAKOTA.nc and DAKOTA.in

from dakota_class import DakotaClass
from dakota_file import DakotaFile
import argparse

def make_dakota(args):

    # Create template DAKOTA input file
    dakota = DakotaClass()

    # Read user provided file
    user_file = DakotaFile( file_type = args.type )
    user_file.read( args.input )

    # Set Dakota entries from arguments
    dakota.dakota.set_attribute( 'evaluation_concurrency', args.concurrency )
    dakota.dakota.set_attribute( 'analysis_drivers', "'"+args.driver+"'"    )

    # Update DAKOTA input file with uncertain variables
    user_file.write_dakota_input( dakota )

    # Write input file
    dakota.write_input_file( args.output )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    helpstr = "Name of the analysis driver to execute"
    parser.add_argument("-d", "--driver", required=True, help=helpstr)

    helpstr = "Specifies the asynchronous concurrency to use"
    parser.add_argument("-c","--concurrency", required=True, type=int, help=helpstr)

    helpstr = "Name of the input file to use"
    parser.add_argument("-i", "--input", default='DAKOTA.nc', help=helpstr)

    helpstr = "Type of input file. Currently supports netcdf (n) and csv (c)"
    parser.add_argument("-t", "--type", default='netcdf', help=helpstr)

    helpstr = "Name of the output DAKOTA file to create"
    parser.add_argument("-o", "--output", default='DAKOTA.in', help=helpstr)

    args = parser.parse_args()

    make_dakota(args)

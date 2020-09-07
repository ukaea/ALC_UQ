#!/usr/bin/perl
use strict;
use warnings;

# --- Dakota arguments (should be 2: input and ouput file names)
my @my_args = ();
foreach my $a(@ARGV) {push @my_args, $a;}
if ($#my_args ne 1) {exit 1;}
# --- Container arguments
my $my_args_tmp = `cat arguments_for_dakota_script.txt`;
my @my_args2 = split(' ',$my_args_tmp);
if ($#my_args2 ne 6) {exit 2;}
my $container_name = $my_args2[0];
my $run_dir        = $my_args2[1];
my $image_name     = $my_args2[2];
my $filename       = $my_args2[3];
my $file_type      = $my_args2[4];
my $data_filename  = $my_args2[5];
my $dakota_dir     = $my_args2[6];
# --- Initialise some variables
my @split_tmp = ();
my $command = "";
my $output = "";
my $file = "";
# --- Location (needed for the container dir-mount)
my $pwd = `pwd`;
$pwd =~ s/\s+//g;
@split_tmp = split("/",$pwd);
my $dir = $split_tmp[$#split_tmp];
# --- Preprocessing (ie. convert dakota params file back to netcdf)
`python3 /dakota_user_interface/python/interface.py dakota_params dakota_results $filename $file_type`;
# --- Unzip data file if present
if ( ($data_filename ne "none") and ($data_filename ne "select_data_file") ) {`unzip $data_filename`;}
# --- Run container for each dir
$command = 'docker container run --privileged --name '.$container_name.'_'.$dir.' -v '.$run_dir.'/'.$dir.':/tmp/work_dir/ -v '.$dakota_dir.':/dakota_user_interface/ -d '.$image_name;
$output = `$command`;
$command = 'printf "new container: '.$output.'" >> /VVebUQ_runs/terminal_output.txt';
`$command`;
# --- Postprocessing
$output = sprintf("%21s%17.15e f", "", 0.0);
$command = "echo \"".$output."\" >> ".$my_args[1];
`$command`;



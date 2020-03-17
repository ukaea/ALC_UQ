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
if ($#my_args2 ne 2) {exit 2;}
my $container_name = $my_args2[0];
my $run_dir        = $my_args2[1];
my $image_name     = $my_args2[2];
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
`python3 interface.py dakota_params dakota_results`;
# --- Run container for each dir
$command = 'docker container run --name '.$container_name.'_'.$dir.' -v '.$run_dir.'/'.$dir.':/work_dir/ -d '.$image_name;
$output = `$command`;
$command = 'printf "new container: '.$output.'" >> /VVebUQ_runs/terminal_output.txt';
`$command`;
# --- Postprocessing
$output = sprintf("%21s%17.15e f", "", 0.0);
$command = "echo \"".$output."\" >> ".$my_args[1];
`$command`;



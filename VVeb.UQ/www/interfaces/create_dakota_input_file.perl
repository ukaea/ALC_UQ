#!/usr/bin/perl
use strict;
use warnings;
# --- Arguments (should be input file name)
my @my_args = ();
my $filename = "none";
foreach my $a(@ARGV) {push @my_args, $a;}
if ($#my_args eq -1) {exit 0;}
$filename = $my_args[0];
# --- Create file
my $dakota_file = '';
$dakota_file = $dakota_file."environment\n";
$dakota_file = $dakota_file."  tabular_data\n";
$dakota_file = $dakota_file."    tabular_data_file = \"dakota_run.dat\"\n";
$dakota_file = $dakota_file."method\n";
$dakota_file = $dakota_file."  multidim_parameter_study\n";
$dakota_file = $dakota_file."    partitions = 4 4\n";
$dakota_file = $dakota_file."model\n";
$dakota_file = $dakota_file."  single\n";
$dakota_file = $dakota_file."variables\n";
$dakota_file = $dakota_file."  continuous_design = 2\n";
$dakota_file = $dakota_file."    descriptors       \"x1\" \"x2\"\n";
$dakota_file = $dakota_file."    lower_bounds       0.1    0.2\n";
$dakota_file = $dakota_file."    upper_bounds       0.5    0.3\n";
$dakota_file = $dakota_file."interface,\n";
$dakota_file = $dakota_file."        fork\n";
$dakota_file = $dakota_file."          analysis_driver = \"run_script.perl\"\n";
$dakota_file = $dakota_file."          parameters_file = \"dakota_params.in\"\n";
$dakota_file = $dakota_file."          results_file    = \"dakota_params.out\"\n";
$dakota_file = $dakota_file."          work_directory named=\"workdir_VVebUQ\" directory_tag directory_save file_save\n";
$dakota_file = $dakota_file."          copy_files = \"files_for_dakota/*\"\n";
$dakota_file = $dakota_file."        asynchronous\n";
$dakota_file = $dakota_file."          evaluation_concurrency = 16\n";
$dakota_file = $dakota_file."responses\n";
$dakota_file = $dakota_file."  response_functions = 1\n";
$dakota_file = $dakota_file."  no_gradients\n";
$dakota_file = $dakota_file."  no_hessians\n";

open(my $fh, '>', $filename);
print $fh $dakota_file;
close $fh;


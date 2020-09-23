<?php

// --- Get session name
$session_name = $_GET['VVebUQ_session_name'];

// --- Get run directory
$run_name = $_GET["run_name"];
$dir_name  = 'workdir_'.$run_name;

// --- The download location depends on the user
$download_dir = '/var/www/html/VVebUQ_downloads/'.$session_name.'/';
shell_exec('mkdir -p '.$download_dir);

// --- Get names of selected files
$files = $_GET["files"];
$zip_command = 'zip -rg '.$download_dir.$run_name.'_selected.zip ';
foreach ($files as $file)
{
  if (trim($file) != '')
  {
    $filename = $dir_name.'/workdir_VVebUQ.*/'.trim($file);
    $zip_command = $zip_command.' '.$filename;
  }
}

// --- Remove file if it already exists, and create zip file of selected files
shell_exec('cd /VVebUQ_runs/'.$session_name.'/ ; rm -f '.$run_name.'_selected.zip ; cd -');
shell_exec('cd /VVebUQ_runs/'.$session_name.'/ ; '.$zip_command.' ; cd -');

// --- Move zip file to downloads/
shell_exec('mv /VVebUQ_runs/'.$session_name.'/'.$run_name.'_selected.zip '.$download_dir);

// --- We read file into output only for the restAPI
if (! isset($_GET["get_back_to_js"]))
{
  readfile($download_dir.$run_name.'_selected.zip');
}
?>

<?php
$run_name = $_POST["run_name"];
$run_dir = 'workdir_'.$_POST["run_name"];
$files = $_POST["files"];
$zip_command = 'zip -rg '.$run_name.'_selected.zip ';
foreach ($files as $file)
{
  $filename = $run_dir.'/workdir_VVebUQ.*/'.$file;
  $zip_command = $zip_command.' '.$filename;
}
shell_exec('cd /VVebUQ_runs/ ; '.$zip_command.' ; cd -');
shell_exec('mkdir -p ../downloads ; mv /VVebUQ_runs/'.$run_name.'_selected.zip ../downloads/');
readfile('../downloads/'.$run_name.'_selected.zip');
?>

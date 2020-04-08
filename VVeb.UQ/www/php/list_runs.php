<?php
$output = shell_exec('ls /VVebUQ_runs/ | grep workdir');
$split_list = preg_split("/\r\n|\n|\r/",$output);
foreach ($split_list as $run)
{
  $clean_run_name = explode('workdir_',$run)[1];
  echo($clean_run_name."\n");
}
?>


<?php

// --- Get session name
if (isset($_GET['VVebUQ_session_name']))
{
  $session_name = $_GET['VVebUQ_session_name'];
}else
{
  if ($argc < 2) {exit();}
  $session_name = $argv[1];
}

// --- Get jobs inside that session
$output = shell_exec('ls /VVebUQ_runs/'.$session_name.'/ | grep workdir');
$split_list = preg_split("/\r\n|\n|\r/",$output);
foreach ($split_list as $run)
{
  $clean_run_name = explode('workdir_',$run)[1];
  echo($clean_run_name."\n");
}
?>

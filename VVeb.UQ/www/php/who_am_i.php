<?php

// --- Get run-dir
$run_dir = shell_exec('cat config.in');
$run_dir = str_replace("\n", '', $run_dir);
$name_split = explode('VVebUQ_user_', $run_dir);
if (count($name_split) == 1)
{
  $name = '';
}else
{
  $name = $name_split[1];
  $name_split = preg_split('/\//', $name);
  $name = $name_split[0];
}

echo $name;

?>

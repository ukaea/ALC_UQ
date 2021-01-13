<?php

$arguments = array();
$arguments["prominence_id_file"]  = $argv[1];
$arguments["run_name"]            = $argv[2];
$arguments["vvuq_container"]      = $argv[3];

$command = 'docker exec '.$arguments["vvuq_container"].' prominence list workflows | grep '.$arguments["run_name"];
$prominence_id = shell_exec($command);
$prominence_id = trim($prominence_id);
if ($prominence_id != '')
{
  $prominence_id = preg_split('/\s+/',$prominence_id);
  $prominence_id = trim($prominence_id[0]);
  if ($prominence_id != '')
  {
    shell_exec('echo '.$prominence_id.' > '.$arguments["prominence_id_file"]);
  }
}


exit;

?>

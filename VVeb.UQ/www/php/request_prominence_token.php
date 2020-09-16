<?php

// --- Get VVUQ software
$vvuq_container = strtolower(trim($_POST["selected_vvuq"])).'_container';

// --- If we have been called from restAPI, need to print command to terminal
if (isset($_POST["action"]))
{
  $printout_location = '';
}else
{
  $printout_location = ' &> /VVebUQ_runs/terminal_output.txt';
}

// --- Execute request
$command = 'docker exec -t '.$vvuq_container.' prominence register';
shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
$command = $command.$printout_location;
if (isset($_POST["action"]))
{
  while (@ ob_end_flush()); // end all output buffers if any
  $proc = popen($command, 'r');
  while (!feof($proc))
  {
      echo fread($proc, 4096);
      @ flush();
  }
}else
{
  shell_exec($command);
}

$command = 'docker exec -t '.$vvuq_container.' prominence login';
shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
$command = $command.$printout_location;
if (isset($_POST["action"]))
{
  while (@ ob_end_flush()); // end all output buffers if any
  $proc = popen($command, 'r');
  while (!feof($proc))
  {
      echo fread($proc, 4096);
      @ flush();
  }
}else
{
  shell_exec($command);
}

// --- Go Home! (Said Nigel Fromage)
header("Refresh: 0; Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

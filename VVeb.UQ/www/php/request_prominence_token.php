<?php

// --- Get date
$date_full = getdate();
$date = $date_full[mday]."-".$date_full[month]."-".$date_full[year];
$date = $date."---".$date_full[hours]."-".$date_full[minutes]."-".$date_full[seconds];

// --- Get Image name
$vvuq_container = $_POST["vvuq_container"];

// --- Run Prominence request from inside vvuq container
if ($vvuq_container == 'dakota')
{
  $command = 'docker exec -t dakota_container prominence register';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');
  $command = 'docker exec -t dakota_container prominence login';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');
}

// --- Go Home! (Said Nigel Fromage)
header("Refresh: 0; Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

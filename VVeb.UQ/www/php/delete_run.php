<?php

// --- Get name of containers
$run_name = 'VVebUQ_CONTAINER_'.$_GET["run_name"];
$dir_name  = 'workdir_'.$_GET["run_name"];

// --- Remove all containers
$prominence_id_file = '/VVebUQ_runs/'.$dir_name.'/prominence_workflow_id.txt';
$use_prominence = file_exists($prominence_id_file);

// --- Before checking everything, check which vvuq software we're using
$arguments = shell_exec('cat /VVebUQ_runs/'.$dir_name.'/arguments_for_vvuq_script.txt');
$arguments = preg_split('/\s+/',trim($arguments));
$selected_vvuq = trim($arguments[count($arguments)-1]);

// --- The VVUQ container name depends on the user
$who_am_i = shell_exec('php who_am_i.php');
$vvuq_container = $selected_vvuq.'_container_'.$who_am_i;

// --- Simple case with containers
if (! $use_prominence)
{
  shell_exec('for i in `docker ps -aqf name='.$run_name.' --format="{{.ID}}"` ; do docker rm -f $i ; done');
}else
{
  $prominence_id = shell_exec('cat '.$prominence_id_file);
  $prominence_id = trim($prominence_id);
  if ($prominence_id != '')
  {
    $command = 'docker exec -t '.$vvuq_container.' prominence delete '.$prominence_id;
    shell_exec($command);
    // --- We use a flag file to record that the run has bee "deleted" (because Prominence doesn't really delete the containers)
    $command = 'echo DELETED > /VVebUQ_runs/'.$dir_name.'/prominence_workflow_has_been_deleted.txt';
    shell_exec($command);
  }
}

?>

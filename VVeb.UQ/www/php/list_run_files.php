<?php

// --- Get session name
$session_name = $_GET['VVebUQ_session_name'];
  
// --- Name of run directory
$dir_name = '/VVebUQ_runs/'.$session_name.'/workdir_'.$_GET["run_name"];

// --- Count number of sub-tasks in that run
$all_sub_runs  = shell_exec('ls '.$dir_name.' | grep workdir_VVebUQ | grep -v ".json"');
$all_sub_runs  = preg_split("/\r\n|\n|\r/",$all_sub_runs);
$n_runs = count($all_sub_runs) - 1;

$prominence_id_file = $dir_name.'/prominence_workflow_id.txt';
$use_prominence = file_exists($prominence_id_file);

// --- Before checking everything, check which vvuq software we're using
$arguments = shell_exec('cat '.$dir_name.'/arguments_for_vvuq_script.txt');
$arguments = preg_split('/\s+/',trim($arguments));
$selected_vvuq = trim($arguments[count($arguments)-2]);

// --- The VVUQ container name depends on the user
$vvuq_container = $selected_vvuq.'_container_'.$session_name;

// --- Simple case with containers
$all_files = array();
if (! $use_prominence)
{
  // --- Get list of files and folders
  $command = 'ls -p '.$dir_name.'/'.$all_sub_runs[0].'/';
  $command = $command.' | grep -v "arguments_for_vvuq_script.txt"';
  $command = $command.' | grep -v "dakota_params"';
  $command = $command.' | grep -v "dakota_results"';
  $all_files = shell_exec($command);
  $all_files = preg_split("/\r\n|\n|\r/",$all_files);
}else
{
  $prominence_id = shell_exec('cat '.$prominence_id_file);
  $prominence_id = trim($prominence_id);
  if ($prominence_id != '')
  {
    $command = 'docker exec -t '.$vvuq_container.' prominence list jobs '.$prominence_id.' --all';
    $containers = shell_exec($command);
    $containers_lines = preg_split('/\R/',$containers);
    if (count($containers_lines) > 2)
    {
      $containers_2nd_line = str_replace('/\R/','',$containers_lines[1]);
      if ($containers_2nd_line != '')
      {
        // --- Get format line
        $format = $containers_lines[0];
        $ID_position = preg_split('/\s+/',$format);
        for ($i=0 ; $i< count($ID_position) ; $i++)
        {
          if ($ID_position[$i] == 'ID')
          {
            $ID_position = $i;
            break;
          }
        }
        // --- Just get the first job
        for ($i=1 ; $i< count($containers_lines) ; $i++)
        {
          if ($containers_lines[$i] == '') {continue;}
          $prominence_job_id = preg_split('/\s+/',$containers_lines[$i])[$ID_position];
          break;
        }
        // --- Record new containers list
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'rm /'.$selected_vvuq.'_dir/workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'prominence download '.$prominence_job_id.'\'';
        $success = shell_exec($command);
        if ( (strpos($success,'workdir_VVebUQ') !== false) && (strpos($success,'Downloading file') !== false) )
        {
          $command = 'docker exec -t '.$vvuq_container.' bash -c \'tar -xvzf /'.$selected_vvuq.'_dir/workdir_VVebUQ.*.tgz\'';
          $success = shell_exec($command);
          $command = 'docker exec -t '.$vvuq_container.' bash -c \'rm /'.$selected_vvuq.'_dir/workdir_VVebUQ.*.tgz\'';
          $success = shell_exec($command);
          $command = 'docker exec -t '.$vvuq_container.' bash -c \'ls -p /'.$selected_vvuq.'_dir/workdir_VVebUQ.*/';
          $command = $command.' | grep -v "arguments_for_vvuq_script.txt"';
          $command = $command.' | grep -v "dakota_params"';
          $command = $command.' | grep -v "dakota_results"';
          $command = $command.'\'';
	  $fullcontent = shell_exec($command);
          $all_files = preg_split('/\R/',$fullcontent);
          $command = 'docker exec -t '.$vvuq_container.' bash -c \'rm -f /'.$selected_vvuq.'_dir/workdir_VVebUQ.*\'';
          $success = shell_exec($command);
        }
      }
    }
  }
}

// --- Return everything
echo("This run contains ".$n_runs." sub-tasks\n");
if (count($all_files) > 2)
{
  echo("At first sight, each sub-task contains\n");
  for ($i=0 ; $i<count($all_files) ; $i++)
  {
    if ($all_files[$i] != '') {echo("  ".$all_files[$i]."\n");}
  }
}else
{
  echo("At first sight, the sub-tasks do not contain anything\n");
}

?>

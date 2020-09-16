<?php

// --- Get name of run
$run_name = $_GET["run_name"];

// --- Check if we are using Prominence
$dir_name = $run_name;
$dir_name = str_replace("VVebUQ_CONTAINER_","",$dir_name);
$dir_name = "workdir_".$dir_name;
$prominence_id_file = '/VVebUQ_runs/'.$dir_name.'/prominence_workflow_id.txt';
$use_prominence = file_exists($prominence_id_file);

// --- Before checking everything, check if job is stil being prepared
if (file_exists('/VVebUQ_runs/'.$dir_name.'/JOB_BEING_PREPARED_FOR_SUBMISSION.txt'))
{
  echo "Your job is being prepared for submission...\n";
  exit();
}

// --- Before checking everything, check which vvuq software we're using
$arguments = shell_exec('cat /VVebUQ_runs/'.$dir_name.'/arguments_for_vvuq_script.txt');
$arguments = preg_split('/\s+/',trim($arguments));
$selected_vvuq = trim($arguments[count($arguments)-1]);

// --- Simple case with containers
if (! $use_prominence)
{
  $command = 'docker ps -aqf name='.$run_name.' --format="table {{.Image}}\\t{{.ID}}\\t{{.RunningFor}}\\t{{.Status}}" ';
  $containers = shell_exec($command);
}else
{
  $prominence_id = shell_exec('cat '.$prominence_id_file);
  $prominence_id = trim($prominence_id);
  $prominence_job_has_been_deleted = '/VVebUQ_runs/'.$dir_name.'/prominence_workflow_has_been_deleted.txt';
  $prominence_job_has_been_deleted = file_exists($prominence_job_has_been_deleted);
  if ( ($prominence_id == '') || ($prominence_job_has_been_deleted) )
  {
    $containers = "ID   NAME   CREATED               STATUS   ELAPSED      IMAGE   CMD\n";
  }else
  {
    // --- Get list of jobs from that workflow
    $command = 'docker exec -t '.$selected_vvuq.'_container prominence list jobs '.$prominence_id.' --all';
    $containers = shell_exec($command);
    $containers_lines = preg_split('/\R/',$containers);
    if (count($containers_lines) > 2)
    {
      $containers_2nd_line = $containers_lines[1];
      $containers_2nd_line = str_replace('/\R/',"",$containers_2nd_line);
      if ($containers_2nd_line != '')
      {
        // --- NAMEs are usually very long, cut them
        $format = $containers_lines[0];
        $NAME_length = explode('NAME',$format)[1];
        $next_print = preg_split('/\s+/',$NAME_length)[1];
        $NAME_length = strlen(explode($next_print,$NAME_length)[0]);
        $NAME_position = preg_split('/\s+/',$format);
        for ($i=0 ; $i< count($NAME_position) ; $i++)
        {
          if ($NAME_position[$i] == 'NAME')
          {
            $NAME_position = $i;
            break;
          }
        }
        $first_line = preg_split('/\R/',$containers)[1];
	$full_name = preg_split('/\s+/',$first_line)[$NAME_position];
        $workflow_name = preg_split('/\//',$full_name)[0];
        $workflow_name_length = strlen($workflow_name) + 1;
        $subjob_name = preg_split('/\//',$full_name)[1];
        // --- Create new NAME+spaces with less spaces
        $NAME_new = 'NAME';
        for ($i=0 ; $i< $NAME_length-$workflow_name_length ; $i++) {$NAME_new = $NAME_new.' ';}
        // --- Replace NAME+spaces in format line
        $containers_new = $containers_lines[0];
        $containers_new = explode("NAME",$containers_new);
        $containers_new = $containers_new[0].$NAME_new.trim($containers_new[1])."\n";
        // --- Remove workflow identifier from job NAME
        for ($i=1 ; $i< count($containers_lines) ; $i++)
        {
          if ($containers_lines[$i] == '') {continue;}
          $str_tmp = $containers_lines[$i];
          $str_tmp = str_replace($workflow_name."/","",$str_tmp);
          $containers_new = $containers_new.$str_tmp."\n";
        }
        // --- Record new containers list
        $containers = $containers_new;
      }else
      {
        $containers = "ID   NAME   CREATED               STATUS   ELAPSED      IMAGE   CMD\n";
      }
    }else
    {
      $containers = "ID   NAME   CREATED               STATUS   ELAPSED      IMAGE   CMD\n";
    }
  }
}

// --- Return result
echo $containers;
exit();

?>

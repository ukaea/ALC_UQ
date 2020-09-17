<?php

// --- Get run directory
$run_name = $_GET["run_name"];
$dir_name  = 'workdir_'.$run_name;

// --- Create zip file of entire run
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
  shell_exec('cd /VVebUQ_runs/ ; rm -f '.$run_name.'.zip ; cd -');
  shell_exec('cd /VVebUQ_runs/ ; zip -r '.$run_name.'.zip ./'.$dir_name.' ; cd -');
}else
{
  $prominence_id = shell_exec('cat '.$prominence_id_file);
  $prominence_id = trim($prominence_id);
  if ($prominence_id == '')
  {
    $containers = '';
  }else
  {
    $command = 'docker exec -t '.$vvuq_container.' prominence list jobs '.$prominence_id.' --all';
    $containers = shell_exec($command);
    $containers_lines = preg_split('/\R/',$containers);
    if (count($containers_lines) > 2)
    {
      $containers_2nd_line = $containers_lines[1];
      $containers_2nd_line = str_replace('/\R/',"",$containers_2nd_line);
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
        // --- First remove existing files
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'rm /'.$selected_vvuq.'_dir/workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
        // --- Download each job
        for ($i=1; $i< count($containers_lines); $i++)
        {
          if (trim($containers_lines[$i]) == '') {continue;}
          $prominence_job_id = preg_split('/\s+/',$containers_lines[$i])[$ID_position];
          $command = 'docker exec -t '.$vvuq_container.' bash -c \'prominence download '.$prominence_job_id.'\'';
          $success = shell_exec($command);
        }
        // --- zip everything together
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'cd /'.$selected_vvuq.'_dir/ ; rm -f '.$run_name.'.zip ; zip '.$run_name.'.zip workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
        // --- Remove tarballs
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'rm /'.$selected_vvuq.'_dir/workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
        // --- Move zip to right place
        $command = 'docker exec -t '.$vvuq_container.' bash -c \'mv /'.$selected_vvuq.'_dir/'.$run_name.'.zip /VVebUQ_runs/\'';
        $success = shell_exec($command);
      }
    }
  }
}


// --- Move zip file to downloads/
shell_exec('mkdir -p ../downloads ; mv /VVebUQ_runs/'.$run_name.'.zip ../downloads/');

// --- We read file into output only for the restAPI
if (! isset($_GET["get_back_to_js"]))
{
  readfile('../downloads/'.$run_name.'.zip');
}

?>

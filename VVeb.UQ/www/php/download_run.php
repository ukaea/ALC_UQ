<?php

// --- Get session name
$session_name = $_GET['VVebUQ_session_name'];

// --- Get run directory
$run_name = $_GET["run_name"];
$dir_name  = 'workdir_'.$run_name;

// --- Create zip file of entire run
$prominence_id_file = '/VVebUQ_runs/'.$session_name.'/'.$dir_name.'/prominence_workflow_id.txt';
$use_prominence = file_exists($prominence_id_file);

// --- Before checking everything, check which vvuq software we're using
$arguments = shell_exec('cat /VVebUQ_runs/'.$session_name.'/'.$dir_name.'/arguments_for_vvuq_script.txt');
$arguments = preg_split('/\s+/',trim($arguments));
$selected_vvuq = trim($arguments[count($arguments)-2]);

// --- The VVUQ container name depends on the user
$vvuq_container = $selected_vvuq.'_container_'.$session_name;

// --- Note: The download location depends on the user, and on Prominence vs. the app
// --- There are two download locations: the one for Prominence, which needs to be inside the VVUQ container
// --- And the one from the app itself, which needs to be accessible from /var/www/html/
// --- They are both the same mounted dir, but the name in the app is /var/www/html/VVebUQ_downloads/
// --- whereas it's just /VVebUQ_downloads/ in the VVUQ container
$download_dir = '/var/www/html/VVebUQ_downloads/'.$session_name.'/';
shell_exec('mkdir -p '.$download_dir);

// --- Simple case with containers
if (! $use_prominence)
{
  shell_exec('cd '.$download_dir.' ; rm -f '.$run_name.'.zip ; cd -');
  shell_exec('cd /VVebUQ_runs/'.$session_name.'/ ; zip -r '.$download_dir.$run_name.'.zip '.$dir_name.' ; cd -');
}else
{
  $download_dir = '/VVebUQ_downloads/'.$session_name.'/';
  $command = 'docker exec -w '.$download_dir.' -t '.$vvuq_container.' bash -c \'rm -f '.$run_name.'.zip\'';
  $success = shell_exec($command);
  $arguments_update_id = $prominence_id_file.' '.$run_name.' '.$vvuq_container;
  shell_exec('php ../php/update_prominence_id.php '.$arguments_update_id.' > /dev/null &');
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
        $command = 'docker exec -w '.$download_dir.' -t '.$vvuq_container.' bash -c \'rm workdir_VVebUQ.*.tgz *.zip\'';
        $success = shell_exec($command);
        // --- Download each job
        for ($i=1; $i< count($containers_lines); $i++)
        {
          if (trim($containers_lines[$i]) == '') {continue;}
          $prominence_job_id = preg_split('/\s+/',$containers_lines[$i])[$ID_position];
          $command = 'docker exec -w '.$download_dir.' -t '.$vvuq_container.' bash -c \'prominence download '.$prominence_job_id.'\'';
          $success = shell_exec($command);
        }
        // --- zip everything together
        $command = 'docker exec -w '.$download_dir.' -t '.$vvuq_container.' bash -c \'zip '.$run_name.'.zip workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
        // --- Remove tarballs
        $command = 'docker exec -w '.$download_dir.' -t '.$vvuq_container.' bash -c \'rm workdir_VVebUQ.*.tgz\'';
        $success = shell_exec($command);
      }
    }
  }
}

// --- We read file into output only for the restAPI
if (! isset($_GET["get_back_to_js"]))
{
  $download_dir = '/var/www/html/VVebUQ_downloads/'.$session_name.'/';
  readfile($download_dir.$run_name.'.zip');
}

?>

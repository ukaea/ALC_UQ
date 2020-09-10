<?php

// --- Get date
$date_full = getdate();
$date = $date_full[mday]."-".$date_full[month]."-".$date_full[year];
$date = $date."---".$date_full[hours]."-".$date_full[minutes]."-".$date_full[seconds];

// --- Get Image name
$image_name = trim($_POST["docker_image_run"]);
$container_name = $image_name;
$container_name = str_replace('/','_',$container_name);
$container_name = str_replace(':','_',$container_name);
$workdir_name   = 'workdir_'.$date.'_'.$container_name;
$container_name = 'VVebUQ_CONTAINER_'.$date.'_'.$container_name;

// --- Get the number of cpu available (THIS NEEDS TO BE GENERALISED PROPERLY!!!)
$n_cpu = (int)trim($_POST["n_cpu"]);

// --- Get the file name
$filename = trim($_POST["input_file_name"]);

// --- Get the format of the input file
$file_ext = trim($_POST["input_file_type"]);
$file_type = 'netcdf';
if ($file_ext == 'csv') {$file_type = 'csv';}

// --- Get the file name
$data_filename = trim($_POST["input_data_file_name"]);

// --- Get run-dir
$run_dir = shell_exec('cat config.in');
$run_dir = str_replace("\n", '', $run_dir);
$name_split = preg_split('/VVeb.UQ/', $run_dir);
$dakota_dir = $name_split[0].'user_interface/';

// --- Are we running with Prominence or locally?
$use_prominence = trim($_POST["use_prominence"]);

// --- Produce files in run directory of container
$work_dir        = '/VVebUQ_runs';
$base_dir        = $work_dir.'/'.$workdir_name;
$mount_dir       = $run_dir.$workdir_name;
$files_dir       = $base_dir.'/files_for_dakota';
$input_file      = $work_dir.'/'.$filename;
$data_input_file = $work_dir.'/'.$data_filename;
$args_file       = $files_dir.'/arguments_for_dakota_script.txt';
shell_exec('mkdir -p '.$base_dir);
shell_exec('mkdir -p '.$files_dir);
shell_exec('cp '.$input_file.' '.$files_dir.'/'.$filename);
shell_exec('cp '.$data_input_file.' '.$files_dir.'/'.$data_filename);
shell_exec('cp ../interfaces/run_script.py '.$base_dir.'/');
shell_exec('chmod +x '.$base_dir.'/run_script.py');
shell_exec('printf \''.$container_name.' '.$mount_dir.' '.$image_name.' '.$filename.' '.$file_type.' '.$data_filename.' '.$dakota_dir.' '.$use_prominence.'\' > '.$args_file);

// --- Produce Dakota input file based on netcdf file provided by user
$command = 'docker exec -w '.$base_dir.' -t dakota_container python3 /dakota_user_interface/python/main.py -d run_script.py -c '.$n_cpu.' -i '.$input_file.' -o '.$base_dir.'/dakota_run.in -t '.$file_type;
echo $command;
shell_exec($command);

// --- Run Container
$command = 'docker exec -w '.$base_dir.' -t dakota_container dakota -i ./dakota_run.in -o dakota_run.out';
shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');

// --- When using Prominence, the dakota commands prepares all the .json jobs, which are submitted as a workflow
if ($use_prominence == 'true')
{
  // --- Upload Dakota user interface
  $command = 'docker exec -t dakota_container tar -cvzf dakota_user_interface.tgz /dakota_user_interface';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');
  $command = 'docker exec -t dakota_container prominence upload --filename=dakota_user_interface.tgz --name=dakota_user_interface.tgz';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');
  // --- Get job files
  $prominence_job_file = `ls $base_dir/workdir_VVebUQ*.json`;
  $prominence_job_file = preg_split('/\s+/', $prominence_job_file);
  $prominence_jobs = array();
  foreach($prominence_job_file as &$file)
  {
    $filename = $file;
    if (is_dir($filename)) continue;
    if (! file_exists($filename)) continue;
    $job = `cat $filename`;
    $job_json = json_decode($job);
    array_push($prominence_jobs, $job_json);
  }
  // --- Create workflow
  $workflow = array( "name" => $workdir_name, "jobs" => $prominence_jobs);
  $workflow_json = json_encode($workflow);
  $workflow_filename = $base_dir.'/prominence_workflow.json';
  file_put_contents($workflow_filename, $workflow_json);
  // --- Submit workflow
  $command = 'docker exec -w '.$base_dir.' -t dakota_container prominence run '.$workflow_filename;
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
  $prominence_output = shell_exec($command);
  shell_exec('printf \''.$prominence_output.'\n\' &> /VVebUQ_runs/terminal_output.txt');
  $workflow_id = explode('Workflow created with id ', $prominence_output);
  $workflow_id = trim($workflow_id[1]);
  shell_exec('printf \''.$workflow_id.'\' > '.$base_dir.'/prominence_workflow_id.txt');
  // --- Prominence might take a few seconds internally to get everything ready, wait
  sleep(5);
}

// --- Go Home! (Said Nigel Fromage)
header("Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

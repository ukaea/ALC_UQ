<?php

// --- The arguments are given through POST when using the web-front
// --- However, they are given as normal variables when using the rest-API
// --- This is to allow this call to be asynchronous when using the rest-API
$arguments = array();
if (isset($_POST["docker_image_run"]))
{
  $arguments["docker_image_run"]     = $_POST["docker_image_run"];
  $arguments["n_cpu"]                = $_POST["n_cpu"];
  $arguments["input_file_name"]      = $_POST["input_file_name"];
  $arguments["input_file_type"]      = $_POST["input_file_type"];
  $arguments["input_data_file_name"] = $_POST["input_data_file_name"];
  $arguments["use_prominence"]       = $_POST["use_prominence"];
}else
{
  if ($argc < 7) {exit();}
  $arguments["docker_image_run"]     = $argv[1];
  $arguments["n_cpu"]                = $argv[2];
  $arguments["input_file_name"]      = $argv[3];
  $arguments["input_file_type"]      = $argv[4];
  $arguments["input_data_file_name"] = $argv[5];
  $arguments["use_prominence"]       = $argv[6];
}

// --- Get date
$date_full = getdate();
$date = $date_full[year]."-".$date_full[mon]."-".$date_full[mday];
$date = $date."---".$date_full[hours]."-".$date_full[minutes]."-".$date_full[seconds];

// --- Get Image name
$image_name = trim($arguments["docker_image_run"]);
$container_name = $image_name;
$container_name = str_replace('/','_',$container_name);
$container_name = str_replace(':','_',$container_name);
$workdir_name   = 'workdir_'.$date.'_'.$container_name;
$container_name = 'VVebUQ_CONTAINER_'.$date.'_'.$container_name;

// --- Get the number of cpu available (THIS NEEDS TO BE GENERALISED PROPERLY!!!)
$n_cpu = (int)trim($arguments["n_cpu"]);

// --- To keep safe, we always force Dakota in serial
// --- This is because it can lead to containers being launched at the same time
// --- without knowing about one another, which can result in the containers running
// --- on the same cores. This can be very bad when you launch a lot of MPI containers at the same time...
$n_cpu_dakota = 1;

// --- Get the file name
$filename = trim($arguments["input_file_name"]);

// --- Get the format of the input file
$file_ext = trim($arguments["input_file_type"]);
$file_type = 'netcdf';
if ($file_ext == 'csv') {$file_type = 'csv';}

// --- Get the file name
$data_filename = trim($arguments["input_data_file_name"]);

// --- Get run-dir
$run_dir = shell_exec('cat config.in');
$run_dir = str_replace("\n", '', $run_dir);
$name_split = preg_split('/VVeb.UQ/', $run_dir);
$dakota_dir = $name_split[0].'user_interface/';

// --- Are we running with Prominence or locally?
$use_prominence = trim($arguments["use_prominence"]);

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
shell_exec('printf \''.$container_name.' '.$mount_dir.' '.$image_name.' '.$filename.' '.$file_type.' '.$data_filename.' '.$dakota_dir.' '.$use_prominence.' '.$n_cpu.'\' > '.$args_file);

// --- Before starting, we create a flag file to inform that the job is being prepared
shell_exec('echo "JOB_BEING_PREPARED_FOR_SUBMISSION" > '.$base_dir.'/JOB_BEING_PREPARED_FOR_SUBMISSION.txt');

// --- Produce Dakota input file based on netcdf file provided by user
$command = 'docker exec -w '.$base_dir.' -t dakota_container python3 /dakota_user_interface/python/main.py -d run_script.py -c '.$n_cpu_dakota.' -i '.$input_file.' -o '.$base_dir.'/dakota_run.in -t '.$file_type;
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

// --- Once we finished, we can remove the flag file
shell_exec('rm '.$base_dir.'/JOB_BEING_PREPARED_FOR_SUBMISSION.txt');

// --- Go Home! (Said Nigel Fromage)
header("Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

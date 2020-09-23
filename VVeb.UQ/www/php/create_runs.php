<?php

// --- The arguments are given through POST when using the web-front
// --- However, they are given as normal variables when using the rest-API
// --- This is to allow this call to be asynchronous when using the rest-API
$arguments = array();
if (isset($_POST["docker_image_run"]))
{
  $arguments["docker_image_run"]     = $_POST["docker_image_run"];
  $arguments["selected_vvuq"]        = $_POST["selected_vvuq"];
  $arguments["n_cpu"]                = $_POST["n_cpu"];
  $arguments["input_file_name"]      = $_POST["input_file_name"];
  $arguments["input_file_type"]      = $_POST["input_file_type"];
  $arguments["input_data_file_name"] = $_POST["input_data_file_name"];
  $arguments["use_prominence"]       = $_POST["use_prominence"];
  $arguments["VVebUQ_session_name"]  = $_POST['VVebUQ_session_name'];
}else
{
  if ($argc < 9) {exit();}
  $arguments["docker_image_run"]     = $argv[1];
  $arguments["selected_vvuq"]        = $argv[2];
  $arguments["n_cpu"]                = $argv[3];
  $arguments["input_file_name"]      = $argv[4];
  $arguments["input_file_type"]      = $argv[5];
  $arguments["input_data_file_name"] = $argv[6];
  $arguments["use_prominence"]       = $argv[7];
  $arguments["VVebUQ_session_name"]  = $argv[8];
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
$container_name = 'VVebUQ_CONTAINER_'.$arguments["VVebUQ_session_name"].'_'.$date.'_'.$container_name;

// --- Get the number of cpu available (THIS NEEDS TO BE GENERALISED PROPERLY!!!)
$n_cpu = (int)trim($arguments["n_cpu"]);

// --- The Dakota run itself will prepare all the directories, which can be done in parallel
// --- By default we use however many processes are available to do this (minus 1 for the app itself)
$n_cpu_dakota = intval(shell_exec('nproc')) - 1;
$n_cpu_dakota = max(1,$n_cpu_dakota);

// --- Get the file name
$filename = trim($arguments["input_file_name"]);

// --- Get the format of the input file
$file_ext = trim($arguments["input_file_type"]);
$file_type = 'netcdf';
if ($file_ext == 'csv') {$file_type = 'csv';}

// --- Get the additional-data file name
$data_filename = trim($arguments["input_data_file_name"]);

// --- Get mount-paths
$mount_paths = shell_exec('php ../php/get_mount_paths.php');
$run_dir        = trim(explode(',',$mount_paths)[0]);
$user_inter_dir = trim(explode(',',$mount_paths)[1]);

// --- The VVUQ container name depends on the user
$vvuq_container = $arguments["selected_vvuq"].'_container_'.$arguments["VVebUQ_session_name"];

// --- Are we running with Prominence or locally?
$use_prominence = trim($arguments["use_prominence"]);

// --- Produce files in run directory of container
$work_dir        = '/VVebUQ_runs/'.$arguments["VVebUQ_session_name"];
$base_dir        = $work_dir.'/'.$workdir_name;
$mount_dir       = $run_dir.$arguments["VVebUQ_session_name"].'/'.$workdir_name;
$files_dir       = $base_dir.'/files_for_'.$arguments["selected_vvuq"]; // either files_for_dakota or files_for_easyvvuq
$input_file      = $work_dir.'/'.$filename;
$data_input_file = $work_dir.'/'.$data_filename;
shell_exec('mkdir -p '.$base_dir);
shell_exec('mkdir -p '.$files_dir);
shell_exec('cp '.$input_file.' '.$files_dir.'/'.$filename);
shell_exec('cp '.$data_input_file.' '.$files_dir.'/'.$data_filename);
shell_exec('cp ../interfaces/* '.$base_dir.'/');
shell_exec('mv '.$base_dir.'/run_script_'.$arguments["selected_vvuq"].'.py '.$base_dir.'/run_script.py');
shell_exec('chmod +x '.$base_dir.'/*.py');

// --- Set arguments to be found by run_script
$arguments_file = '';
$arguments_file = $arguments_file.' '.$container_name;
$arguments_file = $arguments_file.' '.$mount_dir;
$arguments_file = $arguments_file.' '.$image_name;
$arguments_file = $arguments_file.' '.$filename;
$arguments_file = $arguments_file.' '.$file_type;
$arguments_file = $arguments_file.' '.$data_filename;
$arguments_file = $arguments_file.' '.$user_inter_dir;
$arguments_file = $arguments_file.' '.$use_prominence;
$arguments_file = $arguments_file.' '.$n_cpu;
$arguments_file = $arguments_file.' '.$arguments["selected_vvuq"];
$arguments_file = $arguments_file.' '.$arguments["VVebUQ_session_name"];
$args_file = $files_dir.'/arguments_for_vvuq_script.txt';
shell_exec('printf \''.$arguments_file.'\' > '.$args_file);
$args_file = $base_dir.'/arguments_for_vvuq_script.txt';
shell_exec('printf \''.$arguments_file.'\' > '.$args_file);

// --- Before starting, we create a flag file to inform that the job is being prepared
shell_exec('echo "JOB_BEING_PREPARED_FOR_SUBMISSION" > '.$base_dir.'/JOB_BEING_PREPARED_FOR_SUBMISSION.txt');

// --- Produce VVUQ input file (for Dakota) or python script (for easyvvuq) based on netcdf file provided by user
if ($arguments["selected_vvuq"] == 'dakota')
{
  $command_user_interface = 'python3 /vvuq_user_interface/python/main.py';
  $out_file_user_interface = 'dakota_run.in';
  $command_vvuq = 'dakota -i ./dakota_run.in -o dakota_run.out';
}else
{
  $command_user_interface = './fake_user_interface_easyvvuq.py';
  $out_file_user_interface = 'easyvvuq_main.py';
  $command_vvuq = 'python3 easyvvuq_main.py';
}
// --- Launch VVUQ input command
$command = 'docker exec -w '.$base_dir.' -t '.$vvuq_container.' '.$command_user_interface.' -d run_script.py -c '.$n_cpu_dakota.' -i '.$input_file.' -o '.$base_dir.'/'.$out_file_user_interface.' -t '.$file_type;
shell_exec($command);
// --- Run VVUQ software with fake output, just to prepare the run-directories
$command = 'docker exec -w '.$base_dir.' -t '.$vvuq_container.' '.$command_vvuq;
shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_output.txt');

// --- Rename directories if we used easyvvuq
if ($arguments["selected_vvuq"] == 'easyvvuq')
{
  $run_directories = shell_exec('ls '.$base_dir.'/easyvvuq_campaign*/runs/ | grep Run_');
  $run_directories = preg_split('/\s+/',$run_directories);
  foreach ($run_directories as $run_dir_tmp)
  {
    if ($run_dir_tmp != '')
    {
      $run_dir_new = explode('Run_',$run_dir_tmp);
      $run_dir_new = 'workdir_VVebUQ.'.$run_dir_new[1];
      $command = 'mv '.$base_dir.'/easyvvuq_campaign*/runs/'.$run_dir_tmp.' '.$base_dir.'/'.$run_dir_new;
      shell_exec($command);
    }
  }
}
	
// --- Submit the workflow
if ($use_prominence == 'true')
{
  $command = 'docker exec -w '.$base_dir.' -t '.$vvuq_container.' ./submit_prominence_workflow.py';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_output.txt');
  // --- Prominence might take a few seconds internally to get everything ready, wait
  sleep(5);
}else
{
  $command = 'docker exec -w '.$base_dir.' -t '.$vvuq_container.' ./submit_local_workflow.py';
  shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_command.txt');
  shell_exec($command.' &> /VVebUQ_runs/'.$arguments["VVebUQ_session_name"].'/terminal_output.txt');
}

// --- Once we finished, we can remove the flag file
shell_exec('rm '.$base_dir.'/JOB_BEING_PREPARED_FOR_SUBMISSION.txt');

// --- Go Home! (Said Nigel Fromage)
header("Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

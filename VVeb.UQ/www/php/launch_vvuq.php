<?php


// --- Get session name
$session_name = $_POST['VVebUQ_session_name'];

// --- Get Form Variables
$image_name = $_POST["docker_image"];
$container_name = $_POST["container_name"];
$mount_paths = shell_exec('php ../php/get_mount_paths.php');
$run_dir        = trim(explode(',',$mount_paths)[0]);
$user_inter_dir = trim(explode(',',$mount_paths)[1]);
$download_dir   = trim(explode(',',$mount_paths)[2]);

// --- Check if container already running
$command = 'docker ps -aqf name='.$container_name.' --filter status=running';
$container_running = shell_exec($command);
if (trim($container_running) != '')
{
  if (isset($_POST['action']))
  {
    echo "An instance of ".$image_name." is already running!\n";
    exit;
  }else
  {
    header("Location: {$_SERVER['HTTP_REFERER']}");
    exit;
  }
}

// --- Run Container
$command = 'docker container run --privileged --name '.$container_name.' -v /var/run/docker.sock:/var/run/docker.sock -v '.$run_dir.':/VVebUQ_runs/ -v '.$user_inter_dir.':/VVebUQ_user_interface/ -v '.$download_dir.':/VVebUQ_downloads/ -id '.$image_name;
shell_exec('printf \''.$command.'\n\' > /VVebUQ_runs/'.$session_name.'/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/'.$session_name.'/terminal_output.txt');

// --- Go Home! (Said Nigel Fromage)
// --- Check if container already running
$command = 'docker ps -aqf name='.$container_name.' --filter status=running';
$container_running = shell_exec($command);
if (trim($container_running) != '')
{
  if (isset($_POST['action']))
  {
    echo "An instance of ".$image_name." has been launched\n";
    exit;
  }else
  {
    header("Location: {$_SERVER['HTTP_REFERER']}");
    exit;
  }
}

?>

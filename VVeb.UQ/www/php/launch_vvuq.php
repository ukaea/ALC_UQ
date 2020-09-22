<?php


// --- Get session name
$session_name = $_POST['VVebUQ_session_name'];

// --- Get Form Variables
$image_name = $_POST["docker_image"];
$container_name = $_POST["container_name"];
$run_dir = shell_exec('cat config.in | grep APP_DIRECTORY');
$run_dir = explode(' = ',$run_dir)[1];
$run_dir = trim(str_replace("\n", '', $run_dir));
$name_split = preg_split('/VVeb.UQ/', $run_dir);
$user_inter_dir = $name_split[0].'user_interface/';
#$run_dir = $run_dir.$session_name.'/';

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
$command = 'docker container run --privileged --name '.$container_name.' -v /var/run/docker.sock:/var/run/docker.sock -v '.$run_dir.':/VVebUQ_runs/ -v '.$user_inter_dir.':/vvuq_user_interface/ -id '.$image_name;
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

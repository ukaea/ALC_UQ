<?php

// --- GET the username
$username = strtolower(trim($_GET["username"]));
if ($username == '')
{
  echo "Please provide a valid username\n";
  exit;
}

// --- Get run-dir required for Docker-mounts
$run_dir = shell_exec('cat config.in');
$run_dir = str_replace("\n", '', $run_dir);
$name_split = preg_split('/VVeb.UQ/', $run_dir);
$user_inter_dir = $name_split[0].'user_interface/';

// --- Check existing user workdirs in main directory
$workdirs = shell_exec('ls /VVebUQ_runs/ | grep VVebUQ_user_ | grep port');
$workdirs = preg_split('/\s+/', $workdirs);
$user_already_has_session = false;
$session_name = '';
$existing_ports = array();
for ($i=0; $i<count($workdirs); $i++)
{
  if (trim($workdirs[$i]) != '')
  {
    if(strpos($workdirs[$i], $username) !== false)
    {
      $user_already_has_session = true;
      $session_healthy = true;
      $session_name = trim($workdirs[$i]);
      $session_port = explode('VVebUQ_user_'.$username.'_port_',trim($workdirs[$i]))[1];
      // --- CHeck session isn't broken
      $container_name = 'vvebuq_app_'.$session_name;
      $command = 'docker exec -it '.$container_name.' cat /var/www/html/php/config.in';
      $existing_config = trim(shell_exec($command));
      if ($existing_config == '')
      {
        $session_healthy = false;
      }
    }
    $port = explode('VVebUQ_user_'.$username.'_port_',trim($workdirs[$i]))[1];
    array_push($existing_ports, $port);
  }
}

// --- Act depending if a session already exists
if ($user_already_has_session && $session_healthy)
{
  
  $session_address = $_SERVER['HTTP_REFERER'];
  $session_address = explode(':',trim($session_address));
  $session_address = $session_address[0].':'.$session_address[1].':'.$session_port;  // because http://IP:port
  echo 'You already have a session running, please follow this link:<br/><a href="'.$session_address.'">'.$session_address.'</a>';
}else
{
  if (! $user_already_has_session)
  {
    // --- Create new PORT id
    $session_port = rand(50000,59999);
    while (true)
    {
      if (in_array($session_port,$existing_ports))
      {
        $session_port = rand(50000,59999);
      }else
      {
        break;
      }
    }
  }
  // --- Create new workdir for user
  $session_name = 'VVebUQ_user_'.$username.'_port_'.$session_port;
  $new_workdir = '/VVebUQ_runs/'.$session_name;
  shell_exec('mkdir -p '.$new_workdir);
  $workdir_mount = $run_dir.$session_name.'/';
  $session_address = $_SERVER['HTTP_REFERER'];
  $session_address = explode(':',trim($session_address));
  $session_address = $session_address[0].':'.$session_address[1].':'.$session_port;  // because http://IP:port
  // --- Launch new container
  $container_name = 'vvebuq_app_'.$session_name;
  $command = 'docker container run --privileged --name '.$container_name.' -v /var/run/docker.sock:/var/run/docker.sock -v '.$workdir_mount.':/VVebUQ_runs/ -v '.$user_inter_dir.':/vvuq_user_interface/ -p '.$session_port.':80 -d vvebuq';
  shell_exec($command);
  // --- Make sure config.in is up to date in new container
  shell_exec('echo "'.$workdir_mount.'" > /var/www/html/php/config.in.tmp');
  $command = 'docker cp /var/www/html/php/config.in.tmp '.$container_name.':/var/www/html/php/config.in';
  shell_exec($command);
  // --- Return link of new session to user
  echo 'You already have a session running, please follow this link:<br/><a href="'.$session_address.'">'.$session_address.'</a>';
}

exit;

?>

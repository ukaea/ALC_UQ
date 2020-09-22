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

// --- Check existing user workdirs in main directory
$workdirs = shell_exec('ls /VVebUQ_runs/ | grep VVebUQ_user_ | grep _id_');
$workdirs = preg_split('/\s+/', $workdirs);
$user_already_has_session = false;
$session_name = '';
for ($i=0; $i<count($workdirs); $i++)
{
  if (trim($workdirs[$i]) != '')
  {
    if(strpos($workdirs[$i], $username) !== false)
    {
      $user_already_has_session = true;
      $session_name = trim($workdirs[$i]);
      $user_hash = explode('VVebUQ_user_'.$username.'_id_',trim($workdirs[$i]));
      $user_hash = $user_hash[1];
    }
  }
}

// --- Get address we're at
$session_address = $_SERVER['HTTP_REFERER'];
if (trim($session_address) == '')
{
  $session_address = $_SERVER['HTTP_HOST'];
}
// --- Make sure we have http at the beginning of our address
if(! (strpos($session_address, "http") !== false) )
{
  $session_address = 'http://'.$session_address;
}
// --- Make sure we have / at the end
if (substr($session_address, -1) != '/')
{
  $session_address = $session_address.'/';
}

// --- Act depending if a session already exists
if ($user_already_has_session)
{
  // --- Refer user to his already allocated address
  $session_address = $session_address.$user_hash.'/';
  if (isset($_GET['FROM_WEB_FRONT']))
  {
    echo 'You already have a session running, please follow this link:<br/><a href="'.$session_address.'">'.$session_address.'</a>';
  }else
  {
    echo "You already have a session running, please follow this link:\n";
    echo $session_address."\n";
  }
}else
{
  // --- For new users, create a unique hash
  $user_hash = md5(uniqid(rand(),true));      
  $session_name = 'VVebUQ_user_'.$username.'_id_'.$user_hash;
  $session_address = $session_address.$user_hash.'/';
  // --- Create new workdir for user
  $new_workdir = '/VVebUQ_runs/'.$session_name;
  shell_exec('mkdir -p '.$new_workdir);
  // --- Create new index.html webpage and rest_api.php for user
  $new_workdir = '../'.$user_hash;
  shell_exec('mkdir -p '.$new_workdir);
  shell_exec('cp ../default_page/index.html '.$new_workdir.'/');
  shell_exec('cp ../default_page/rest_api.php '.$new_workdir.'/');
  shell_exec('cp config.in '.$new_workdir.'/');
  // --- Return link of new session to user
  if (isset($_GET['FROM_WEB_FRONT']))
  {
    echo 'You now have a new session running, please follow this link:<br/><a href="'.$session_address.'">'.$session_address.'</a>';
  }else
  {
    echo "You now have a new session running, please follow this link:\n";
    echo $session_address."\n";
  }
}

exit;

?>

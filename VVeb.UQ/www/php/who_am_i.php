<?php

// --- The address holds the user id
$session_address = $_SERVER['HTTP_REFERER'];
if (trim($session_address) == '')
{
  $session_address = $_SERVER['HTTP_HOST'];
}
// --- Get the user id
$session_address = explode(':',$session_address);
$user_hash = trim($session_address[count($session_address)-1]);
if (substr($user_hash, -1) != '/')
{
  $user_hash = explode('/',$user_hash);
  $user_hash = $user_hash[count($user_hash)-1];
}else
{
  $user_hash = explode('/',$user_hash);
  $user_hash = $user_hash[count($user_hash)-2];
}

// --- Find username
$workdirs = shell_exec('ls /VVebUQ_runs/ | grep VVebUQ_user_ | grep _id_');
$workdirs = preg_split('/\s+/', $workdirs);
$username = '';
$session_name = '';
for ($i=0; $i<count($workdirs); $i++)
{
  if (trim($workdirs[$i]) != '')
  {
    if(strpos($workdirs[$i], $user_hash) !== false)
    {
      $session_name = trim($workdirs[$i]);
      $username = explode('VVebUQ_user_',trim($workdirs[$i]));
      $username = $username[1];
      $username = explode('_id_'.$user_hash,trim($workdirs[$i]));
      $username = $username[0];
    }
  }
}

echo $session_name;

?>

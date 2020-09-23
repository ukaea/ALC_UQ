<?php

$vvebuq_id = trim(shell_exec('docker ps -aqf name=vvebuq_app --filter status=running'));
$vvebuq_mounts = shell_exec('docker inspect -f "{{.Mounts}}" '.$vvebuq_id);
$vvebuq_mounts = explode('} {',$vvebuq_mounts);
$user_interface = '';
$working_directory = '';
foreach ($vvebuq_mounts as $mount_tmp)
{
  if (    (strpos($mount_tmp, 'bind') !== false)
       && (strpos($mount_tmp, 'vvuq_user_interface') !== false) )
  {
    $user_interface = trim(explode('bind',$mount_tmp)[1]);
    $user_interface = trim(preg_split('/\s+/',$user_interface)[0]);
    if (substr($user_interface, -1) != '/')
    {
      $user_interface = $user_interface.'/';
    }
  }elseif (    (strpos($mount_tmp, 'bind') !== false)
            && (strpos($mount_tmp, 'VVebUQ_runs') !== false) )
  {
    $working_directory = trim(explode('bind',$mount_tmp)[1]);
    $working_directory = trim(preg_split('/\s+/',$working_directory)[0]);
    if (substr($working_directory, -1) != '/')
    {
      $working_directory = $working_directory.'/';
    }
  }
}

echo $working_directory.','.$user_interface;

?>

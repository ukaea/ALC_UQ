<?php


// --- Inputs
$session_name = $_REQUEST["VVebUQ_session_name"];
$run_name = $_REQUEST["run_name"];
$selected_cloud = $_REQUEST["selected_cloud"];

// --- Straight-forward if running locally
if ($selected_cloud != "use_prominence") { exit(); }

// --- Check if we are using Prominence
$dir_name = $run_name;
$dir_name = "workdir_".$dir_name;
$dir_name = '/VVebUQ_runs/'.$session_name.'/'.$dir_name;
$prominence_id_file = $dir_name.'/prominence_workflow_id.txt';
$use_prominence = file_exists($prominence_id_file);

// --- If we're not using Prominence, do nothing
if (! $use_prominence) {exit();}

// --- Before checking everything, check which vvuq software we're using
$arguments = shell_exec('cat '.$dir_name.'/arguments_for_vvuq_script.txt');
$arguments = preg_split('/\s+/',trim($arguments));
$selected_vvuq = trim($arguments[count($arguments)-2]);

// --- The VVUQ container name depends on the user
$vvuq_container = $selected_vvuq.'_container_'.$session_name;

$prominence_token = shell_exec('docker exec '.$vvuq_container.' bash -c \'cat $HOME/.prominence/token\'');
$prominence_token = explode('{"access_token": "',$prominence_token);
if (count($prominence_token) == 2)
{
  $prominence_token = explode('"',$prominence_token[1])[0];
  $command = 'docker exec -t '.$vvuq_container.' bash -c \'curl -i -H "Authorization: Bearer '.$prominence_token.'" $PROMINENCE_OIDC_URL/userinfo\'';
  $token_valid = shell_exec($command);
  $token_valid = explode('200 OK',$token_valid);
  if (count($token_valid) == 2)
  {
    // --- If Prominence token is valid, do nothing
    exit();
  }else
  {
    echo "expired";
    exit();
  }
}else
{
  echo "expired";
  exit();
}

exit();


?>

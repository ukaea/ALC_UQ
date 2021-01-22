<?php

// --- Get input
$session_name = $_REQUEST["VVebUQ_session_name"];
$selected_vvuq = $_REQUEST["selected_vvuq"];

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

<?php

if (isset($_GET["docker_image"]))
{
  $image_name = $_GET["docker_image"];
}else
{
  if ($argc < 2) {exit();}
  $image_name = $argv[1];
}
$name_split = explode(':',$image_name)[0];
$username  = explode('/',$name_split)[0];
$imagename = explode('/',$name_split)[1];
$command  = 'docker search '.$imagename.' | grep -i '.$username;
$docker   = shell_exec($command);

$docker_image = strtolower(trim(preg_split('/\s+/',$docker)[0]));
$input_image = trim(strtolower($username).'/'.strtolower($imagename));
if ($docker_image == $input_image)
{
  echo $docker_image;
}

?>

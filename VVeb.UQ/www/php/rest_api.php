<?php

// --- input-file-upload
if (isset($_FILES["fileToUpload"]["name"][0]))
{
  include('upload.php');
  exit();
}

// --- data-file-upload
if (isset($_FILES["dataFileToUpload"]["name"][0]))
{
  include('upload_data_file.php');
  exit();
}

// --- All other cases should have an action
if (! isset($_POST["action"]))
{
  clean_exit("You did not specify any action");
}

// --- Request Prominence Token
if (trim($_POST["action"]) == 'request_prominence_token')
{
  if (! isset($_POST["vvuq_container"]))       {$_POST["vvuq_container"] = "dakota";}
  include('request_prominence_token.php');
  exit();
}

// --- Launch new run
if (trim($_POST["action"]) == 'launch_run')
{
  if (! isset($_POST["docker_image_run"]))     {clean_exit("Variable \"docker_image_run\" required");}
  if (! isset($_POST["n_cpu"]))                {clean_exit("Variable \"n_cpu\" required");}
  if (! isset($_POST["input_file_name"]))      {clean_exit("Variable \"input_file_name\" required");}
  if (! isset($_POST["input_file_type"]))      {clean_exit("Variable \"input_file_type\" required");}
  if (! isset($_POST["input_data_file_name"])) {$_POST["input_data_file_name"] = "none";}
  if (! isset($_POST["use_prominence"]))       {$_POST["use_prominence"] = "false";}
  include('create_runs.php');
  exit();
}

// --- List runs
if (trim($_POST["action"]) == 'list_runs')
{
  include("list_runs.php");
  exit();
}




exit();






// --- remove image from registry
function clean_exit($message)
{
  echo 'VVebUQ: '.$message."\n";
  echo "        please visit https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ\n";
  echo "        for detailed instructions.\n";
  exit();
}


?>

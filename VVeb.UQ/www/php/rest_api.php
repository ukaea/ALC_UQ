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
if ( (! isset($_POST["action"])) && (! isset($_GET["action"])) )
{
  clean_exit("You did not specify any action");
}else
{
  if (isset($_POST["action"]))
  {
    $ACTION = trim($_POST["action"]);
  }else
  {
    $ACTION = trim($_GET["action"]);
  }
}

// --- Request Prominence Token
if ($ACTION == 'request_prominence_token')
{
  if (! isset($_POST["vvuq_container"]))       {$_POST["vvuq_container"] = "dakota";}
  include('request_prominence_token.php');
  exit();
}

// --- Launch new run
if ($ACTION == 'launch_run')
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
if ($ACTION == 'list_runs')
{
  include("list_runs.php");
  exit();
}

// --- Get run status
if ($ACTION == 'get_run_status')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("get_run_status.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'list_run_files')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("list_run_files.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'download_run')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("download_run.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'download_run_files')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("download_run_files.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'delete_run')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("delete_run.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'delete_run_data')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run();
  }
  include("delete_run.php");
  include("delete_run_data.php");
  exit();
}


exit();






function get_latest_run()
{
  $all_runs = shell_exec('php list_runs.php');
  $all_runs = preg_split('/\R/',$all_runs);
  $year_max = -1;
  $month_max = -1;
  $day_max = -1;
  $hour_max = -1;
  $min_max = -1;
  $sec_max = -1;
  $last_run = 0;
  for ($i=0 ; $i<count($all_runs); $i++)
  {
    if (trim($all_runs[$i]) != '')
    {
      $run_tmp = trim($all_runs[$i]);
      $date_full = explode("_",$run_tmp)[0];
      $date = explode("---",$date_full)[0];
      $time = explode("---",$date_full)[1];
      $date = explode("-",$date);
      $time = explode("-",$time);
      $year = $date[0];
      $month = $date[1];
      $day = $date[2];
      $hour = $time[0];
      $min = $time[1];
      $sec = $time[2];
      if ($year >= $year_max)
      {
        $year_max = $year;
        $last_run = $i;
        continue;
        if ($month >= $month_max)
        {
          $month_max = $month;
          $last_run = $i;
          continue;
          if ($day >= $day_max)
          {
            $day_max = $day;
            $last_run = $i;
            continue;
            if ($hour >= $hour_max)
            {
              $hour_max = $hour;
              $last_run = $i;
              continue;
              if ($min >= $min_max)
              {
                $min_max = $min;
                $last_run = $i;
                continue;
                if ($sec >= $sec_max)
                {
                  $sec_max = $sec;
                  $last_run = $i;
                  continue;
      } } } } } }
    }
  }
  return trim($all_runs[$last_run]);
}






// --- remove image from registry
function clean_exit($message)
{
  echo 'VVebUQ: '.$message."\n";
  echo "        please visit https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ\n";
  echo "        for detailed instructions.\n";
  exit();
}


?>

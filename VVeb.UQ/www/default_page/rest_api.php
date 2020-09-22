<?php

// --------------------------
// --- Initialisation
// --------------------------

// --- First we need to know who the user is
$pwd = trim(shell_exec('pwd'));
$user_hash = explode('/',$pwd);
if (substr($pwd, -1) != '/')
{
  $user_hash = $user_hash[count($user_hash)-1];
}else
{
  $user_hash = $user_hash[count($user_hash)-2];
}

// --- Find username based on user id-hash
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

// --- In principle, this should never happen
if ($session_name == '')
{
  clean_exit("Could not determine username and session!");
}

// --- Set the session name for every action
$_POST['VVebUQ_session_name'] = $session_name;
$_GET['VVebUQ_session_name'] = $session_name;


// --------------------------
// --- List of rest-API calls
// --------------------------

// --- input-file-upload
if (isset($_FILES["fileToUpload"]["name"][0]))
{
  include('../php/upload.php');
  exit();
}

// --- data-file-upload
if (isset($_FILES["dataFileToUpload"]["name"][0]))
{
  include('../php/upload_data_file.php');
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

// --- Launch VVUQ container
if ($ACTION == 'launch_vvuq')
{
  if (! isset($_POST["selected_vvuq"]))       {clean_exit("Variable \"selected_vvuq\" required (either dakota or easyvvuq)");}
  if (strtolower($_POST["selected_vvuq"]) == 'dakota')
  {
    $_POST["docker_image"] = 'dakota_image';
    $_POST["container_name"] = 'dakota_container_'.$session_name;
  }else
  {
    $_POST["docker_image"] = 'easyvvuq_image';
    $_POST["container_name"] = 'easyvvuq_container_'.$session_name;
  }
  include('../php/launch_vvuq.php');
  exit();
}

// --- Request Prominence Token
if ($ACTION == 'request_prominence_token')
{
  if (! isset($_POST["selected_vvuq"]))       {clean_exit("Variable \"selected_vvuq\" required (either dakota or easyvvuq)");}
  include('../php/request_prominence_token.php');
  exit();
}

// --- Launch new run
if ($ACTION == 'launch_run')
{
  // --- Check all inputs are here
  if (! isset($_POST["docker_image_run"]))     {clean_exit("Variable \"docker_image_run\" required");}
  if (! isset($_POST["selected_vvuq"]))        {clean_exit("Variable \"selected_vvuq\" required");}
  if (! isset($_POST["n_cpu"]))                {clean_exit("Variable \"n_cpu\" required");}
  if (! isset($_POST["input_file_name"]))      {clean_exit("Variable \"input_file_name\" required");}
  if (! isset($_POST["input_file_type"]))      {clean_exit("Variable \"input_file_type\" required");}
  if (! isset($_POST["input_data_file_name"])) {$_POST["input_data_file_name"] = "none";}
  if (! isset($_POST["use_prominence"]))       {$_POST["use_prominence"] = "false";}
  // --- In order to allow the job submission as an async bash command
  // --- the arguments must be passed as normal variables, not as $_POST
  $arguments = $_POST["docker_image_run"];
  $arguments = $arguments.' '.$_POST["selected_vvuq"];
  $arguments = $arguments.' '.$_POST["n_cpu"];
  $arguments = $arguments.' '.$_POST["input_file_name"];
  $arguments = $arguments.' '.$_POST["input_file_type"];
  $arguments = $arguments.' '.$_POST["input_data_file_name"];
  $arguments = $arguments.' '.$_POST["use_prominence"];
  $arguments = $arguments.' '.$session_name;
  shell_exec('php ../php/create_runs.php '.$arguments.' > /dev/null &');
  echo "Your job is being prepared for submission...\n";
  exit();
}

// --- List runs
if ($ACTION == 'list_runs')
{
  include("../php/list_runs.php");
  exit();
}

// --- Get run status
if ($ACTION == 'get_run_status')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/get_run_status.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'list_run_files')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/list_run_files.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'download_run')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/download_run.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'download_run_files')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/download_run_files.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'delete_run')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/delete_run.php");
  exit();
}

// --- List files inside run tasks
if ($ACTION == 'delete_run_data')
{
  // --- If the user did not specify a run-name, we use the most recent one
  if (! isset($_GET["run_name"]))
  {
    $_GET["run_name"] = get_latest_run($session_name);
  }
  include("../php/delete_run.php");
  include("../php/delete_run_data.php");
  exit();
}


exit();






function get_latest_run($session_name)
{
  $all_runs = shell_exec('php ../php/list_runs.php '.$session_name);
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
      $year = intval($date[0]);
      $month = intval($date[1]);
      $day = intval($date[2]);
      $hour = intval($time[0]);
      $min = intval($time[1]);
      $sec = intval($time[2]);
      if ($year >= $year_max)
      {
        if ($year > $year_max)
        {
          $year_max = $year;
          $month_max = $month;
          $day_max = $day;
          $hour_max = $hour;
          $min_max = $min;
          $sec_max = $sec;
          $last_run = $i;
          continue;
        }
        if ($month >= $month_max)
        {
          if ($month > $month_max)
          {	
            $year_max = $year;
            $month_max = $month;
            $day_max = $day;
            $hour_max = $hour;
            $min_max = $min;
            $sec_max = $sec;
            $last_run = $i;
            continue;
          }
          if ($day >= $day_max)
          {
            if ($day > $day_max)
            {
              $year_max = $year;
              $month_max = $month;
              $day_max = $day;
              $hour_max = $hour;
              $min_max = $min;
              $sec_max = $sec;
              $last_run = $i;
              continue;
            }
            if ($hour >= $hour_max)
            {
              if ($hour > $hour_max)
              {
                $year_max = $year;
                $month_max = $month;
                $day_max = $day;
                $hour_max = $hour;
                $min_max = $min;
                $sec_max = $sec;
                $last_run = $i;
                continue;
              }
              if ($min >= $min_max)
              {
                if ($min > $min_max)
                {
                  $year_max = $year;
                  $month_max = $month;
                  $day_max = $day;
                  $hour_max = $hour;
                  $min_max = $min;
                  $sec_max = $sec;
                  $last_run = $i;
                  continue;
                }
                if ($sec > $sec_max)
                {
                  $year_max = $year;
                  $month_max = $month;
                  $day_max = $day;
                  $hour_max = $hour;
                  $min_max = $min;
                  $sec_max = $sec;
                  $last_run = $i;
      } } } } } }
    }
  }
  if (trim($all_runs[$last_run]) == '')
  {
    echo "There are no jobs currently submitted or running\n";
    exit();
  }
  return trim($all_runs[$last_run]);
}






// --- remove image from registry
function clean_exit($message)
{
  echo 'VVebUQ: '.$message."\n";
  echo "        Maybe you used GET method instead of POST (or vice versa)?\n";
  echo "        please visit https://github.com/ukaea/ALC_UQ/wiki/VVeb.UQ\n";
  echo "        for detailed instructions.\n";
  exit();
}


?>

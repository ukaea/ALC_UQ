<?php
$run_name = '/VVebUQ_runs/workdir_'.$_POST["run_name"];
$all_sub_runs  = shell_exec('ls '.$run_name.' | grep workdir_VVebUQ');
$all_sub_runs  = preg_split("/\r\n|\n|\r/",$all_sub_runs);
$all_sub_dirs  = shell_exec('ls -d '.$run_name.'/'.$all_sub_runs[0].'/*/');
$all_sub_dirs  = preg_split("/\r\n|\n|\r/",$all_sub_dirs);
$all_sub_files = shell_exec('ls -p '.$run_name.'/'.$all_sub_runs[0].'/ | grep -v /');
$all_sub_files = preg_split("/\r\n|\n|\r/",$all_sub_files);
$n_runs = count($all_sub_runs) - 1;
echo("This run contains ".$n_runs." containers\n");
if ( (count($all_sub_dirs) > 1) || (count($all_sub_files) > 1))
{
  echo("At first sight, each container contains\n");
  if (count($all_sub_files) > 1)
  {
    echo("the following files:\n");
    foreach ($all_sub_files as $file)
    {                                 
      if ($file != '') {echo(" - ".$file."\n");}
    }
  }
  if (count($all_sub_dirs) > 1)
  {
    echo("and the following sub-folders:\n");
    foreach ($all_sub_dirs as $subdir)
    {
      if ($subdir != '') {echo(" - ".$subdir."\n");}
    }
  }
}
?>

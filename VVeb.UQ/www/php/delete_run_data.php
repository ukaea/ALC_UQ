<?php
// --- Get session name
$session_name = $_GET['VVebUQ_session_name'];

// --- Delete directory of run
$dir_name = 'workdir_'.$_GET["run_name"];
shell_exec('rm -rf /VVebUQ_runs/'.$session_name.'/'.$dir_name);
?>

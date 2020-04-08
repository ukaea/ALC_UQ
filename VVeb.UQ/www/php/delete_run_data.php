<?php
$run_name = '/VVebUQ_runs/workdir_'.$_POST["run_name"];
shell_exec('rm -rf '.$run_name);
?>

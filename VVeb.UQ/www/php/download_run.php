<?php
$run_name = $_POST["run_name"];
$run_dir  = 'workdir_'.$_POST["run_name"];
shell_exec('cd /VVebUQ_runs/ ; zip -r '.$run_name.'.zip ./'.$run_dir.' ; cd -');
shell_exec('mkdir -p ../downloads ; mv /VVebUQ_runs/'.$run_name.'.zip ../downloads/');
readfile('../downloads/'.$run_name.'.zip');
?>

<?php

$run_name = $_GET["run_name"];
$command = 'docker ps -aqf name='.$run_name.' --format="table {{.Image}}\\t{{.ID}}\\t{{.RunningFor}}\\t{{.Status}}" ';
$output = shell_exec($command);
echo $output;
exit();

?>

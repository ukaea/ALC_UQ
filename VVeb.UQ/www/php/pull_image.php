<?php


// --- Get Form Variables
$image_name = $_POST["docker_image"];

// --- Run Container
$command = 'docker pull '.$image_name;
shell_exec('printf \''.$command.'\n\' &> /VVebUQ_runs/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');

// --- Go Home! (Said Nigel Fromage)
header("Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

<?php


// --- Get Form Variables
$image_name = $_POST["docker_image"];
$container_name = $_POST["container_name"];
$run_dir = shell_exec('cat config.in');
$run_dir = str_replace("\n", '', $run_dir);

// --- Run Container
$command = 'docker container run --privileged --name '.$container_name.' -v /var/run/docker.sock:/var/run/docker.sock -v '.$run_dir.':/VVebUQ_runs/ -id '.$image_name;
shell_exec('printf \''.$command.'\n\' > /VVebUQ_runs/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');

// --- Copy wrappers to run-dir
$command = 'docker cp '.$container_name.':/dakota_wrappers/ /VVebUQ_runs/';
shell_exec('printf \''.$command.'\n\' > /VVebUQ_runs/terminal_command.txt');
shell_exec($command.' &> /VVebUQ_runs/terminal_output.txt');

// --- Go Home! (Said Nigel Fromage)
header("Location: {$_SERVER['HTTP_REFERER']}");
exit;

?>

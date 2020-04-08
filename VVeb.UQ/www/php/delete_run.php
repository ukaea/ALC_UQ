<?php
$run_name = 'VVebUQ_CONTAINER_'.$_POST["run_name"];
shell_exec('for i in `docker ps -aqf name='.$run_name.' --format="{{.ID}}"` ; do docker rm -f $i ; done');
?>

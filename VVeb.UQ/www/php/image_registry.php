<?php

// --- Get arguments
$action = $_REQUEST["action"];
$image  = $_REQUEST["image"];

if ($action == "check_image"   ) {echo check_image   ($image);}
if ($action == "add_image"     ) {echo add_image     ($image);}
if ($action == "remove_image"  ) {echo remove_image  ($image);}
if ($action == "sanity_check"  ) {echo sanity_check  (      );}
if ($action == "get_all_images") {echo get_all_images(      );}



exit;


// --- Get all images
function get_all_images()
{
  // --- Make a long string containing all images, separated by a flag ___%%%___, and the id is separated from name by %%%___%%%
  $all_images = "";
  $file_content = file_get_contents('./image_registry.csv');
  $lines = explode("\n",$file_content);
  for ($i=1; $i<count($lines); $i++)
  {
    if ($lines[$i] == "") {continue;}
    $details  = explode(",",$lines[$i]);
    $name_tmp = $details[0];
    $id_tmp   = $details[1];
    $all_images = $all_images.$name_tmp."%%%___%%%".$id_tmp."___%%%___";
  }
  return $all_images;
}



// --- add image to registry
function add_image($image)
{
  // --- get name and id
  $details  = explode(",",$image);
  $name     = $details[0];
  $id       = $details[1];
  // --- First check image isn't already there...
  $already_there = "false";
  $file_content = file_get_contents('./image_registry.csv');
  $lines = explode("\n",$file_content);
  for ($i=1; $i<count($lines); $i++)
  { 
    if ($lines[$i] == "") {continue;}
    $details  = explode(",",$lines[$i]);
    $name_tmp = $details[0];
    $id_tmp   = $details[1];
    if ( ($name_tmp == $name) && ($id_tmp == $id) )
    {
      $already_there = "true";
    }
  }
  if ($already_there == "false")
  {
    shell_exec('printf \''.$image.'\n\' >> ./image_registry.csv');
  }
  return "done";
}




// --- check image exists both in the registry and in the docker built images
function check_image($image)
{
  $file_content = file_get_contents('./image_registry.csv');
  $lines = explode("\n",$file_content);
  for ($i=1; $i<count($lines); $i++)
  {
    if ($lines[$i] == "") {continue;}
    $details  = explode(",",$lines[$i]);
    $name_tmp = $details[0];
    $id_tmp   = $details[1];
    if ($name_tmp == $image)
    {
      $command  = 'docker images --format="{{.ID}} {{.Repository}}:{{.Tag}}" | grep '.$name_tmp.' | grep '.$id_tmp;
      $docker   = shell_exec($command);
      if ($docker != "")
      {
        return "found";
      }else
      {
        // --- if image is in the registry but not built, we need to remove it from registry
        remove_image($image);
        return "none";
      }
    }
  }
  return "none";
}


// --- check all images exist both in the registry and in the docker built images
function sanity_check()
{
  $file_content = file_get_contents('./image_registry.csv');
  $lines = explode("\n",$file_content);
  for ($i=1; $i<count($lines); $i++)
  {
    if ($lines[$i] == "") {continue;}
    $details  = explode(",",$lines[$i]);
    $name_tmp = $details[0];
    $id_tmp   = $details[1];
    $command  = 'docker images --format="{{.ID}} {{.Repository}}:{{.Tag}}" | grep '.$name_tmp.' | grep '.$id_tmp;
    $docker   = shell_exec($command);
    if ($docker == "")
    {
      remove_image($name_tmp);
    }
  }
  return "done";
}




// --- remove image from registry
function remove_image($image)
{
  $new_file = "";
  $file_content = file_get_contents('./image_registry.csv');
  $lines = explode("\n",$file_content);
  for ($i=0; $i<count($lines); $i++)
  {
    if ($lines[$i] == "") {continue;}
    $details  = explode(",",$lines[$i]);
    $name_tmp = $details[0];
    $id_tmp   = $details[1];
    if ($name_tmp != $image)
    {
      $new_file = $new_file.$lines[$i].'\n';
    }
  }
  shell_exec('printf \''.$new_file.'\' > ./image_registry.csv');
  return "done";
}



?>

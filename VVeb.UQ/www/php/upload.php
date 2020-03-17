<?php


// --- Prepare printout
echo "<div style=\"background:white;color:black;\"><br />";

// --- Get number of files
$n_files = count($_FILES["fileToUpload"]["name"]);
if($n_files == 0) 
{
  echo "Sorry, there was an error uploading your file.<br />";
echo " file: ".$_FILES["fileToUpload"]["name"]."<br/>";
  echo "It seems you did not select any files to upload.<br />";
  echo "Use exit button to get back to main page...<br />";
  echo "</div>";
  exit();
}



  
// --- Loop over all files
for($i=0 ; $i<$n_files ; $i++)
{
  
  // --- Rename the file to avoid spaces (this could be extended at some point to avoid strange characters...)
  $file_name = basename($_FILES["fileToUpload"]["name"][$i]);
  $name_split = preg_split('/\s+/', $file_name);
  $new_name = "";
  $count = 0;
  foreach ($name_split as &$name_part)
  {
    $count = $count + 1;
    if ($count > 1)
    {
      $new_name = $new_name."_".$name_part;
    }else
    {
      $new_name = $name_part;
    }
  }		  
  $new_name = '/VVebUQ_runs/'.$new_name;
  $default_name = '/VVebUQ_runs/vvebuq_input.nc';
 
  // --- Define temporary target file here (it will be moved after upload)
  $target_file = basename($_FILES["fileToUpload"]["name"][$i]);
  
  // --- Check if file already exists, if yes, make a copy
  if (file_exists($new_name))
  {
    $date_full = getdate();
    $date_deleted = $date_full[mday]."-".$date_full[month]."-".$date_full[year];
    $date_deleted = $date_deleted."---".$date_full[hours]."-".$date_full[minutes]."-".$date_full[seconds];
    $trash_file = $new_name.'.saved_'.$date_deleted;
    rename($new_name, $trash_file);
  }
  
  
  // --- Try to upload the file
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"][$i], $target_file))
  {
      // --- If our file was uploaded to the temporary place, rename it.
      rename($target_file, $new_name);
      shell_exec('cp '.$new_name.' '.$default_name);
  } else {
      echo "Sorry, there was an error uploading your file.<br />";
      echo "You will be redirected to the main page in a few seconds.<br />";
      echo "Otherwise click the exit button...<br />";
      echo "</div>";
      exit();
  }
}

// --- Now exit with a convenient message...
echo "Your files have been uploaded.<br />";
echo "</div>";

// --- Go Home! (Said Nigel Fromage)
#header("Location: {$_SERVER['HTTP_REFERER']}");
exit;


?>


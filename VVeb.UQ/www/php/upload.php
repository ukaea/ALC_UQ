<?php

// --- Get session name
$session_name = $_POST['VVebUQ_session_name'];

// --- Get number of files
$n_files = count($_FILES["fileToUpload"]["name"]);
if($n_files == 0) 
{
  echo '{"error":"It seems you did not select any files to upload."}';
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
  $new_name = '/VVebUQ_runs/'.$session_name.'/'.$new_name;
 
  // --- Define temporary target file here (it will be moved after upload)
  $target_file = basename($_FILES["fileToUpload"]["name"][$i]);
  
  // --- Check if file already exists, if yes, make a copy
  if (file_exists($new_name))
  {
    $date_full = getdate();
    $date_deleted = $date_full[year]."-".$date_full[mon]."-".$date_full[mday];
    $date_deleted = $date_deleted."---".$date_full[hours]."-".$date_full[minutes]."-".$date_full[seconds];
    $trash_file = $new_name.'.saved_'.$date_deleted;
    rename($new_name, $trash_file);
  }
  
  
  // --- Try to upload the file
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"][$i], $target_file))
  {
      // --- If our file was uploaded to the temporary place, rename it.
      rename($target_file, $new_name);
  } else {
      echo "Sorry, there was an error uploading your file.<br />";
      echo "You will be redirected to the main page in a few seconds.<br />";
      echo "Otherwise click the exit button...<br />";
      echo "</div>";
      exit();
  }
}

// --- Now exit with a convenient message...
echo '{"success":"Your files have been uploaded."}';

// --- Go Home! (Said Nigel Fromage)
#header("Location: {$_SERVER['HTTP_REFERER']}");
exit;


?>


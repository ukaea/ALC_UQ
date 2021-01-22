#!/bin/bash

all_urls=`cat VVebUQ_URL_individual_jobs.txt`
url_array=(${all_urls//$'\n'/ })

if [ -d "download_dir" ] ; then
  echo "The directory \"download_dir\" already exists"
  echo "This script will download all URLs not yet present in \"download_dir\"."
  echo "If you want to restart a new download, either delete"
  echo "or rename the directory \"download_dir\""
  echo -n "Do you want to continue downloading? (y/n) "
  read answer
  if [ $answer != "y" ] ; then
    exit 0;
  fi
else
  mkdir download_dir
fi

for i in "${!url_array[@]}"; do
  if [ ${url_array[i]} != "" ] ; then
    ip1=$((i + 1)) 
    file_tmp="download_dir/workdir_VVebUQ."$ip1".tgz"
    if [ ! -f $file_tmp ] ; then
      curl "${url_array[i]}" > $file_tmp
    else
      echo "file \""$file_tmp"\" already exists, skipping..."
    fi
  fi
done

echo "finished"
echo "to extract all tarballs, you can execute the following command:"
echo "cd download_dir/ ; for file in ./* ; do tar -xvzf \$file ; done ; cd ../"



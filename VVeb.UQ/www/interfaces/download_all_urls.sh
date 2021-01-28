#!/bin/bash

# --- Read input file
all_urls=`cat VVebUQ_URL_individual_jobs.txt`
url_array=(${all_urls//$'\n'/ })

IFS=$'\n'
url_array=($all_urls)

# --- Create download directory
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

# --- Check size of download
total_size=0
total_files=0
for i in "${!url_array[@]}"; do
  if [ ${url_array[i]} != "" ] ; then
    IFS=' '
    file_size_tmp=(${url_array[i]})
    file_size_tmp=${file_size_tmp[0]}
    IFS=$'\n'
    total_files=$((total_files + 1))
    total_size=$((total_size + file_size_tmp))
  fi
done
averaged_size="$((total_size/total_files))"

echo ""
echo "There are $total_files files, with an averaged size of $averaged_size"
echo "The total size of the download is $total_size"
echo -n "Do you want to continue downloading? (y/n) "
read answer
if [ $answer != "y" ] ; then
  exit 0;
fi

# --- Proceed with download
for i in "${!url_array[@]}"; do
  if [ ${url_array[i]} != "" ] ; then
    ip1=$((i + 1)) 
    file_tmp="download_dir/workdir_VVebUQ."$ip1".tgz"
    if [ ! -f $file_tmp ] ; then
      IFS=' '
      url_tmp=(${url_array[i]})
      url_tmp=${url_tmp[1]}
      IFS=$'\n'
      curl "$url_tmp" > $file_tmp
    else
      echo "file \""$file_tmp"\" already exists, skipping..."
    fi
  fi
done

echo "finished"
echo "to extract all tarballs, you can execute the following command:"
echo "cd download_dir/ ; for file in ./* ; do tar -xvzf \$file ; done ; cd ../"



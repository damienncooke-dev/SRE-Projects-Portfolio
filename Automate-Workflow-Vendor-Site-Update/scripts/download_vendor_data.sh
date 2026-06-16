#!/bin/bash

# Copy vendor file called: 'supplier-data.tar.gz'.
# Note: 'wget' does not work on MacOS by default. Use 'curl -O' to get file from URL and save.
curl -O https://storage.googleapis.com/gwg-content/gic223/supplier-data.tar.gz


TAR_FILE="$PWD/supplier-data.tar.gz"
DATA_DIR="$PWD/supplier-data"

if [[ -f "$TAR_FILE" && ! -d "$DATA_DIR" ]] ; then
  echo "Extracting .tar File"
  tar -xzf $TAR_FILE
elif [[ -f "$TAR_FILE" && -d "$DATA_DIR" ]]; then
  echo "Removing Old Directory:" $DATA_DIR
  rm -Rf  $DATA_DIR
  sleep 2
  echo "Extracting new .tar file"
  tar -xzf $TAR_FILE
else
  echo "Check for" $TAR_FILE
fi




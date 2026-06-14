#!/bin/bash

# Copy vendor file called: 'supplier-data.tar.gz'.
# Note: 'wget' does not work on MacOS by default. Use 'curl -O' to get file from URL and save.
curl -O https://storage.googleapis.com/gwg-content/gic223/supplier-data.tar.gz

# Use 'tar -xf <file>' to extract
# Need update to script to ask for confirmation to extract file



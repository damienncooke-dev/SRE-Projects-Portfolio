#!/usr/bin/env python3

"""
The main script to iterate over the supplier text data, read each file and turn it into JSON dictionary data, and upload to the website with
image name to map to the correct image.

"""

import os
import requests
from pathlib import Path

main_dir = Path(__file__).parent.parent
description_dir = main_dir / "supplier-data" / "descriptions"
images_dir = main_dir / "supplier-data" / "images"

desc_text = [file.name for file in description_dir.iterdir()]

desc_text_list = [] # Create an empty list to append description read from each text file

for file in desc_text:
    fname, ext = os.path.splitext(file) # Get filename, extension
    image_file = f"{fname}.jpeg"  # Get the associated image file of the text file description
    description_file = description_dir / file
    with open(description_file, 'r') as f:
        desc_text_list.append({"name":f.readline().rstrip("\n"),
                               "weight":int(f.readline().rstrip("\n").split(" ")[0]),
                               "description":f.read().rstrip("\n"),
                               "image_name":image_file})

# Iterate over the list of dictionaries and upload each one to the website
for record in desc_text_list:
    resp = requests.post("http://34.69.110.154/fruits/", json=record)  # POST each record as JSON
    print(resp.status_code)




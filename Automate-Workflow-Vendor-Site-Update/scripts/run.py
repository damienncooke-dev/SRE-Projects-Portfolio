#!/usr/bin/env python3

"""
The main script to iterate over the supplier text data, read each file and turn it into JSON dictionary data, and upload to the website with
image name to map to the correct image.

"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Set directory path objects
main_dir = Path(__file__).parent.parent
description_dir = main_dir / "supplier-data" / "descriptions"
images_dir = main_dir / "supplier-data" / "images"
dotenv_path = main_dir / ".dotenv"

# Load environment variables from .env file
load_dotenv(dotenv_path=dotenv_path)
fruit_store_url = os.getenv("FRUIT_COMP_URL")

# Get the list of files in the directory to iterate over
desc_text = [file.name for file in description_dir.iterdir()]

desc_text_list = [] # Create an empty list to append description read from each text file

# Iterate over the list of files to create a list of description information in JSON format
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
url = f"http://{fruit_store_url}/fruits/"  # URL to upload images to
url_main = f"http://{fruit_store_url}"  # URL to upload images to

for record in desc_text_list:
    resp = requests.post(url, json=record)  # POST each record as JSON
    print(resp.status_code)

print("Uploaded product description to: {}".format(url))
print("Check the website for the updated text descriptions and product images here: {}".format(url_main))




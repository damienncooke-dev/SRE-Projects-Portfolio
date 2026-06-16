#!/usr/bin/env python3

"""
Uploads images with '.jpeg' extensions to the website

"""

import requests
import os
from pathlib import Path
from dotenv import load_dotenv


# Set directory path objects
main_dir = Path(__file__).parent.parent
image_dir = main_dir / "supplier-data" / "images"
dotenv_path = main_dir / ".dotenv"

# Load environment variables from .env file
load_dotenv(dotenv_path=dotenv_path)
fruit_store_url = os.getenv("FRUIT_COMP_URL")


# Iterate over image_dir and get list of filenames
images = [file.name for file in image_dir.iterdir()]

url = f"http://{fruit_store_url}/upload/"  # URL to upload images to

# for file in images:   # Iterate over list of image filenames
#    fname, ext = os.path.splitext(file)  # Get filename, extension
#    image_file = image_dir / file  # Get full path to image file
#    if ".jpeg" in ext:  # Only upload .jpeg files
#       with open (image_file, 'rb') as opened:  # Open image file in binary mode
#          result = requests.post(url, files={'file': opened})  # POST request to upload image

print("Uploaded images to: {}".format(url))
print("Check the website for the uploaded images.")

# Add error handling for non-connection
# Add check to prevent duplicate uploads, maybe tag the files as uploaded if POST request is successful.


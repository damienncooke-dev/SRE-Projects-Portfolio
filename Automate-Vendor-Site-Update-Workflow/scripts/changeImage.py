#!/usr/bin/env python3

"""
Works on the image files with '.tiff' extension to resize them from 3000x2000 to 600x400 pixels and save modified files in 'jpeg' format.

"""

from PIL import Image
from pathlib import Path
import os

# Set directory path objects
main_dir = Path(__file__).parent.parent
image_dir = main_dir / "supplier-data" / "images"

# Creates a list of all the image files in the directory
images = [file.name for file in image_dir.iterdir()]

# Iterate through the list of images, split filename and extension. Confirm only '.tiff' files will be processed.
for file in images:
   fname, ext = os.path.splitext(file) # Get filename, extension
   if "tiff" in ext:  # Check if extension is .tiff
      file_img = Image.open(image_dir / file) # Creates image object
      file_img.resize((600,400)).convert("RGB").save(image_dir / f"{fname}.jpeg")  # Resize, convert to RGB and save as jpeg



#!/usr/bin/env python3

"""
Works on the image files with '.tiff' extension to resize them from 3000x2000 to 600x400 pixels and save modified files in 'jpeg' format.

"""

from PIL import Image
from pathlib import Path

main_dir = Path(__file__).parent.parent


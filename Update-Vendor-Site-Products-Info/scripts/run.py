#!/usr/bin/env python3

"""
The main script to iterate over the supplier text data, turn it into JSON dictionary data, and upload to the website with
image name to map to the correct image.

"""

import os
import requests
from pathlib import Path

main_dir = Path(__file__).parent.parent


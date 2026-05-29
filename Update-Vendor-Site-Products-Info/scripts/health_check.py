#!/usr/bin/env python3

"""
Script used to check the health of the server every 60 seconds. If an incident is detected, an email is sent alerting to the error condition

"""

import os
import shutil
from pathlib import Path

import psutil


main-dir = Path(__file__).parent.parent


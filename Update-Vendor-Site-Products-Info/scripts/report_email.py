#!/usr/bin/env python3

"""
Processes the description data generated from the execution of the run.py. Calls the generate_report() to create a PDF file

"""

import os
import datetime
import reports
import email
from pathlib import Path

main_dir = Path(__file__).parent.parent


#!/usr/bin/env python3

"""
Module to define the methods to generate a PDF report

"""

import os
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

main_dir = Path(__file__).parent.parent

def generate_report():
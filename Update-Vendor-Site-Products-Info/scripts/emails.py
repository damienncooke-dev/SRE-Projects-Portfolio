#!/usr/bin/env python3

"""
Module to define the methods to create and send emails.

"""

import smtplib
import email.message
from pathlib import Path

main_dir = Path(__file__).parent.parent


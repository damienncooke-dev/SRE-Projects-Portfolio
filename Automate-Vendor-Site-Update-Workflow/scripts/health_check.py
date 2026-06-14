#!/usr/bin/env python3

"""
Script used to demonstrate various systems checks every 60 seconds enabled in cron. If an incident is detected, an email is sent alerting to the error condition

"""

import shutil
import psutil
import socket
import emails


body = "Please check your system and resolve the issue as soon as possible."

# Checks disk usage and sends email if available space < 20%
du = shutil.disk_usage("/")
du_free = du.free/du.total * 100  # Calculate free space as a percentage
if du_free < 20:
    subject = "Error - Available disk space is less than 20%"
    message = emails.generate_error_email(subject, body)
    emails.send_email(message)

# Checks CPU usage and sends email if usage >80%
cpu_util = psutil.cpu_percent(1)
if cpu_util > 80:
    subject = "Error - CPU usage is over 80%"
    message = emails.generate_error_email(subject, body)
    emails.send_email(message)

# Checks for available memory, if < 100mb sends an email
mem = psutil.virtual_memory()
target = 100 * 1024 * 1024  # (100 * 1024 KB * 1024 Bytes)
if mem.available < target:
    subject = "Error - Available memory is less than 100MB"
    message = emails.generate_error_email(subject, body)
    emails.send_email(message)

# Checks internal network adapter and TCP/IP stack by trying to resolve hostname to "127.0.0.1" and sends an email if it can't
hostname = socket.gethostbyname('localhost')
if hostname != '127.0.0.1':
    subject = "Error - localhost cannot be resolved to 127.0.0.1"
    message = emails.generate_error_email(subject, body)
    emails.send_email(message)



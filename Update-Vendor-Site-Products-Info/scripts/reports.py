#!/usr/bin/env python3

"""
Module to define the methods to generate a PDF report

"""
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Define method generate_report() to create PDF report using output 'filename', pdf 'title' and product_data

def generate_report(filename, title, paragraph):
   styles = getSampleStyleSheet()
   report = SimpleDocTemplate(filename) # pdf filename to write to
   report_title = Paragraph(title, styles["h1"])
   report_info = Paragraph(paragraph, styles["BodyText"])
   empty_line = Spacer(1,20)
   report.build([report_title, empty_line, report_info])
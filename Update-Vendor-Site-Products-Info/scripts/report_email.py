#!/usr/bin/env python3

"""
Processes the description data generated from the execution of the run.py. Calls the generate_report() to create a PDF file

"""

import datetime as df
import reports
import emails
from pathlib import Path


# Define a main() function that will do the file processing and generate PDF
def main():
    # Set the directory path objects
    main_dir = Path(__file__).parent.parent
    description_dir = main_dir / "supplier-data" / "descriptions"

    # Get the list of files in the directory to iterate over
    desc_text = [file.name for file in description_dir.iterdir()]

    desc_text_list = []  # Create an empty list to append description information read from each text file

    # Iterate over the list of files
    for file in desc_text:
        description_file = description_dir / file
        with open(description_file, 'r') as f:
            desc_text_list.append({"name": f.readline().rstrip("\n"),
                                   "weight": f.readline().rstrip("\n")})

    # Create title, filename path, and paragraph for the PDF Document
    title = f"Processed Update on {df.datetime.now().strftime('%b-%d-%Y')}"
    filename = str(main_dir / "outfiles" / "processed.pdf")
    paragraph = ""  # create empty paragraph string for accumulation of description information
    for record in sorted(desc_text_list, key=lambda x: x['name']):  # sort the data using the key 'name'
        paragraph +=f"name: {record['name']}<br/>weight: {record['weight']}<br/><br/>"

    # Create the PDF report
    reports.generate_report(filename, title, paragraph)
    return filename


if __name__ == "__main__":
    attachments = main()
    print(attachments)
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
    msg = emails.generate_email(subject, body, attachments)
    emails.send_email(msg)


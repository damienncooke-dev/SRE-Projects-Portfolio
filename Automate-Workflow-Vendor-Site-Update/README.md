# Automate Workflow - Vendor Site Update

## Project Overview
An online fruit reseller is manually updating their website with supplier information regarding the fruit products they sell by manually uploading images of the product and providing their associated text description. They want to automate this workflow as well as automatically generate an email notifying the supplier of the updated information. Due to a recent spate of system issues they also want, as a nice-to-have, a way to monitor their system and get real-time notification when certain system events occur.



## Key Features and Components

* **Automated Data Ingestion** - Created bash pipeline for data retrieval of .tar source file and extraction.
* **Batch Image Processing** - Leveraged `PIL` to programmatically resize and convert images from `.tiff` to `.jpeg` format.
* **Data Serialization** - Parsed unstructured text file and mapped the information as list of JSON records.
* **RESTful API Integration** - Securely transmitted JSON structured records and processed image files via `POST` method usig `requests` library.
* **Automated PDF Generation** - Utilized `reportlab` to generate PDF summary of the processed and uploaded supplier information.
* **SMTP Email Notification** - Automatically sends notification to supplier with PDF report summary as an attachment.
* **Observability and Monitoring** - Developed a resource monitoring script leveraging `psutil` and `shutil` to track real-time CPU utilization, memory thresholds, disk space availability and internal network adapter.
* **SMTP Error Alert Notification** - Send email alert with error condition and asap response notification.



## System Architecture and Workflow

This project is built with a modular design to ensure clean separation of functionality and reusability:

### Data Flow
   * **<u>Input:</u>** Unstructured Text File, TIFF Image Files, `.dotenv` File for Environment Variables
   * **<u>Processing:</u>** Download and extract compressed file, Resize and convert TIFF image files, Read text files and serialize into JSON format, Generate PDF Report, Montor system metrics for threshold violation, Create email object with attachment and send, Create email object for alert notification and send.
   * **<u>Output:</u>** Resized and Converted JPEG Image Files, Generated PDF Report, JSON Payload for REST API POST

### Artifacts
   * `dowload_vendor_data.sh`:
      * Downloads `.tar` file from URL and saves to root project folder.
      * Extracts contents to [`supplier-data/images`, `supplier-data/descriptions`].
   * `changeImage.py`:
      * A script to process the images will iterate over the `tiff` image files and perform the following:
         * Resize image to 600x400.
         * Convert image from 'RGBA' to 'RGB' - (JPEG format does not support the 'Alpha' transparency layer and it has to be stripped away.  Also it makes the file size smaller.).
         * Save the image in JPEG format.
   * `supplier_image_upload.py`:
      * Script will upload the modified `jpeg` images to the company's website via `POST` request.
   * `run.py`:
      * A script to process the description information from the text files by iterating over the text files and extracting:
         * Name of the product.
         * The weight of the product.
         * The full description of the product.
      * The script will construct a JSON representation of the product description and associated image and upload to company's website.
   * `report_email.py`:
      * A script that calls functions from `reports.py` and `emails.py` to generate PDF report, construct email with attachment, construct regular notification alert and send them.
   * `reports.py`:
      * A module containing a function to generate a PDF document using `reportlab` SimpleDocTemplate.
   * `emails.py`:
      * A module containing functions to:
         * Generate email with attachment using `email` and `mimetypes` modules.
         * Generate email without attachment using `email` and `mimetypes` modules.
         * Send email using `smtplib` module.
   * `health_check.py`:
      * A script to monitor system metrics; disk utilization, cpu and memory saturation and checking if the computer's internal network adapter and if TCP/IP stack is functional.
      * Calls function from `emails.py` to send email alert notifying of system monitoring incidents and response priority.

### Directory Structure

        
        Automate-Workflow-Vendor-Site/
        ├── outfiles/
        │   └── .gitkeep (to keep folder intact in the structure)
        ├── scripts/
        │   └─changeImage.py
        │   └─download_vendor_data.sh
        │   └─emails.py
        │   └─health_check.py
        │   └─report_email.py
        │   └─reports.py
        │   └─run.py
        │   └─supplier_image_upload.py
        ├── requirements.txt
        ├── README.md



   ...after running `download_vendor_data.sh`...



        Automate-Workflow-Vendor-Site/
        ├── outfiles/
        │   └── .gitkeep (to keep folder intact in the structure)
        ├── supplier-data/
        │   └── descriptions/
        │       └── *.txt ( product description files )
        │   └── images/
        │       └── *.tiff ( product images)
        ├── scripts/
        │   └─changeImage.py
        │   └─download_vendor_data.sh
        │   └─emails.py
        │   └─health_check.py
        │   └─report_email.py
        │   └─reports.py
        │   └─run.py
        │   └─supplier_image_upload.py
        ├── requirements.txt
        ├── README.md


## Tech Stack & Tools

* **Language:** Python 3.14, Bash
* **Libraries & Frameworks:**
  * **Built-in:** `os`, `pathlib`, `smtplib`, `mimetypes`, `email`, `shutil`, `socket`, `datetime`
  * **Third Party:** `requests` (API Integration), `PIL` (Image Processing), `dotenv` (Environment Variables), `psutil` (System Metrics), `reportlab` (PDF Generation)


## Installation and Setup Instructions

### Prerequisites
* Python 3.14
* Package Manager `pip`
* Ability to create a virtual environment
* Ability to reach external URLs
* Ability to send email notifications using SMTP

### Installation
1. Clone the repository:








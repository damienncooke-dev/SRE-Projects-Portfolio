# Automate Workflow - Vendor Site Update

## Project Overview
An online fruit reseller is regularly updating their website with supplier provided information regarding the fruit products they sell online. The company manually uploads images of the product and copy/paste their associated text descriptions into a website text box. They want to automate this workflow as well as automatically generate an email confirmation to the supplier regarding the information they received. Also, due to a recent spate of system issues they would like, as a nice-to-have, a way to monitor their system and get real-time notification when certain system events occur.

<br>

## Key Features and Components

* **Automated Data Ingestion** - Created bash pipeline for data retrieval of .tar source file and extraction.
* **Batch Image Processing** - Leveraged `PIL` to programmatically resize and convert images from `.tiff` to `.jpeg` format.
* **Data Serialization** - Parsed unstructured text file and mapped the information as list of JSON records.
* **RESTful API Integration** - Securely transmitted JSON structured records and processed image files via `POST` method usig `requests` library.
* **Automated PDF Generation** - Utilized `reportlab` to generate PDF summary of the processed and uploaded supplier information.
* **SMTP Email Notification** - Automatically sends notification to supplier with PDF report summary as an attachment.
* **Observability and Monitoring** - Developed a resource monitoring script leveraging `psutil` and `shutil` to track real-time CPU utilization, memory thresholds, disk space availability and internal network adapter.
* **SMTP Error Alert Notification** - Send email alert with error condition and asap response notification.

<br>

## System Architecture and Workflow

This project is built with a modular design to ensure clean separation of functionality and reusability:

### Data Flow
   * **Input:** 
       > Unstructured Text File, TIFF Image Files, `.dotenv` File for Environment Variables
   * **Processing:** 
       > Download and extract compressed file, Resize and convert TIFF image files, Read text files and serialize into JSON format, Generate PDF Report, Montor system metrics for threshold violation, Create email object with attachment and send, Create email object for alert notification and send.
   * **Output:** 
       > Resized and Converted JPEG Image Files, Generated PDF Report, JSON Payload for REST API POST

### Artifacts
   * `dowload_vendor_data.sh`:
      >* Downloads `.tar` file from URL and saves to root project folder.
      >* Extracts contents to [`supplier-data/images`, `supplier-data/descriptions`].
   * `changeImage.py`:
      >* A script to process the images will iterate over the `tiff` image files and perform the following:
        > * Resize image to 600x400.
        > * Convert image from 'RGBA' to 'RGB' - (JPEG format does not support the 'Alpha' transparency layer and it has to be stripped away.  Also it makes the file size smaller.).
        > * Save the image in JPEG format.
   * `supplier_image_upload.py`:
      > * Script will upload the modified `jpeg` images to the company's website via `POST` request.
   * `run.py`:
      > * A script to process the description information from the text files by iterating over the text files and extracting:
        > * Name of the product.
        > * The weight of the product.
        > * The full description of the product.
        > * The script will construct a JSON representation of the product description and associated image and upload to company's website.
   * `report_email.py`:
        > * A script that calls functions from `reports.py` and `emails.py` to generate PDF report, construct email with attachment, construct regular notification alert and send them.
   * `reports.py`:
        > * A module containing a function to generate a PDF document using `reportlab` SimpleDocTemplate.
   * `emails.py`:
      > * A module containing functions to:
        >  * Generate email with attachment using `email` and `mimetypes` modules.
        >  * Generate email without attachment using `email` and `mimetypes` modules.
        >  * Send email using `smtplib` module.
   * `health_check.py`:
      > * A script to monitor system metrics; disk utilization, cpu and memory saturation and checking if the computer's internal network adapter and if TCP/IP stack is functional.
      > * Calls function from `emails.py` to send email alert notifying of system monitoring incidents and response priority.

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

<br>

## Tech Stack & Tools

* **Language:** Python 3.14, Bash
* **Libraries & Frameworks:**
  * **Built-in:** `os`, `pathlib`, `smtplib`, `mimetypes`, `email`, `shutil`, `socket`, `datetime`
  * **Third Party:** `requests` (API Integration), `PIL` (Image Processing), `dotenv` (Environment Variables), `psutil` (System Metrics), `reportlab` (PDF Generation)

<br>

## Installation and Setup Instructions

### Prerequisites
* Python 3.14
  ```python
     python --version
  ```
* Package Manager `pip`
* Ability to create a virtual environment
* Ability to reach external URLs
* Ability to send email notifications using SMTP
* Ability to clone a repository from GitHub

### Installation
1. Clone the repository: `git clone https://github.com/damienncooke-dev/Automation-Portfolio.git `
2. Navigate to the project directory:
   ```python
      cd Automate-Workflow-Vendor-Site
   
   ```
3. Create a virtual environment in which to install dependencies and run scripts:
   ```python
      python3 -m venv .venv         # creates the virtual environment
      source .venv/bin/activate     # activates the virtual environment
      pip3 install --upgrade pip    # update pip to latest version
      pip3 --version                # check pip version
      pip3 install setuptools       # update to latest setuptools
      pip3 show setuptools          # check setuptools version

   ```
4. Install the dependencies using the `requirements.txt` file:
   ```python
      pip3 install -f requirements.txt
   ```
5. Check that the following were installed or updated successfully:
   ```python
      pip list                      # commad to list installed packages
   ```
   ```
      Listed Packages:
      - certifi
      - charset-normalizer
      - idna
      - pillow
      - pip
      - psutil
      - python-dotenv
      - reportlab
      - requests
      - setuptools
      - urllib3
    ```
6. Create `.dotenv` file in the project root directory and add the following based on your email provider settings:
   ```python
      vi .dotenv
   ```
   ```
   In the .dotenv file enter:
   
   # .env
      EMAIL_SENDER=
      EMAIL_RECIPIENT=
      EMAIL_CLIENT_PASSWORD=
      EMAIL_SERVER=
      EMAIL_PORT=587
   ```
   ```
   For reference:
      EMAIL_SENDER= # email address of the sender #
      EMAIL_RECIPIENT= # email address of the recipient #
      EMAIL_CLIENT_PASSWORD= # password of the sender's email account #
      EMAIL_SERVER= # email server address: e.g. smtp.gmail.com #
      EMAIL_PORT= # port 587 is the default port for TLS #
   ```
7. Setup is complete!

<br>

## Runtime and Output Screenshots


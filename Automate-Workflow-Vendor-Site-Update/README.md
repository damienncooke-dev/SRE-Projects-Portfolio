# Automate Workflow - Vendor Site Update

## Executive Summary
An online fruit reseller is manually updating their website with supplier information regarding fruit products by manually uploading images of the product, providing their weight and associated text description. They want to automate this as well as automatically generate an email notifying the supplier of the updated information. Due to a recent spate of system issues they also want, as a nice-to-have, a way to monitor their system and get real-time notification when certain system events occur.  


## System Architecture and Workflow
1. **Data Input**
   - A tar file is downloaded from a website and saved to local directory/root folder.
   - File contents are extracted to directory in root folder [`supplier-data:images`, `supplier-data:descriptions`].
2. **Data Processing**
   - A script to process the images will iterate over the `tiff` image files and perform the following:
     - Resize image to 600x400.
     - Convert image from 'RGBA' to 'RGB' - (JPEG format does not support the 'Alpha' transparency layer and it has to be stripped away.  Also it makes the file size smaller. ).
     - Save the image in JPEG format.
   - An upload images script will upload the modified jpeg images to the company's website.
   - A script to process the description text files will iterate over the text files, extracting the:
	 - Name of the product.
	 - The weight of the product.
	 - The full description.
   - The script will construct a JSON representation of the product description and associated image and upload to company's website.
   - Nice-to-have:  A script to monitor system metrics; disk utilization, cpu and memory saturation and checking if the computer's internal network adapter and TCP/IP stack is functional.
3. **Data Output**
   - A final script will generate a PDF report and send it to the supplier via email.
   - Email notifying of system monitoring incidents. 

## Key Features and Components


# Relister

Relister is a script that will add a listing to KSL Classifieds programatically.
Sometimes it is helpful to keep you listing on top of the pile. This script will
help.


## Installation

Install required packages:

`pip install -r requirements.txt`


## Instructions

You will need to manually get the category ID and subcategory ID from KSL. Just
go to KSL and create a new ad. Select the category and subcategory and click
next. The URL will display the IDs. Look at the form_3 and form_4 values in the 
URL parameters. These are the category and subcategory IDs repectively.

Example:
http://www.ksl.com/index.php?nid=640&form_3=345&form_4=486
345 is Electronics
486 is SmartPhones/PDA Phones

Look at example.py for an example script to add a classified ad.


## Debugging

When the script runs it will create various .html files. 

* 1.html: This is the output of posted basic ad details. It should contain 
  content for step 2, contact infomation.
* 2.html: This is the output of posting contact infomation.
* image.html: This is the output of trying to upload an image.
* 3.html: This is the output after accepting the terms.
* 4.html: This is the output after publishing the post.
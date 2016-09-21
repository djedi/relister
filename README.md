# Relister

Relister is a script that will add a listing to KSL Classifieds programatically.
Sometimes it is helpful to keep you listing on top of the pile. This script will
help.


## Installation

Install required packages:

```shell
pip install -r requirements.txt
```


## Instructions

You will need to manually get the category and subcategory from KSL. These are
now just string values. So browse to the category and subcategory you would like
to post in and get the category and subcategory names.

Look at example.py for an example script to add a classified ad.


## Debugging

When the script runs it will create various .html files. Create the relister
object with debug set to true

```shell
from relister import Relister

relister = Relister(debug=True)
```

* 0.html: This is the listing page result to set up session info.
* 1.html: This is the result after submitting the classified post data.
* 2.html: This is the response after activating the ad.
* img.json: This is the output of the last attempt to upload a photo.

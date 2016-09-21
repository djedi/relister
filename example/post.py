from collections import OrderedDict
import os
import sys

sys.path.append('..')

from relister import Relister, AD_TYPES, SELLER_TYPES

CATEGORY = 'Furniture'
SUBCATEGORY = 'Dining Tables'
PRICE = 80


# Create Relister instance
relister = Relister(debug=True)

# Log in to KSL with username & password
relister.login('youremail@example.com', 'KSLPassword')

# Read description from file. File should have window style line endings (\r\n)
# in order to display correctly online.
images_path = './'
desc = open(os.path.join(images_path, 'desc.txt')).read()
title = open(os.path.join(images_path, 'title.txt')).read()

# This will look for all files ending in '.jpg' and create an OrderedDict to
# pass into the post_item script. This will add all the images in this folder to
# the post. It will use the image names as descriptions for each image.
img_dict = {}
for filename in os.listdir(images_path):
    if filename.lower().endswith('.jpg'):
        img_dict[filename[0:-4]] = os.path.join(images_path, filename)
img_dict = OrderedDict(sorted(img_dict.items(), key=lambda t: t[0]))

# This will actually create the classified ad.
relister.post_item(
    category=CATEGORY,
    subcategory=SUBCATEGORY,
    price=PRICE,
    title=title,
    description=desc,
    ad_type=AD_TYPES.sale,
    seller=SELLER_TYPES.private,
    display_name='John',
    email='youremail@example.com',
    phone='801-555-1234',
    accept_text=1,
    city='Salt Lake City',
    state='UT',
    zip_code=84101,
    images=img_dict,
)

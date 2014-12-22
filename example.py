from collections import OrderedDict
import os

from relister import Relister, AD_TYPES, SELLER_TYPES


# Create Relister instance
relister = Relister()

# Log in to KSL with username & password
relister.login('your@email.com', 'yourpassword')

# Read description from file. File should have window style line endings (\r\n)
# in order to display correctly online.
desc = open('example_desc.txt').read()

# This will look for all files ending in '.jpg' and create an OrderedDict to
# pass into the post_item script. This will add all the images in this folder to
# the post. It will use the image names as descriptions for each image.
images_path = '/path/to/images'
img_dict = {}
for filename in os.listdir(images_path):
    if filename.lower().endswith('.jpg'):
        img_dict[filename[0:-4]] = os.path.join(images_path, filename)
img_dict = OrderedDict(sorted(img_dict.items(), key=lambda t: t[0]))

# This will actually create the classified ad.
relister.post_item(
    category=345,   # Electronics
    subcategory=486,  # SmartPhones/PDA Phones
    price=200,
    title='iPhone 5 - Black - 16GB - Verizon',
    description=desc,
    ad_type=AD_TYPES.sale,
    seller=SELLER_TYPES.private,
    display_name='Dustin',
    email='dustin@example.com',
    home_phone='8015551234',
    work_phone='8015554321',
    cell_phone='8015556789',
    address='1234 Lonely Street',
    address2='Suite 1',
    city='Farmington',
    state='UT',
    zip_code=84025,
    images=img_dict,
)
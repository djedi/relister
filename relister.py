import os
import json

import requests


LOGIN_URL = 'https://www.ksl.com/public/member/signin'


def enum(**enums):
    return type('Enum', (), enums)

AD_TYPES = enum(sale='sale', wanted='wanted')
SELLER_TYPES = enum(private='Private', business='Business')


class Relister(object):
    session = requests.session()
    id = None
    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        self.photos = []

    def login(self, email, password):
        """
        Log in to KSL.com
        :param email:
        :param password:
        :return:
        """
        print "logging in..."
        self.session.get(LOGIN_URL)
        payload = {
            'MAX_FILE_SIZE': '50000000',
            'dado_form_3': 1,
            'member[email]': email,
            'member[password]': password,
        }
        resp = self.session.post(LOGIN_URL, payload)

    def post_item(self, category, subcategory, price, title, description,
                  display_name, email, phone, city, state, zip_code,
                  ad_type='Sale', seller=SELLER_TYPES.private,
                  images=None, accept_text=1):
        """
        Post classified item to KSL.com
        :param category: category name
        :param subcategory: sub-category name
        :param price: asking price
        :param title: classified title
        :param description: descriptive text
        :param display_name: name of contact person
        :param email: contact email
        :param phone: phone as 10 digit number 8015551234

        :param city: city
        :param state: state, 2 digit code eg. 'UT'
        :param zip_code: zip code

        :param ad_type: 'Sale' or 'Wanted'
        :param seller: 0=private, 1=business
        :param images: dict or OrderedDict of local image paths
        :param accept_text: phone number can receive texts? 1=yes, 0=no
        :return:
        """
        url = 'https://www.ksl.com/classifieds/sell'

        # Get sid & fid
        print "initializing..."
        resp = self.session.get(url)
        if self.debug:
            open('0.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        self.get_session_id()

        # upload images
        for key in images.keys():
            self.upload_photo(images[key])

        photo_order = ','.join([p['id'] for p in self.photos])

        payload = {
            'acceptText': accept_text,
            'category': category,
            'city': city,
            'description': description,
            'email': email,
            'id': self.id,
            'lat': '',
            'latLonSource': '',
            'lon': '',
            'marketType': ad_type,
            'name': display_name,
            'photoOrder': photo_order,
            'price': '${}'.format(price),
            'primaryPhone': phone,
            'sellerType': seller,
            'state': state,
            'subCategory': subcategory,
            'title': title,
            'zip': zip_code,
        }
        url = 'https://www.ksl.com/classifieds/sell/save-main-ad-data'
        resp = self.session.post(url, payload)
        if self.debug:
            open('1.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        url = 'https://www.ksl.com/classifieds/sell/activate-ad'
        payload = {
            'id': self.id,
        }
        resp = self.session.post(url, payload)
        if self.debug:
            open('2.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

    def get_session_id(self):
        """
        Makes call to create an ad session ID
        :return: session Id
        """
        url = 'https://www.ksl.com/classifieds/sell/create-stub?' \
              'XDEBUG_SESSION_START=1'
        resp = self.session.post(url)
        resp_obj = json.loads(resp.text)
        self.id = resp_obj['adId']
        return self.id

    def upload_photo(self, img_path):
        """
        Uploads an image to the ad
        :param img_path: local path of image to upload. Should be 640x480
        :return:
        """
        print 'uploading {}'.format(img_path)
        img_basename = os.path.basename(img_path)
        img_size = os.path.getsize(img_path)
        url = 'https://www.ksl.com/classifieds/sell/upload-photo?id={}&' \
              'qqfile={}'.format(self.id, img_basename)

        headers = {
            'Content-Type': 'multipart/form-data',
            'X-File-Name': img_basename,
            'X-File-Size': img_size,
            'X-Requested-With': 'XMLHttpRequest',
        }

        resp = self.session.post(url, headers=headers, data=open(img_path, 'rb'))
        obj = json.loads(resp.text)
        self.photos.append(obj)
        if self.debug:
            open('img.json', 'w').write(resp.text.encode('utf-8', 'ignore'))

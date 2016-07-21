from collections import OrderedDict

from bs4 import BeautifulSoup
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
                  display_name, email, home_phone, address, city, state,
                  zip_code,
                  ad_type='Sale', seller=SELLER_TYPES.private, work_phone=None, cell_phone=None,
                  address2=None, images=None):
        """
        Post classified item to KSL.com
        :param category: category name
        :param subcategory: sub-category name
        :param price: asking price
        :param title: classified title
        :param description: descriptive text
        :param display_name: name of contact person
        :param email: contact email
        :param home_phone: phone as 10 digit number 8015551234

        :param address: address line 1
        :param address2: address line 2
        :param city: city
        :param state: state, 2 digit code eg. 'UT'
        :param zip_code: zip code

        :param ad_type: 'Sale' or 'Wanted'
        :param seller: 0=private, 1=business
        :param work_phone: phone as 10 digit number 8015551234
        :param cell_phone: phone as 10 digit number 8015551234
        :param images: dict or OrderedDict of local image paths
        :return:
        """
        url = 'https://www.ksl.com/classifieds/sell-v1/s1'

        # Get sid & fid
        print "initializing..."
        resp = self.session.get(url)
        if self.debug:
            open('0.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        home = self.split_phone(home_phone)
        work = self.split_phone(work_phone)
        cell = self.split_phone(cell_phone)

        payload = {
            'category': category,
            'subCategory': subcategory,
            'price': price,
            'title': title,
            'marketType': ad_type,
            'sellerType': seller,
            'description': description,
            'next': 'Next Page >>',
        }
        url = 'https://www.ksl.com/classifieds/sell-v1/s1-submit'
        resp = self.session.post(url, payload)
        if self.debug:
            open('1.html', 'w').write(resp.text.encode('utf-8', 'ignore'))
        soup = BeautifulSoup(resp.text, 'lxml')
        self.id = soup.find('input', attrs={'name': 'id'}).attrs['value']

        print "adding contact info"
        payload = {
            'id': self.id,
            'name': display_name,
            'email': email,
            'confirmEmail': email,
            'homePhoneAreaCode': home[0],
            'homePhonePrefix': home[1],
            'homePhoneSuffix': home[2],
            'workPhoneAreaCode': work[0],
            'workPhonePrefix': work[1],
            'workPhoneSuffix': work[2],
            'cellPhoneAreaCode': cell[0],
            'cellPhonePrefix': cell[1],
            'cellPhoneSuffix': cell[2],
            'address1': address,
            'address2': address2,
            'city': city,
            'state': state,
            'zip': zip_code,
            'next': 'Next Page >>',
        }

        url = 'https://www.ksl.com/classifieds/sell-v1/s2-submit/id/{}'.format(
            self.id)
        resp = self.session.post(url, payload)
        if self.debug:
            open('2.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        # upload images
        for key in images.keys():
            self.upload_image(images[key], key)

        print "accepting terms"
        url = 'https://www.ksl.com/classifieds/sell-v1/' \
              's-post-tos-submit/id/{}'.format(self.id)
        payload = {
            'id': self.id,
            'memberstuff': '',
            'next': 'Next Page >>',
        }
        resp = self.session.post(url, payload)
        if self.debug:
            open('3.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

    def upload_image(self, img_path, description=''):
        """
        Uploads an image to the ad
        :param img_path: local path of image to upload. Should be 640x480
        :param description: image description
        :return:
        """
        print 'uploading {} - {}'.format(img_path, description)
        url = 'https://www.ksl.com/classifieds/sell-v1/upload-photo'

        payload = {
            'id': self.id,
            'MAX_FILE_SIZE': 10000000,
            'description': description,
            'imageFileSubmit': 'Upload file',
        }

        files = {
            'imageFile': ('image.jpg', open(img_path, 'rb')),
        }

        resp = self.session.post(url, payload, files=files)
        if self.debug:
            open('image.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

    @staticmethod
    def split_phone(phone):
        """
        Split a 10 digit phone number into its parts
        :param phone: phone number eg. 8015551234
        :return: array of parts eg. ['801', '555', '1234']
        """
        if not phone:
            return ['', '', '']
        phone = str(phone)
        return [
            phone[:3],
            phone[3:6],
            phone[-4:]
        ]

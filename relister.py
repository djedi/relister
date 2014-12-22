from collections import OrderedDict

from bs4 import BeautifulSoup
import requests


LOGIN_URL = 'https://www.ksl.com/public/member/signin'


def enum(**enums):
    return type('Enum', (), enums)

AD_TYPES = enum(sale='sale', wanted='wanted')
SELLER_TYPES = enum(private=0, business=1)


class Relister(object):
    session = requests.session()
    sid = None
    fid = None

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
                  ad_type='sale', seller=0, work_phone=None, cell_phone=None,
                  address2=None, images=None):
        """
        Post classified item to KSL.com
        :param category: category ID
        :param subcategory: sub-category ID
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

        :param ad_type: 'sale' or 'wanted'
        :param seller: 0=private, 1=business
        :param work_phone: phone as 10 digit number 8015551234
        :param cell_phone: phone as 10 digit number 8015551234
        :param images: dict or OrderedDict of local image paths
        :return:
        """
        # https://www.ksl.com/index.php?nid=640&form_3=345&form_4=615
        url = 'https://www.ksl.com/index.php?nid=640&form_3={}&form_4={}'.format(
            category, subcategory)

        # Get sid & fid
        print "getting sid & fid"
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        self.sid = soup.find('input', attrs={'name': 'sid'}).attrs['value']
        self.fid = soup.find('input', attrs={'name': 'fid'}).attrs['value']
        form_45 = soup.find('input', attrs={'name': 'form_45'}).attrs['value']

        base_payload = {
            'nid': 640,
            'sid': self.sid,
            'fid': self.fid,
            'next': 'Next Page >>',
        }

        home = self.split_phone(home_phone)
        work = self.split_phone(work_phone)
        cell = self.split_phone(cell_phone)
        payload = dict(base_payload.items() + {
            'form_3': category,
            'form_4': subcategory,
            'form_6': price,
            'form_8': title,
            'form_136': 'sale',
            'form_135': 0,  # private
            'form_9': description,
            'form_45': form_45,
        }.items())
        print "creating the ad"
        resp = self.session.post(url, payload)
        open('1.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        payload = OrderedDict(base_payload.items() + {
            # page 2
            'form_11': display_name,
            'form_12': email,
            'form_13': email,
            'form_73_a': home[0],
            'form_73_b': home[1],
            'form_73_c': home[2],
            'form_74_a': work[0],
            'form_74_b': work[2],
            'form_74_c': work[1],
            'form_75_a': cell[0],
            'form_75_b': cell[1],
            'form_75_c': cell[2],
            'form_34': address,
            'form_35': address2,
            'form_36': city,
            'form_37': state,
            'form_38': zip_code,
        }.items())
        payload = OrderedDict(sorted(payload.items(), key=lambda t: t[0]))
        print payload
        print "adding contact info"
        resp = self.session.post(url, payload)
        soup = BeautifulSoup(resp.text, 'lxml')
        aid = soup.find('input', attrs={'name': 'aid'}).attrs['value']
        open('2.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        # upload images
        for key in images.keys():
            self.upload_image(aid, images[key], key)

        print "accepting terms"
        resp = self.session.post(url, base_payload)
        open('3.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

        payload = dict(base_payload.items() + {
            'memberstuff': '',
            'post_source': 'desktop',
        }.items())
        print "publishing ad"
        resp = self.session.post(url, payload)
        open('4.html', 'w').write(resp.text.encode('utf-8', 'ignore'))

    def upload_image(self, aid, img_path, description=''):
        """
        Uploads an image to the ad
        :param img_path: local path of image to upload. Should be 640x480
        :return:
        """
        print 'uploading {} - {}'.format(img_path, description)
        url = 'https://www.ksl.com/resources/form/upload.php'

        payload = {
            'nid': 640,
            'sid': self.sid,
            'fid': self.fid,
            'source': 'airlock',
            'aid': aid,
            'MAX_FILE_SIZE': 10000000,
            'd-142': description,
            's-142': 'Upload file',
        }

        files = {
            '142': ('image.jpg', open(img_path, 'rb')),
        }

        resp = self.session.post(url, payload, files=files)
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

"""import os
from PIL import Image
//from PIL.ExifTags import TAGS

print(TAGS)"""
import io
import re
import urllib.request

import PIL
import lxml.html
from PIL import Image
import requests
# from StringIO import StringIO
from urllib.request import urlopen
from html.parser import HTMLParser
import urllib.request as urllib
from bs4 import BeautifulSoup as bs, BeautifulSoup
from mechanize import Browser
from lxml.html import parse


class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, attributes):
        self.match = tag == 'title'

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False


def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


string = 'Australia says Pfizer to expand COVID-19 vaccine supply amid Sydney outbreak https://t.co/Rn9JGvpDAV https://t.co/Oqzy3UdD4C https://t.co/gl2INtZwwQ https://t.co/bQqC7Og2o3'
urls = Find(string)
for x in urls:
    print("Urls: ", x)
    ur = requests.get(f'{x}').url
    print(ur)
    # response = requests.get(ur)
    r = requests.get(ur)
    soup = bs(r.content, 'lxml')
    try:
        print(soup.select_one('title').text)
    except:
        print(ur)
        """urlData = urllib.urlopen(ur)
        data = str(urlData.readlines())
        bs = BeautifulSoup(data)
        imgUrl = bs.find('img', attrs={'alt': 'Embedded image permalink'}).get('src')
        urllib.urlretrieve(imgUrl, "cnn.jpg")"""

    """html_string = str(urlopen(ur).read())
    parser = TitleParser()
    parser.feed(html_string)
    print(parser.title)  # prints: Example Domain

media_files = set()
for status in string:
    media = status.entities.get('media', [])
if(len(media) > 0):
    media_files.add(media[0]['media_url'])

response = requests.get("https://i.imgur.com/ExdKOOz.png")
image_bytes = io.BytesIO(response.content)

img = PIL.Image.open(image_bytes)
img.show()"""

url = 'https://t.co/Rn9JGvpDAV'
filename = url.split('/')[-1]
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)

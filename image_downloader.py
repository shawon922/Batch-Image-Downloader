import datetime
import os
import re
import urllib.request as ulib
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup as BS

import pyperclip
import sys
from urllib.parse import urlparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

now = datetime.datetime.now()

today = str(datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)).replace(' ', '_').replace(':', '_')


def download_image(image_link, image_name):
    with open(today + '/' + image_name, 'wb') as file_obj:
        resp = ulib.urlopen(image_link)
        file_obj.write(resp.read())


def get_image_src(link):
    try:
        response = requests.get(link, headers=headers)
    except (IOError, requests.ConnectionError, requests.HTTPError):
        print('Exception....')
        return []

    beautiful_obj = BS(response.content, 'html.parser')

    image_tags = beautiful_obj.find_all('img')

    src_list = [image_tag['src'] for image_tag in image_tags if image_tag.has_attr('src')]

    return src_list


def get_page_links(bs_obj):
    anchor_tags = bs_obj.find_all('a')

    anchor_link_list = [anchor_tag['href'] for anchor_tag in anchor_tags if anchor_tag.has_attr('href')]

    return anchor_link_list


def crawler(url, all_link='n'):
    response = ''
    too_much = ''
    page_links = []

    try:
        response = requests.get(url, headers=headers)
    except (IOError, requests.ConnectionError, requests.HTTPError):
        print('Invalid link..')
        exit()

    if response.status_code != 200:
        print('Bad status code : '+ response.status_code)
        exit()

    beautiful_obj = BS(response.content, 'html.parser')

    page_links.append(url)

    if all_link in ['y', 'Y']:
        page_links.extend(get_page_links(beautiful_obj))

    visited_links = []
    downloaded_images = []

    for page_link in page_links:

        if not re.match(url, page_link):
            page_link = url + page_link.lstrip('/')

        if page_link not in visited_links:
            visited_links.append(page_link)

            image_srcs = get_image_src(page_link)

            if len(image_srcs) > 0:
                os.makedirs(today, exist_ok=True)

            with ThreadPoolExecutor(max_workers=10) as executor:
                for image_src in image_srcs:

                    if image_src not in downloaded_images:
                        downloaded_images.append(image_src)

                        image_name = str(image_src.split('/')[-1]).split('?')[0]

                        if (re.match('http://', image_src) or re.match('https://', image_src)) and (
                            re.search('.png', image_src) or re.search('.jpg', image_src)):
                            image_link = image_src
                            print(image_link)
                        elif re.search('.png', image_src):
                            image_link = url + image_src
                            print(image_link)
                        elif re.search('.jpg', image_src):
                            image_link = url + image_src
                            print(image_link)
                        else:
                            image_link = ''

                        if image_link:
                            executor.submit(download_image, image_link, image_name)

                        if len(downloaded_images) >= 50 and too_much == '':
                            too_much = input('Too much images. Want to stop ? <y or n> : ').strip() or 'y'
                            if too_much[0] not in ['y', 'Y', 'n', 'N']:
                                too_much = 'y'

                        if too_much in ['y', 'Y']:
                            exit()


"""
Use the system clipboard, get the copied link,
check if it's empty or not. Also check if there's any
cmd arg or not. If both conditions fail, proceed to ask the
use for input. (Makes the program convenient)
"""


# used for validating url
def validate_url(url_link):
    parsed_url = urlparse(url_link)

    if not parsed_url.scheme and not parsed_url.netloc:
        return False
    else:
        return True


def get_validated_url_from_clip():
    paste_data = pyperclip.paste()

    if validate_url(paste_data):
        return paste_data
    else:
        return ''


validated_url = get_validated_url_from_clip()

# checks if clipboard has something and also a cmd arg
if validated_url and len(sys.argv) == 2:
    url = validated_url
    visit_all = sys.argv[1]

# ask for user input, none are present
else:
    url = input('Enter a url: ').strip()
    visit_all = input('Want to visit sub-pages? <n or y> : ').strip() or 'n'


# check the url and visit_all var
if visit_all[0] not in ['y', 'Y', 'n', 'N']:
    visit_all = 'n'

if url[-1] != '/':
    url += '/'

crawler(url, visit_all[0])

#! python3
"""
scheduledComicDownloader.py - checks websites and downloads new comic if exists since last check.
"""

import os
import requests
import bs4
from urllib.parse import urljoin


def get_comic(site_name, url):
    """
    Downloads an image to the local directory. Check if image exist locally before downloading.
    :param site_name: string. Name of the website.
    :param url: A full web address to the image to downloaded
    :return: none
    """
    download_path = 'C:/Users/HOME4400/Desktop/comic_images'
    image_name = os.path.basename(url)
    os.makedirs(os.path.abspath(download_path), exist_ok=True)

    print('Checking {}... '.format(site_name), end='')
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print('Requests Exception: {}'.format(e))
        return

    if image_name in os.listdir(download_path):  # check if comic has been previously downloaded
        print('Image already exists. No new comic today!')
        return
    else:
        print('Downloading {}...'.format(url), end='')
        file_object = open(os.path.join(download_path, image_name), 'wb')
        for chunk in res.iter_content(100000):
            file_object.write(chunk)
        file_object.close()
        print(' Complete. Enjoy!')

# List of the site we want to check for new images.
comic_sites = {'xkcd': {'url': 'http://xkcd.com/',
                        'selector': '#comic img'},
               'Left-Handed Toons': {'url': 'http://www.lefthandedtoons.com',
                                     'selector': 'img.comicimage'},
               'Two Guys and Guy': {'url': 'http://www.twogag.com',
                                    'selector': '#comic img'},
               'Savage Chickens': {'url': 'http://www.savagechickens.com',
                                   'selector': '.entry_content'}}
# 'Bizarro': {'url': 'http://bizarro.com',
#             'selector': 'div#comicpanel img'}}

# Loop through sites and data from dictionary
for site, contents in comic_sites.items():
    try:
        rq = requests.get(contents['url'])
        rq.raise_for_status()
        soup = bs4.BeautifulSoup(rq.text, 'lxml')
        comic_elem = soup.select(contents['selector'])
        comic_rel_url = comic_elem[0].get('src')
        comic_abs_url = urljoin(contents['url'], comic_rel_url)  # combine root site and relative url

        get_comic(site, comic_abs_url)

    except requests.RequestException as err:
        print('Requests Exception: {}'.format(err))
    except Exception as err:
        print('Something ELSE went wrong: {}'.format(err))

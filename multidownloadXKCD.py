#! python3
"""
multidownloadXKCD.py - Downloads XKCD comics using multiple threads
"""

import requests
import os
import bs4
import threading


os.makedirs('xkcd', exist_ok=True)  # stores comic in ./xkcd

def downloadXkcd(startComic, endcomic):
    for urlNumber in range(startComic, endcomic):
        # Download the page.
        print('Downloading page http://xkcd.com/%s...' % urlNumber)
        res = requests.get('http://xkcd.com/%s' % urlNumber)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Find the URL of the comic image.
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            try:
                comicUrl = 'http:' + comicElem[0].get('src')
                # Download the iamge.
                print('Downloading image %s...' % comicUrl)
                res = requests.get(comicUrl)
                res.raise_for_status()
            except requests.exceptions.MissingSchema:
                print('Missing schema.')
                # skip this comic
                continue

            # Save the image to ./xkcd.
            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

# create and start the thread objects.
downloadThreads = []                # a list of all the Thread objects
for i in range(0, 1400, 100):       # loops 14 times, creates 14 threads
    downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))
    downloadThreads.append(downloadThread)
    downloadThread.start()

# wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()

print('Done')

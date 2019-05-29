import urllib.request as url
import os
import numpy as np
import requests

from multiprocessing import Pool
from pathlib import Path

DIRECTORY = '/home/hackerton/image_url'


def write_content(directory, content_name, wid):
    if not os.path.isdir(directory):
        os.mkdir(directory)

    file_loc = directory + '/' + content_name
    my_file = Path(file_loc)
    base_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='

    if not my_file.is_file():
        try:
            web_page = requests.get(base_url + wid, timeout=1)

            with open(file_loc, 'w') as file:
                file.write(web_page.text)
        except requests.RequestException as e:
            print(e)


def grab_inter(wid):
    write_content(DIRECTORY, wid + '.txt', wid)


def main():
    list_array = []

    with open('./imagenet_synset_list.txt', 'r') as file:
        for line in file:
            list_array.append(line.replace('\n', ''))

    print('Downloading Imagenet dataset!')
    with Pool(50) as p:
        p.map(grab_inter, list_array)

    print('Finished downloading dataset!')


if __name__ == '__main__':
    main()

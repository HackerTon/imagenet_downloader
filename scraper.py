import os
import requests
import logging

from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def get_image(link, wid):
    path = os.path.join('imagenet', wid)
    imgdir_path = Path(path)

    if not imgdir_path.exists():
        try:
            os.makedirs(imgdir_path)
        except Exception as e:
            print(f'Misc Error: {e}')

    imgname = os.path.split(link)[-1].replace(' ', '').replace('\r', '')
    imgpath = os.path.join(path, imgname)

    if not os.path.isfile(imgpath):
        try:
            web = requests.get(link, timeout=1)
            web.raise_for_status()

            image = Image.open(BytesIO(web.content))
            image.save(imgpath)
        except Exception as e:
            # print(f'Misc Error:')
            pass
        else:
            print(f'Save {imgpath}')


def get_link(directory, wid):
    content_name = wid + '.txt'
    file_loc = directory + '/' + content_name

    file_path = os.path.join(directory, content_name)
    my_file = Path(file_path)

    base_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='

    try:
        web_page = requests.get(base_url + wid)

        for link in web_page.text.split('\n'):
            get_image(link, wid)

        web_page.raise_for_status()
    except Exception as e:
        print(f'Misc Error: {e}')

    # if not my_file.is_file():
    #     try:
    #         web_page = requests.get(base_url + wid)

    #         with open(file_loc, 'w') as file:
    #             file.write(web_page.text)
    #     except requests.RequestException as e:
    #         print(e)


def grab_inter(wid):
    get_link('list', wid)


def generator():
    with open('./imagenet_synset_list.txt', 'r') as file:
        for line in file:
            url = line.replace('\n', '')

            yield url


def main():
    if not os.path.exists('imagenet_synset_list.txt'):
        print('Imagenet Synset List Not Found')
        print('Downloading it from imagenet.org')

        listurl = 'http://www.image-net.org/api/text/imagenet.synset.obtain_synset_list'

        try:
            response = requests.get(listurl)

            with open('imagenet_synset_list.txt', 'w') as file:
                file.write(response.text)
        except requests.RequestException as e:
            print(e)

    if not os.path.exists('list'):
        print('List directory not found')

        try:
            os.makedirs('list')
        except Exception as e:
            print(f'Misc Error: {e}')

    if not os.path.exists('imagenet'):
        print('Imagenet directory not found!')

        try:
            os.makedirs('imagenet')
        except Exception as e:
            print(f'Misc Error: {e}')

    print('Starting downloading!')
    with ThreadPoolExecutor() as executor:
        executor.map(grab_inter, generator(), chunksize=5)

    print('Finish Downloading')


if __name__ == '__main__':
    main()

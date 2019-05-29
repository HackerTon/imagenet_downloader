import os
import matplotlib.pyplot as plt
import urllib3
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import timeit
from multiprocessing import Pool

DIRECTORY_URL = '/home/hackerton/dp1'
DIRECTORY_IMAGE = '/home/hackerton/image'

link = os.listdir('/home/hackerton/dp1')[1]


def grabber(link):
    with open(DIRECTORY_URL + '/' + link, 'r') as file_link:
        i = 0

        directory_image_temp = DIRECTORY_IMAGE + '/' + link.replace('.txt', '')

        if not os.path.isdir(directory_image_temp):
            os.mkdir(directory_image_temp)

        for line in file_link:
            try:
                webpage = requests.get(line, timeout=1)
                image = Image.open(BytesIO(webpage.content))

                image.save(directory_image_temp + '/' + str(i) + '.jpg')

                i = i + 1
            except OSError:
                pass


def main():
    links = os.listdir(DIRECTORY_URL)

    with Pool(processes=50) as p:
        p.map(grabber, links)


if __name__ == '__main__':
    main()

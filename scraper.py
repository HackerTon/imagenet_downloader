import urllib.request as url
import os
from pathlib import Path

print("In Progress")

with open('./imagenet_synset_list.txt', 'r') as file:

    for line in file:

        content = url.urlopen('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + line)

        # Change to string

        content = str(content.read().decode('utf-8'))

        if not os.path.exists('./url_folder'):
            os.makedirs('./url_folder')
            with open('./url_folder/' + line + '.txt', 'w') as url_file:
                url_file.write(content)
        else:
            with open('./url_folder/' + line + '.txt', 'w') as url_file:
                url_file.write(content)

import sys
import os
import requests
import asyncio
import random
import io
import base64
import json
import time
from io import BytesIO
from PIL import Image
from time import gmtime, strftime
import parameters

# set all non-black color to a random color

# image route (relative)
IMAGE_FOLDER = '/images/'

def randomize_image_color(image_name):
    # load prompt image from png to base64 format
    img = Image.open(f'.\{image_name}')
    img = img.convert("RGB")
    pixels = img.load() # create the pixel map
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            if pixels[i,j] != (0, 0, 0):
                pixels[i,j] = (int(random.random()*256), int(random.random()*256), int(random.random()*256))
    img.save(f'.\(randomized){image_name}')
    print(f'randomized image saved to .\(randomized){image_name}')

if __name__ == '__main__':
    start_time = time.time()
    
    print(f'len(sys.argv) = {len(sys.argv)}')
    if (len(sys.argv) >= 2):
        randomize_image_color(sys.argv[1])
    else:
        print('expect argv[1] = image name')

    end_time = time.time()
    time_lapsed = end_time - start_time
    print(f'Total time elapsed: {time_lapsed}s')
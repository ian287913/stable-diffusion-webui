import sys
import os
import requests
import asyncio
import random
import io
import base64
from PIL import Image
from time import gmtime, strftime


TEXT_PROMPT = 'A detailed 3d character design of one (goldfish) character in the style of pixar'
TEXT_PROMPT_NEGATIVE = ''

# image route (relative)
IMAGE_FOLDER = '/images/'

AI_MODEL = ['v1-5-pruned.ckpt [e1441589a6]']

# stable diffusion api url
URL = "http://127.0.0.1:7860"

def prepare_environment():
    base_path = os.getcwd()
    target_path = base_path + IMAGE_FOLDER + '/'

    # check and generate folder
    os.makedirs(base_path + IMAGE_FOLDER, exist_ok=True)
    os.makedirs(target_path, exist_ok=True)

    # call stable diffusion
    # set model
    print('set model for generation', flush=True)
    payload = {
        "sd_model_checkpoint": AI_MODEL[0],
    }
    response = requests.post(url=f'{URL}/sdapi/v1/options', json=payload)
    print('finish model setting!', flush=True)

    return target_path


def generate_image(target_path):
    payload = {
    "prompt": "maltese puppy",
    "steps": 5
    }
    response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        image.save(target_path + strftime("%Y%m%d_%H%M%S", gmtime()) + '(' + str(0) + ').png')#, pnginfo=pnginfo)


if __name__ == '__main__':
    target_path = prepare_environment()
    generate_image(target_path)

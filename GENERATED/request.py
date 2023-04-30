import sys
import os
import requests
import asyncio
import random
import io
import base64
import json
from io import BytesIO
from PIL import Image
from time import gmtime, strftime
import parameters


TEXT_PROMPT = 'A detailed 3d character design of one (goldfish) character in the style of pixar'
TEXT_PROMPT_NEGATIVE = ''

# image route (relative)
IMAGE_FOLDER = '/images/'

# stable diffusion api url
URL = "http://127.0.0.1:7860"

def prepare_environment():
    base_path = os.getcwd()
    target_path = base_path + IMAGE_FOLDER + '/' + strftime("%Y%m%d_%H%M%S", gmtime()) + '/'

    # check and generate folder
    os.makedirs(base_path + IMAGE_FOLDER, exist_ok=True)
    os.makedirs(target_path, exist_ok=True)

    # call stable diffusion
    # set model
    print('set model for generation', flush=True)
    payload = {
        "sd_model_checkpoint": parameters.PARAMETERS['sd_model_checkpoint'][0],
    }
    response = requests.post(url=f'{URL}/sdapi/v1/options', json=payload)
    print('finish model setting!', flush=True)

    return target_path

# merge rows * cols PIL images into a grid
def images2grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def update_progress(current, target):
    print(f'{current} of {target} images generated. ({(100.0 * float(current) / float(target)):6.2f}%)', flush=True)

def generate_single_image(payload):
    response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/img2img', json=payload)
    status_code = response.status_code
    r = response.json()

    image_list = []

    if (status_code != 200):
        print(f"ERROR status_code = {status_code}")
        print(f"response = {r}")
    else:
        # print(f"images count = {len(r['images'])}", flush=True)
        # print(f"parameters = \n{r['parameters']}\n", flush=True)
        # print(f"info = \n{r['info']}\n", flush=True)

        for idx, i in enumerate(r['images']):
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            image_list.append(image)

            # png_payload = {
            #     "image": "data:image/png;base64," + i
            # }
            # response2 = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/png-info', json=png_payload)
            # print(f'png info = {response2.json().get("info")}')
    
    if (len(image_list) == 0):
        return None
    if (len(image_list) != 1):
        print(f'size of image_list should be 1 but getting {len(image_list)}!')
    return image_list[0]

def generate_image(target_path):
    
    # load prompt image from png to base64 format
    prompt_image = Image.open(f'.\{parameters.PARAMETERS["image_prompt"]}')
    prompt_image = prompt_image.convert("RGB")
    output_buffer = BytesIO()
    prompt_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    prompt_image_b64 = base64.b64encode(byte_data).decode('ascii')

    # output the config json (parameters)
    with open(f"{target_path}parameters.json", "w") as fp:
        json.dump(parameters.PARAMETERS, fp)

    # progress settings
    total_image_count = len(parameters.PARAMETERS["denoising_strength"]) * \
        len(parameters.PARAMETERS["cfg_scale"]) * \
        len(parameters.PARAMETERS["steps"]) * \
        parameters.PARAMETERS["batch_width"]**2
    generated_image_count = 0

    payloads = []
    for dns_idx, dns in enumerate(parameters.PARAMETERS["denoising_strength"]):
        for cfg_idx, cfg in enumerate(parameters.PARAMETERS["cfg_scale"]):
            for step_idx, step in enumerate(parameters.PARAMETERS["steps"]):
                image_list = []
                image_name = f'cfg={cfg} dns={dns} step={step}'
                start_seed = parameters.PARAMETERS["seed"]
                for s in range(0, parameters.PARAMETERS["batch_width"]**2):
                    seed = start_seed + s

                    # set payload
                    payload = {}
                    payload["init_images"] = [prompt_image_b64]
                    payload["prompt"] = parameters.PARAMETERS["prompt"]
                    payload["negative_prompt"] = parameters.PARAMETERS["negative_prompt"]
                    payload["sampler_index"] = parameters.PARAMETERS["sampler_index"]
                    ##payload["include_init_images"] = parameters.PARAMETERS["include_init_images"]

                    # set payload (in list)
                    payload["denoising_strength"] = dns
                    ##payload["image_cfg_scale"] = cfg
                    payload["cfg_scale"] = cfg
                    payload["steps"] = step

                    # set payload (in batch)
                    payload["batch_size"] = 1
                    payload["seed"] = seed

                    # generate image
                    image = generate_single_image(payload)
                    image.save(target_path + image_name + ' (' + str(s) + ').png')
                    image_list.append(image)

                    # update progress
                    generated_image_count += 1
                    update_progress(generated_image_count, total_image_count)
                
                # export images
                image_grid = images2grid(image_list, parameters.PARAMETERS["batch_width"], parameters.PARAMETERS["batch_width"])
                image_grid.save(target_path + '_GRID ' + image_name + '.png')
                

    return

    payload = {}
    payload["init_images"] = [prompt_image_b64]
    payload["prompt"] = parameters.PARAMETERS["prompt"]
    payload["negative_prompt"] = parameters.PARAMETERS["negative_prompt"]
    
    payload["denoising_strength"] = parameters.PARAMETERS["denoising_strength"][0]
    ##payload["image_cfg_scale"] = parameters.PARAMETERS["cfg_scale"][0]
    payload["cfg_scale"] = parameters.PARAMETERS["cfg_scale"][0]
    payload["steps"] = parameters.PARAMETERS["steps"][0]

    payload["batch_size"] = parameters.PARAMETERS["batch_size"]
    payload["seed"] = parameters.PARAMETERS["seed"]

    payload["sampler_index"] = parameters.PARAMETERS["sampler_index"]

    payload["include_init_images"] = parameters.PARAMETERS["include_init_images"]
    
    

    response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/img2img', json=payload)
    status_code = response.status_code
    r = response.json()

    if (status_code != 200):
        print(f"status_code = {status_code}")
        print(f"response = {r}")
    else:
        print(f"images count = {len(r['images'])}", flush=True)
        print(f"parameters = \n{r['parameters']}\n", flush=True)
        print(f"info = \n{r['info']}\n", flush=True)

        for idx, i in enumerate(r['images']):
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
            image.save(target_path + '(' + str(idx) + ').png')#, pnginfo=pnginfo)


if __name__ == '__main__':
    target_path = prepare_environment()
    generate_image(target_path)

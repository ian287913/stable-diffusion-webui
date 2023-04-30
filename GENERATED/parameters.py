PARAMETERS = {
    'sd_model_checkpoint' : ['v1-5-pruned.ckpt [e1441589a6]'],
    'image_prompt' : 'image prompt gray.png',

    'prompt' : "A detailed 3d character design of one (regal_blue_tang) character in the style of pixar, black background, side view, detailed fish scale, concept artwork by pixar, character design by pixar, 8k, uhd, high definition, unreal 5, daz, octane render", 

    'negative_prompt' : "((duplicate)) ((culled)) (((out of frame))) (((deformed))) ((bad anatomy)) ((extra eyes)) ((without head)) ((disfigured))",

    'cfg_scale' : [10, 11, 12],
    'denoising_strength' : [0.80],
    'steps' : [60, 80, 100],
    # generate total batch_width**2 images
    'batch_width' : 3,
    'seed' : 1,
    "sampler_index": "Euler a",
    'include_init_images' : True
    #sampler_name
    #mask_blur = 4
    #"include_init_images": false,
}

# this is for INPAINTING
PARAMETERS = {
    'sd_model_checkpoint' : ['v1-5-pruned.ckpt [e1441589a6]'],
    'image_prompt' : 'front_rendered/front_rendered_rgb ex0.png',
    'mask' : 'front_rendered/front_inpaint_mask_rgb ex0.png',
    ##'image_prompt' : 'image prompt random.png',
    'prompt_species' : ['tuna'],
    ##'prompt_species' : ['regal blue tang'],
    'prompt' : "A detailed 3d character design of one (tuna) character in the style of pixar, front view, black background, detailed fish scale, concept artwork by pixar, character design by pixar, 8k, uhd, high definition, unreal 5, daz, octane render", 

    'negative_prompt' : "((duplicate)) ((culled)) (((out of frame))) (((deformed))) ((bad anatomy)) ((extra eyes)) ((without head)) ((disfigured))",

    'cfg_scale' : [1, 2, 3, 5],
    'denoising_strength' : [0.6, 0.7, 0.8],
    'steps' : [70],
    # generate total batch_width**2 images
    'batch_width' : 3,
    'seed' : 1,
    "sampler_index": "Euler",
    'include_init_images' : True
    #sampler_name
    #mask_blur = 4
    #"include_init_images": false,
}
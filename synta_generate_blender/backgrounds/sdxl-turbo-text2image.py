#module load anaconda3;module load cuda cudnn;cd stable_diffusion;
#source activate stable_diffusion
import mediapy as media
import random
import sys
import torch

from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
    )

pipe = pipe.to("cuda")

#prompt = "castle at night photorealistic ISO 800, dslr, 1/250s, F/2,8, 38 mm, Fujifilm XT3" 
#prompt = "beautiful city in sunset photorealistic, ISO 800, dslr, 1/250s, F/2,8, 38 mm, Fujifilm XT3, high resolution"
#prompt = "raining in farm photorealistic, ISO 800, dslr, 1/250s, F/2,8, 38 mm, Fujifilm XT3, high resolution"
#prompt = "A high-resolution image of a desert oasis taken with a DSLR camera, ISO 400, 1/125s, F/2.8, 24mm lens, shot with a Fujifilm XT3. The sunrise casts a soft, warm light over the palm trees and water, with the desert sands subtly illuminated in the background"
#prompt = "A high-resolution photograph of a vast, clear blue sky filled with soft, white clouds, captured with a Fujifilm XT3, ISO 200, 1/250s, F/8, 24mm lens. The clouds are scattered across the sky, creating a serene and peaceful atmosphere, with subtle variations in light and shadow that add depth to the image."
#prompt = "A high-resolution photograph of the calm ocean with soothing waves captured with a Fujifilm XT3, ISO 1600, 1/500s, F/4, 38mm lens photorealistic."
#prompt = "A high-resolution photograph of the far away galaxy captured with hyper realistic details, hubble telescope, nasa published, ISO 1600, 1/500s, F/4, 38mm lens photorealistic."
#prompt = "A high-resolution photograph of a evening in a forest with a DSLR camera, ISO 400, 1/125s, F/2.8, 24mm lens, shot with a Fujifilm XT3."
#prompt = "A high-resolution photograph of a stormy night captured with a Fujifilm XT3, ISO 1600, 1/500s, F/4, 38mm lens photorealistic hyper real."
#prompt = "A hyper-realistic photograph of a grand room inside the White House, captured with a Fujifilm XT3, ISO 800, 1/125s, F/2.8, 24mm lens. The room features classic American architecture, with ornate moldings, high ceilings, and a large crystal chandelier hanging in the center."
#prompt = "A hyper-realistic photograph of a modern office interior, captured with a Fujifilm XT3, ISO 800, 1/125s, F/2.8, 24mm lens. The office features sleek, contemporary design with clean lines and minimalistic decor. A large glass window wall allows natural light to flood the space, offering a view of the city skyline."
#prompt = "beautiful kitchen Fujifilm XT3, ISO 1600, 1/500s, F/4, 38mm lens photorealistic hyper real."
#prompt = "A hyper-realistic photograph of a fire incident, captured with a Fujifilm XT3, ISO 1600, 1/500s, F/4, 24mm lens."
#prompt = "A hyper-realistic photograph of vibrant underwater marine life, captured with a Fujifilm XT3, ISO 400, 1/125s, F/2.8, 24mm lens, diver's camera, photorealistic."
#prompt = "A hyper-realistic photograph inside a five star hotel captured with a Fujifilm XT3, ISO 400, 1/125s, F/2.8, 24mm lens, photorealistic."
#prompt = "A realistic photograph of an ordinary public library interior, captured with a Fujifilm XT3, ISO 800, 1/60s, F/2.8, 24mm lens. The library features simple, functional design with rows of standard wooden bookshelves filled with a mix of hardcover and paperback books. The space is well-lit with fluorescent ceiling lights, casting a bright and even light across the room."
#prompt = "A high-resolution photograph of bowling alley with pins captured with a Fujifilm XT3, ISO 800, 1/60s, F/2.8, 24mm lens, photorealistic."
#prompt = "A high-resolution photograph inside the gym captured with a Fujifilm XT3, ISO 800, 1/60s, F/2.8, 24mm lens, photorealistic."
#prompt = "A high-resolution photograph inside the hospital with a Fujifilm XT3, ISO 800, 1/60s, F/2.8, 24mm lens, photorealistic."
prompt = "A high-resolution photograph inside the warehouse with a Fujifilm XT3, ISO 800, 1/60s, F/2.8, 24mm lens, photorealistic."

seed = random.randint(0, sys.maxsize)

num_inference_steps = 2

images = pipe(
    prompt = prompt,
    guidance_scale = 0.0,
    num_inference_steps = num_inference_steps,
    height=1024,
    width=1024,
    generator = torch.Generator("cuda").manual_seed(seed),
    ).images

print(f"Prompt:\t{prompt}\nSeed:\t{seed}")
media.show_images(images)
#images[0].save("castle.jpg")
#images[0].save("city_sunset.jpg")
#images[0].save("rainy_farm.jpg")
#images[0].save("desert.jpg")
#images[0].save("sky_clouds.jpg")
#images[0].save("ocean.jpg")
#images[0].save("galaxy.jpg")
#images[0].save("forest.jpg")
#images[0].save("storm.jpg")
#images[0].save("inside_white_house.jpg")
#images[0].save("office.jpg")
#images[0].save("kitchen.jpg")
#images[0].save("fire.jpg")
#images[0].save("underwater.jpg")
#images[0].save("hotel.jpg")
#images[0].save("library.jpg")
#images[0].save("bowling.jpg")
#images[0].save("gym.jpg")
#images[0].save("hospital.jpg")
images[0].save("warehouse.jpg")



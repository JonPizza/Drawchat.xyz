from PIL import Image
import os

loaded_images = {} # GLOBAL

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'DeepSkyBlue': (0, 191, 255),
    'gray': (128, 128, 128),
    'lime': (0, 255, 0),
    'pink': (255, 192, 203),
    'brown': (165, 42, 42),
}

colors_reverse = {
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
    (255, 0, 0): 'red',
    (0, 128, 0): 'green',
    (0, 0, 255): 'blue',
    (128, 0, 128): 'purple',
    (255, 255, 0): 'yellow',
    (255, 165, 0): 'orange',
    (0, 191, 255): 'DeepSkyBlue',
    (128, 128, 128): 'gray',
    (0, 255, 0): 'lime',
    (255, 192, 203): 'pink',
    (165, 42, 42): 'brown',
}

def create_png(fname, width, height):
    img = Image.new('RGB', (width, height), color = 'white')
    img.save(fname)

def load_png(fname):
    global loaded_images

    if not os.path.isfile(fname):
        create_png(fname, 100, 100)

    if loaded_images.get(fname, None):
        return loaded_images[fname]
    else:
        img = Image.open(fname)
        pixels = img.load()
        loaded_images[fname] = (img, pixels)
        return (img, pixels)

def update_png(fname, x, y, color):
    img, pixels = load_png(fname)
    pixels[x, y] = colors[color]
    img.save(fname)

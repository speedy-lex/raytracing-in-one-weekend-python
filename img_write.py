import numpy as np
import PIL.Image, PIL.ImageOps

def write_ppm(img, path):
    dat=f'P3\n{np.shape(img)[0]} {np.shape(img)[1]}\n255\n'
    for y in range(np.shape(img)[1]):
        for x in range(np.shape(img)[0]):
            dat=f'{dat}{int(img[x][y][0]*255)} {int(img[x][y][1]*255)} {int(img[x][y][2]*255)}\n'
    with open(path, 'w') as f:
        f.write(dat)

def write(img, path):
    PIL.Image.fromarray((img*255).astype(np.uint8)).rotate(90, expand=True).save(path)

def new(size):
    return np.zeros((*size, 3))

def to_np(color):
    return np.asarray((color.x, color.y, color.z))
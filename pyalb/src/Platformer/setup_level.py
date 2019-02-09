#! C:\Users\HeleneLeBerre\envs\setup_level.py\python.exe
# coding = Utf-8

from __future__ import print_function

from glob import glob

import numpy as np
from PIL import Image
from numpy.random import randint

try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk


class Block:

    def __init__(self, name, block_id, is_solid, aimage):
        self.name = name
        self.id = block_id
        self.is_solid = is_solid
        self.aimage = aimage


def load_blocks(path=""):
    """
    path -> Folder of the blocks, default if current directory.

    returns the dictionnary with key=block_id and value=block
    """
    image_paths = glob(path + '!*;*;*!.png')
    blocks = dict()

    for path in image_paths:

        img_name = path.split('!')[-2]
        # img_name syntax : "!(name);solid=(is_solid);id=(id)!.(ext)"
        # for example "!Block test;solid=1;id=4568!.png"
        split_name = img_name.split(';')

        block_name = split_name[0]
        is_solid = int(split_name[1][-1])  # for example if split_name[1] = 'solid=0', is_solid = 0

        if split_name[2].startswith('id='):
            block_id = np.uint16(split_name[2][3:])  # for example if split_name[2] = 'id=65535', block_id = 65535
        else:
            block_id = np.uint16(split_name[2])

        aimage = np.asarray(Image.open(path))
        if aimage.dtype == np.float32:
            aimage = (aimage * 255).astype(np.uint8)
        aimage = aimage[:, :, :4]
        if aimage.shape[2] == 3:
            try:
                a = np.zeros((*aimage.shape[:2], 4)) + 255
            except SyntaxError:
                a = np.zeros(aimage.shape[:2] + [4]) + 255
            a[:, :, :3] = aimage
            aimage = a

        block = Block(block_name, block_id, is_solid, aimage)

        blocks[block_id] = block

    return blocks


def parse_level(level, blocks=None):
    """
    level -> array

    blocks -> dict of the different available blocks, if None blocks are automatically loaded

    returns the full image of the level and the array of the solid blocks
    """
    solid_blocks_array = np.zeros(level.shape, dtype=np.bool)

    if blocks is None:
        blocks = load_blocks()

    shapes = np.empty(3, dtype=np.int16)
    shapes[0:2] = np.asarray(level.shape) * 16
    shapes[2] = 4
    level_image = np.empty(shapes, dtype=np.uint8)

    for y in range(level.shape[0]):
        for x in range(level.shape[1]):

            block = blocks[level[y, x]]
            level_image[y * 16:y * 16 + 16, x * 16:x * 16 + 16, :] = block.aimage
            if block.is_solid:
                solid_blocks_array[y, x] = True

    return level_image, solid_blocks_array


def properly_resize_img(image, screen_heightorwidth, number_of_blocks):
    """Resize the picture in entrance so that a precise number of 16x16 blocks matches exactly with the height or the
    width of the screen in entrance.

    image -> picture to resize, PIL.Image.Image type
    screen_heightorwidth -> the screen height or width, in pixels
    number_of_blocks -> number of 16x16 blocks
    """

    multiplier = screen_heightorwidth / (16 * number_of_blocks)

    size = tuple(int(a * multiplier) for a in image.size)
    return image.resize(size, Image.NEAREST)


def _main():
    level = randint(0, 5, (50, 100), dtype=np.uint16)

    level_image, solid_blocks_array = parse_level(level)

    root = Tk()

    canvas = Canvas(root)
    canvas['highlightthickness'] = 0
    canvas.pack(fill='both', expand=1)

    pilimage = properly_resize_img(Image.fromarray(level_image), root.winfo_screenheight(), 10)

    img = list()
    img.append(ImageTk.PhotoImage(image=pilimage))

    canvas.create_image(0, 0, image=img[0], anchor='nw')

    root.attributes('-fullscreen', True)
    root.mainloop()

    print(1)


if __name__ == "__main__":
    try:
        from tkinter import Canvas
    except ImportError:
        from Tkinter import Canvas
    from PIL import ImageTk

    _main()

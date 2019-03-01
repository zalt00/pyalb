# coding = Utf-8

import sys
from pickle import Unpickler
from PIL import Image
import os
import setup_level

os.chdir(sys.argv[1])

file_path = sys.argv[-1]
with open(file_path, 'rb') as binary_file:
    data = Unpickler(binary_file).load()

array = data['array_map']
blocks = setup_level.load_blocks('Images/Blocks/')
pil_image = Image.fromarray(setup_level.parse_level(array, blocks)[0])
pil_image.show()

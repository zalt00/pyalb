# -*- coding: utf-8 -*-

from PIL import Image
import tkinter as tk
from math import ceil

root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()

a = 1920 / 1080
b = width / height

if a != b :
    if a < b :
        width = height * a
    elif b < a :
        height = width / a

height = ceil(height)
width = ceil(width)

img = Image.open("main_menu_bg.png").resize((width, height))
img.save("main_menu_bg_resized.png", img.format)

print("hey")
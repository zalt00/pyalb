# -*- coding: utf-8 -*-

from PIL import Image
import tkinter as tk

root = tk.Tk()
shapes = root.winfo_screenwidth(), root.winfo_screenheight()

img = Image.open("main_menu_bg.png").resize(shapes)
img.save("main_menu_bg_resized.png", img.format)
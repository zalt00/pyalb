#! C:\Users\HeleneLeBerre\envs\setup_level.py\python.exe
# coding = Utf-8

import tkinter as tk
from PIL import Image, ImageOps

root = tk.Tk()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

img = Image.open('landscape_painting_by_jonathandufresne-d5pwwbq.jpg')


img = ImageOps.fit(img, (sw, sh), Image.ANTIALIAS)

img.save('bg.png')

print(sw, sh)



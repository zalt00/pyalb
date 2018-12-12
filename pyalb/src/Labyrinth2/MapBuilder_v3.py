# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import askopenfilename
import json
from glob import glob
import numpy as np
from time import perf_counter
from Images.init_images import LabObj, PNGS, save_img


class Interface(tk.Frame) :

    def __init__(self, root, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)


        self.pngs = PNGS("Images/PNGS")

        self.canvas = tk.Canvas(self)
        
        with open("control_mapbuilder.json", "r", encoding="utf8") as data :
            self.ctrls = json.load(data)


        file_path = askopenfilename(title="Ouvrir une carte où appuyez sur Annuler", filetypes=[('txt files','.txt'),('all files','.*')])

        if file_path != "" :
            with open(file_path, "r", encoding="utf8") as fch :
                self.map_str = fch.read()

        else :
            self.map_str = str()


        map_list = self.map_str.splitlines()
        
        self.shapes = len(map_list), len(map_list[0])

        self.blocks = dict()
        
        for y in range(self.shapes[1]//10) :
            for x in range(self.shapes[0]//10) :
                
                ya, yb = y*10, 10+y*10
                xa, xb = x*10, 10+x*10


                block = "\n".join([a[xa:xa+10] for a in map_list[ya:yb]])
                self.blocks[(x, y)] = block

            



        




root = tk.Tk()
Interface(root).pack(fill="both")
root.mainloop()
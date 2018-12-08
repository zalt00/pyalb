# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json
from glob import glob


class Interface(tk.Frame) :

    def __init__(self, root, **kwargs) :


        tk.Frame.__init__(self, root, **kwargs)
        self.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.pngs = glob("Images/PNGS/*.png")
        
        self.pngs_short_name = [a.split("\\")[-1] for a in self.pngs]

        with open("control_mapbuilder.json", "r", encoding="utf8") as data_file :
            self.ctrls = json.load(data_file)

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.focus_set()

        self.coords = [8, 8]

        self.img_curs = tk.PhotoImage(file="Images/curseur.png")
        self.curseur = self.canvas.create_image(self.coords[0], self.coords[1], image=self.img_curs)


        self.imgs = dict()



    def key_press(self, evt) : # create an img

        if not evt.keysym in ["Up", "Right", "Left", "Down", "Delete", "Shift_L", 'Caps_Lock'] :
            
            try :
                touche = self.ctrls[evt.keysym]

                for i, img_name in enumerate(self.pngs_short_name) :
                    

                    if touche == img_name[1] :
                        img_path = str(self.pngs[i])


                self.imgs[tuple(self.coords)] = (tk.PhotoImage(file=img_path).zoom(2), touche)
                self.canvas.create_image(self.coords[0], self.coords[1], image=self.imgs[tuple(self.coords)][0])
                self.canvas.tag_raise(self.curseur)

            except KeyError as e :
                print("KeyError - {}".format(e))
        
        else :

            if evt.keysym == "Up" :
                self.coords[1] -= 16

            elif evt.keysym == "Down" :
                self.coords[1] += 16

            elif evt.keysym == "Left" :
                self.coords[0] -= 16

            elif evt.keysym == "Right" :
                self.coords[0] += 16

            elif evt.keysym == 'Delete' :
                self.imgs[tuple(self.coords)] = None

            if self.coords[0] < 0 :
                self.coords[0] = 8
            if self.coords[1] < 0 :
                self.coords[1] = 8

            self.canvas.coords(self.curseur, self.coords[0], self.coords[1])








root = tk.Tk()
window = Interface(root)

window.mainloop()
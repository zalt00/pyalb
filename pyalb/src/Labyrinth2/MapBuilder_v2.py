# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import json
from glob import glob
import numpy as np
from time import perf_counter





class Interface(tk.Frame) :

    def __init__(self, root, **kwargs) :


        tk.Frame.__init__(self, root, **kwargs)


        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.pngs = glob("Images/PNGS/*.png")
        
        self.pngs_short_name = [a.split("\\")[-1] for a in self.pngs]

        with open("control_mapbuilder.json", "r", encoding="utf8") as data_file :
            self.ctrls = json.load(data_file)

        self.car2img = dict() # permet de passer d'un caractère à un path d'img

        for key in self.ctrls.values() :

            continuer = True
            i = 0
            while continuer:
                
                if key == self.pngs_short_name[i][1] :
                    self.car2img[key] = str(self.pngs[i])
                    continuer = False
                else :
                    i += 1

        

        self.coords = [8, 8]

        self.img_curs = tk.PhotoImage(file="Images/curseur.png")
        self.curseur = self.canvas.create_image(self.coords[0], self.coords[1], image=self.img_curs)

        self.toplevel = None

        self.imgs = dict()
        tab_str = str()

        filename = askopenfilename(title="Ouvrir une carte où appuyez sur Annuler",filetypes=[('txt files','.txt'),('all files','.*')])

        try :
            t1 = perf_counter()
            with open(filename, "r", encoding="utf8") as data :
                tab_str = data.read()

            x, y = 0, 0

            for lettre in tab_str :
                
                if lettre == "\n" :
                    y += 1
                    x = 0

                else :

                    img_path = self.car2img[lettre]


                    pos = x*16+8, y*16+8

                    self.imgs[pos] = (tk.PhotoImage(file=img_path).zoom(2), lettre)
                    self.canvas.create_image(pos[0], pos[1], image=self.imgs[pos][0])

                    x += 1

            self.canvas.tag_raise(self.curseur)
            

        except FileNotFoundError :
            pass
        print(perf_counter()-t1)

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.focus_set()

        self.pos = tk.StringVar()



    def key_press(self, evt) : # create an img

        if not evt.keysym in ["Up", "Right", "Left", "Down", "Delete", "Shift_L", 'Caps_Lock', 'Escape'] :
            
            try :
                touche = self.ctrls[evt.keysym]

                img_path = self.car2img[touche]


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
                try :
                    del(self.imgs[tuple(self.coords)])
                except KeyError :
                    pass
            elif evt.keysym == "Escape" :
                self.show_tlvl()

            if self.coords[0] < 0 :
                self.coords[0] = 8
            if self.coords[1] < 0 :
                self.coords[1] = 8

            self.canvas.coords(self.curseur, self.coords[0], self.coords[1])
            self.pos.set("current pos : {}".format(self.coords))


    def show_tlvl(self) :
        


        self.toplevel = tk.Toplevel(self)

        self.label_ctrl = tk.Label(self.toplevel, text="ctrls : \n{}".format("\n".join(["{} : {}".format(a, b) for a, b in self.ctrls.items()])))
        # ce charabia illisible affiche juste les controles

        self.label_ctrl.pack(side="right")

        self.button_save = tk.Button(self.toplevel, text="Save map", command=self.save_map)
        self.button_save.pack()

        self.label_pos = tk.Label(self.toplevel, textvariable=self.pos)
        self.label_pos.pack()


    def save_map(self) :
        

        val_min = min(self.imgs.keys(), key=lambda a : a[0])[0], min(self.imgs.keys(), key=lambda a : a[1])[1]
        val_max = max(self.imgs.keys(), key=lambda a : a[0])[0], max(self.imgs.keys(), key=lambda a : a[1])[1]

        val_min = tuple([(a-8)//16 for a in val_min])
        val_max = tuple([(a-8)//16+1 for a in val_max])


        shapes = (val_max[1] - val_min[1], val_max[0] - val_min[0])

        print(shapes)
        tab = np.zeros(shapes, dtype=np.str)

        for y in range(val_min[1], val_max[1]) :

            for x in range(val_min[0], val_max[0]) :
                pos = y-val_min[1], x-val_min[0], 
                tab[pos] = self.imgs[(x*16+8, y*16+8)][1]

        tab_lt = tab.tolist()
        tab_str = "\n".join(["".join(a) for a in tab_lt]) + "\n"

        with open("map.txt", "w", encoding="utf8") as data :
            data.write(tab_str)
        


        


        








root = tk.Tk()
window = Interface(root)
window.pack(fill="both", expand=True)

root.mainloop()
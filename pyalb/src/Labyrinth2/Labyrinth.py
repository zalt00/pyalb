# -*- coding: utf-8 -*-


import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from Images.init_images import LabObj, PNGS, Save_img
from time import perf_counter



###### [1] CREATION DU BACKGROUND ######

with open("./carte.txt", "r", encoding="utf8") as fichier:
    carte = fichier.read()


l = 0
list_globale = [[]]
list_globale_tab = []
list_ligne_tab = list()



pngs = PNGS("Images/PNGS")

for caract in carte :
    
    if caract == "\n" :
        

        
        list_globale_tab.append(np.concatenate(list_ligne_tab, axis=1))
        list_globale.append([])
        list_ligne_tab = []
        l += 1
        
    else :
        
        for tile in pngs :
            
            if caract == tile.app:
                list_globale[l].append(tile)
                list_ligne_tab.append(tile.code)
        


tab = np.concatenate(list_globale_tab, axis=0)

###### FIN[1], BG -> tab ; BG(donnes) -> list_globale######



Save_img(tab)


height_tab = tab.shape[0]
width_tab = tab.shape[1]


class PlayInterface (tk.Frame) :


    def __init__(self, fenetre, **kwargs) :

        global height_tab
        global width_tab

        tk.Frame.__init__(self, fenetre, width=width_tab*2, height=height_tab*2, **kwargs)

        self.pack(fill=tk.BOTH)



        self.canvas = tk.Canvas(fenetre, width=width_tab, height=height_tab)

        bg = tk.PhotoImage(file="bg.png")

        self.canvas.create_image(50, 50, image=bg)
        self.canvas.pack()



fenetre = tk.Tk()
interface = PlayInterface(fenetre)

interface.mainloop()
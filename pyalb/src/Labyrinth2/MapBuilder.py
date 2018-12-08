# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json
from glob import glob

class InterfaceMapBuilder(tk.Frame) :



    def __init__(self, root, **kwargs) :

        tk.Frame.__init__(self, root, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)

        self.nb = 0


        self.p = tk.PanedWindow(self, orient="horizontal")

        self.txt = tk.Text(self.p, font=("Consolas", -7), padx=5, pady=5)
        self.p.add(self.txt)


        self.frame = tk.Frame(self.p, relief="sunken", padx=5, pady=5, background="white")

        self.but_refresh = ttk.Button(self.frame, text="Refresh", command=self.refresh_label)
        self.but_refresh.grid(row=0, column=0)

        self.but_fcs = ttk.Button(self.frame, text="Activate focus", command=lambda : self.but_fcs.focus_set())
        self.but_fcs.grid(row=0, column=1)


        self.but_fcs.focus_set()

        self.but_fcs.bind("a", self.touche)
        self.bind_all("<Escape>", self.resize_txt)
        self.lt = list()
        self.img_names = list()


        self.txt2label2 = tk.StringVar()
        self.txt2label2.set("0")
        self.label2 = tk.Label(self.frame, textvariable=self.txt2label2, foreground="black", background="white")
        self.label2.grid(row=2, column=0)

        self.spinbox = ttk.Spinbox(self.frame, from_=0, to=200)
        self.spinbox.grid(row=1, column=1)


        self.txt2label = tk.StringVar()
        self.txt2label.set("")
        self.label = tk.Label(self.frame, textvariable=self.txt2label, foreground="black", background="white")
        self.label.grid(row=1, column=3)



        self.p.add(self.frame)
        self.p.pack(expand=tk.Y, fill=tk.BOTH, side="top")


        with open("control_mapbuilder.json", "r") as data_file :
            
            self.ctrls = json.load(data_file)

        self.imgs = glob("Images/PNGS/*.png")
        
    
        

        


        self.isresized = False




    def touche(self, evt) :
        
        a = ""

        for img_path in self.imgs :
            img_name = img_path.split("/")[-1]
            if img_name[1] == self.ctrls[evt.keysym.lower()] :
                a = img_path

        self.lt.append(tk.PhotoImage(file=a))
        self.txt.image_create("insert", image=self.lt[-1], name="nthS_")
        self.txt2label2.set(len(self.txt.image_names())) # todo



    def refresh_label(self):
        
        list2str = list()

        self.nb = int(self.spinbox.get())

        a = 0

        for name in self.txt.image_names() :
            a += 1

            if a > self.nb :
                list2str.append("\n")
                a = 1


            if name[:3] == "nth" :
                list2str.append(name[3])


        a = "".join(list2str)
        print(a)
        self.txt2label.set(a)

    def resize_txt(self, evt):

        if self.isresized :
            self.txt["width"] = 188
            self.isresized = False
        
        else :
            self.txt["width"] = 2
            self.isresized = True

        
root = tk.Tk()

interface = InterfaceMapBuilder(root)
interface.mainloop()
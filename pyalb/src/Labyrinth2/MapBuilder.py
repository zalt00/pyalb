# -*- coding: utf-8 -*-

import tkinter as tk

zoom = input("Saisir zoom : ")

class InterfaceMapBuilder(tk.Frame) :



    def __init__(self, root, zoom=1, **kwargs) :

        tk.Frame.__init__(self, root, **kwargs)
        self.pack(fill=tk.BOTH)

        self.z = zoom


        self.txt = tk.Text(root, width=188*self.z, height=49*self.z, font=("Consolas", -8*self.z), padx=5, pady=5)
        self.txt.pack(side="left")



        
        
        

        self.frame = tk.Frame(root)

        self.but_refresh = tk.Button(self.frame, text="Refresh", command=self.refresh_label)
        self.but_refresh.pack()

        self.but_fcs = tk.Button(self.frame, text="Activate focus", command=lambda : self.but_fcs.focus_set())
        self.but_fcs.pack()


        self.but_fcs.focus_set()

        self.but_fcs.bind("a", self.touche)
        self.bind_all("<Escape>", self.resize_txt)
        self.lt = list()
        self.img_names = list()


        self.txt2label = tk.StringVar()
        self.txt2label.set("")
        self.label = tk.Label(self.frame, textvariable=self.txt2label, background="white")
        self.label.pack(side="right")

        self.frame.pack(side="right", fill="both")

        


        self.isresized = False




    def touche(self, event) :
        
        self.lt.append(tk.PhotoImage(file="Images/PNGS/_ _nth.png").zoom(self.z))
        self.txt.image_create("insert", image=self.lt[-1], name="nthS_")


    def refresh_label(self):
        
        list2str = list()

        a = 0

        for name in self.txt.image_names() :
            a += 1

            if a > 94 :
                list2str.append("\n")
                a = 1


            if name[:3] == "nth" :
                list2str.append(name[3])


        a = "".join(list2str)
        print(a)
        self.txt2label.set(a)

    def resize_txt(self, evt):

        if self.isresized :
            self.txt["width"] = 188*self.z
            self.isresized = False
        
        else :
            self.txt["width"] = 2
            self.isresized = True

        
root = tk.Tk()

interface = InterfaceMapBuilder(root, zoom=int(zoom))
interface.mainloop()
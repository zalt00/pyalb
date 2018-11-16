# -*- coding: utf-8 -*-


import numpy as np
import tkinter as tk
from Images.init_images import LabObj, PNGS, save_img
from glob import glob

###### [1] CREATION DU BACKGROUND ######


def create_bg(choosen_map) :


    with open("./Cartes/{}".format(choosen_map), "r", encoding="utf8") as fichier:
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


    save_img(tab)


    height_tab = tab.shape[0]
    width_tab = tab.shape[1]
    return width_tab, height_tab, list_globale



####### FIN DEF CREAT_BG #######






class PlayInterface(tk.Frame) :

    def __init__(self, root, **kwargs) :

        tk.Frame.__init__(self, root, width=0, height=0, **kwargs)
        self.pack(fill=tk.BOTH)
        
        self.fenetre = tk.Frame(fenetre, borderwidth=2, relief=tk.FLAT)
        self.fenetre.pack()

        self.ZOOM = 2

        self.play_canvas = tk.Canvas(self.fenetre, width=0, height=0, background="#bbbbbb")
        
        self.coords = [4,2]

        self.menu_map_dis = [a[7:] for a in glob("Cartes/*")]
        self.menu_label = tk.Label(self.fenetre, text="S\u00E9lectionnez une carte parmi celles-ci :")


        self.menu_button = tk.Button(self.fenetre, text="Valider", command=self.get_map)


        self.menu_liste = tk.Listbox(self.fenetre, selectmode=tk.SINGLE, height=len(self.menu_map_dis)+1, width=35)
        i = 1
        for carte in self.menu_map_dis :
            self.menu_liste.insert(i, carte)
            i += 1

        self.r = True
        self.rls = True
        self.tomove = 8
        self.mve_para = None
        self.touche_save = None

        self.pack_menu()



    def pack_menu(self) :

        self.play_canvas.pack_forget()

        self.menu_label.pack()
        self.menu_liste.pack()
        self.menu_button.pack(side=tk.RIGHT)



    def pack_play(self) :

        global fenetre
        
        fenetre.attributes('-fullscreen',True)

        self.menu_label.pack_forget()
        self.menu_button.pack_forget()
        self.menu_liste.pack_forget()

        global create_bg
        width_tab, height_tab, self.list_globale = create_bg(self.carte)

        self.fenetre["borderwidth"] = 16
        self.fenetre["background"] = "#bbbbbb"

        self.play_canvas["width"] = width_tab*self.ZOOM
        self.play_canvas["height"] = height_tab*self.ZOOM

        self.bg = tk.PhotoImage(file="Images/bg.png").zoom(self.ZOOM, self.ZOOM)
        self.play_canvas.create_image(0, 0, image=self.bg, anchor=tk.NW)

        self.pers_img = tk.PhotoImage(file="Images/pers.png").zoom(self.ZOOM, self.ZOOM)
        self.pers = self.play_canvas.create_image(self.psimg(4), self.psimg(2), image=self.pers_img)

        self.play_canvas.focus_set()
        self.play_canvas.bind("<KeyPress>", self.clavier_press)
        self.play_canvas.bind("<KeyRelease>", self.clavier_release)
        self.play_canvas.pack()



    def get_map (self) :
        if self.menu_liste.curselection() != () :
            self.carte = self.menu_liste.get(self.menu_liste.curselection()[0])
            self.pack_play()


    def psimg (self, pos) :
        return (4+8*pos)*self.ZOOM

    
    def clavier_press (self, event) :
        if event.keysym == "Escape" : self.quit()

        if self.r :
            self.r = False
            self.touche_save = None
            self.tomove = 8
            touche = event.keysym.lower()
            self.touche_save = None

            
            self.rls = False
           
            
            if touche == "z" :
                            
                self.move(y=-1)
                        
            elif touche == "s" :

                self.move(y=1)

            elif touche == "d" :
                            
                self.move(x=1)
                        
            elif touche == "q" :
                            
                self.move(x=-1)

            else :
                
                self.r = True
        
        else :
            
            self.touche_save = event
                        
                
                
        

    def move(self, x=0, y=0) :

        if self.mve_para is not None :
            x, y = self.mve_para

        a = 9-self.tomove
        mur = False

        if x < 0 :
            if self.list_globale[self.coords[1]][self.coords[0]-1].tag != "mur" :
                self.play_canvas.coords(self.pers, self.psimg(self.coords[0])-a, self.psimg(self.coords[1]))
            else :
                mur = True
        elif x > 0 :
            if self.list_globale[self.coords[1]][self.coords[0]+1].tag != "mur" :
                self.play_canvas.coords(self.pers, self.psimg(self.coords[0])+a, self.psimg(self.coords[1]))
            else :
                mur = True
        elif y < 0 :
            if self.list_globale[self.coords[1]-1][self.coords[0]].tag != "mur" :
                self.play_canvas.coords(self.pers, self.psimg(self.coords[0]), self.psimg(self.coords[1])-a)
            else :
                mur = True
        elif y > 0 :
            if self.list_globale[self.coords[1]+1][self.coords[0]].tag != "mur" :
                self.play_canvas.coords(self.pers, self.psimg(self.coords[0]), self.psimg(self.coords[1])+a)
            else :
                mur = True
        if not mur :
            self.tomove -= 1

            if self.tomove > -9:
                self.mve_para = (x, y)
                self.after(10, self.move)
            else :

                if x < 0 : 
                    self.coords[0] -= 1
                    tch = "q"
                elif x > 0 :
                    self.coords[0] += 1
                    tch = "d"
                elif y < 0 :
                    self.coords[1] -= 1
                    tch = "z"
                elif y > 0 :
                    self.coords[1] += 1
                    tch = "s"

                self.play_canvas.coords(self.pers, self.psimg(self.coords[0]), self.psimg(self.coords[1]))

                if self.rls :
                    self.mve_para = None
                    self.r = True
                    if self.touche_save is not None :
                        if self.touche_save.keysym.lower() != tch :
                            self.clavier_press(self.touche_save)
                else :
                    self.tomove = 6
                    self.after(8, self.move)
        else :
            self.r = True
            self.mve_para = None
            


    def clavier_release(self, event):
        
        self.rls = True

        if self.touche_save is not None :
            if event.keysym.lower() == self.touche_save.keysym.lower() :
                self.touche_save = None
        


        


        






fenetre = tk.Tk()
fenetre.title("Labyrinth")
interface = PlayInterface(fenetre)



interface.mainloop()
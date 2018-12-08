# -*- coding: utf-8 -*-


import numpy as np
import tkinter as tk
from Images.init_images import LabObj, PNGS, save_img
from glob import glob
from time import perf_counter

###### [1] CREATION DU BACKGROUND ######

t1 = perf_counter()
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
        
        self.fenetre = tk.Frame(self, borderwidth=2, relief=tk.FLAT)
        self.fenetre.pack()

        self.ZOOM = 2

        self.play_canvas = tk.Canvas(self.fenetre, width=0, height=0, background="#bbbbbb")
        
        self.coords = [self.psimg(4),self.psimg(2)]
        self.rlcoords = [4,2]

        self.menu_map_dis = [a[7:] for a in glob("Cartes/*")]
        self.menu_label = tk.Label(self.fenetre, text="S\u00E9lectionnez une carte parmi celles-ci :")


        self.menu_button = tk.Button(self.fenetre, text="Valider", command=self.get_map)


        self.menu_liste = tk.Listbox(self.fenetre, selectmode=tk.SINGLE, height=len(self.menu_map_dis)+1, width=35)
        i = 1
        for carte in self.menu_map_dis :
            self.menu_liste.insert(i, carte)
            i += 1

        self.r = True # evite la pression multiple des touches pour le déplacement du personnage
        self.r_bg = True # evite la pression multiple des touches pour le déplacement de la caméra
        self.rls = True # passe en True quand KeyRelease
        self.touche_save = None

        self.touche = None

        self.bg2move = 8
        self.dirsave = None


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

        self.pos_bgrl = [width_tab*self.ZOOM//2, height_tab*self.ZOOM//2]



        self.bg_img = tk.PhotoImage(file="Images/bg.png").zoom(self.ZOOM, self.ZOOM)
        self.bg = self.play_canvas.create_image(self.pos_bgrl[0], self.pos_bgrl[1], image=self.bg_img)

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

    def bgimg(self, pos) :
        return (8*pos)*self.ZOOM





    def clavier_press (self, event) :
        touche = event.keysym
        if touche == "Escape" : self.quit()

        




        if self.r and touche.lower() in "zqsd" :
            self._pers_evt(touche)

        elif self.r_bg and touche.lower() in "oklm" :
            self._bg_evt(touche)      

        else :
            self.touche_save = event


    def _bg_evt (self, touche) :
        self.r_bg = False
        self.touche_save = None
        self.touche = touche.lower()
        self.rls = False


        if self.touche == "l" :
            self.move_bg(0, -1)
            
        elif self.touche == "o" :
            self.move_bg(0, 1)

        elif self.touche == "k" :
            self.move_bg(1, 0)

        elif self.touche == "m" :
            self.move_bg(-1, 0)

        else :
            self.r_bg = True            
            

    def _pers_evt (self, touche) :
        self.r = False
        self.touche_save = None
        self.touche = touche.lower()

            
        self.rls = False
           
            
        if self.touche == "z" :           
            self.move_pers(0, -1)
                        
        elif self.touche == "s" :
            self.move_pers(0, 1)

        elif self.touche == "d" :         
            self.move_pers(1, 0)
                        
        elif self.touche == "q" :         
            self.move_pers(-1, 0)

        else :
            self.r = True





    def move_pers(self, x, y) :
        
        mur = False

        posorneg = x, y # positive or negative

        if x > 0 :
            if self.list_globale[self.rlcoords[1]][self.rlcoords[0]+1].tag != "mur" :

                n_2move = [2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True
        
        if x < 0 :
            if self.list_globale[self.rlcoords[1]][self.rlcoords[0]-1].tag != "mur" :

                n_2move = [-2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True

        if y > 0 :
            if self.list_globale[self.rlcoords[1]+1][self.rlcoords[0]].tag != "mur" :

                n_2move = [0, 2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True

        if y < 0 :
            if self.list_globale[self.rlcoords[1]-1][self.rlcoords[0]].tag != "mur" :

                n_2move = [0, -2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True



        if not mur :
           
            self._movepers(n_2move, posorneg, xory, 8)

        else :
            self.r = True


    def _todo_after_movepers(self, posorneg, xory) :
        

        self.coords[xory] += posorneg[xory] * 8 * self.ZOOM
        self.rlcoords[xory] += posorneg[xory]

        if not self.rls :
            self.after(16, self.move_pers, posorneg[0], posorneg[1])
        else :
            self.r = True
            if self.touche_save is not None :
                if self.touche_save.keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save)


    def _movepers(self, n_2move, posorneg, xory, nb) :

        self.play_canvas.coords(self.pers, self.coords[0]+n_2move[0], self.coords[1]+n_2move[1])

        n_2move[xory] += posorneg[xory] * self.ZOOM
        nb -= 1
        if nb != 0 :
            self.after(16, self._movepers, n_2move, posorneg, xory, nb)
        else :
            self.after(8, self._todo_after_movepers, posorneg, xory)






        
    def move_bg(self, x, y) :
        
        posorneg = x, y
        
        if y != 0 :
            xory = 1
        elif x != 0 :
            xory = 0



        self._movebg(posorneg, xory)


    def _movebg(self, posorneg, xory) :
            
        self.coords[xory] += posorneg[xory] * self.ZOOM *4
        self.play_canvas.coords(self.pers, self.coords[0], self.coords[1])

        self.pos_bgrl[xory] += posorneg[xory] * self.ZOOM *4
        self.play_canvas.coords(self.bg, self.pos_bgrl[0], self.pos_bgrl[1])

        if not self.rls :
            self.after(16, self._movebg, posorneg, xory)
        else :
            self.r_bg = True
            if self.touche_save is not None :
                if self.touche_save.keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save)






    def clavier_release(self, event):
        
        self.rls = True

        if self.touche_save is not None :
            if event.keysym.lower() == self.touche_save.keysym.lower() :
                self.touche_save = None
        


        


        






fenetre = tk.Tk()
fenetre.title("Labyrinth")
interface = PlayInterface(fenetre)

print(perf_counter()-t1)

interface.mainloop()
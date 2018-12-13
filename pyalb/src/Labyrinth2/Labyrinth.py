# -*- coding: utf-8 -*-

from time import perf_counter
t1 = perf_counter()

import numpy as np
import tkinter as tk

from Images.init_images import LabObj, PNGS, save_img
from glob import glob


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


class Root(tk.Tk) :

    def __init__(self) :

        super().__init__()


        self.in_game = InGameInterface(self)
        self.main_menu = MainMenuInterface(self)

        self.com = dict()

    def change_page(self, actual, new) :
        
        getattr(self, actual).pack_forget()
        getattr(self, new).pack(fill="both")
        






class MainMenuInterface(tk.Frame) :

    def __init__(self, root, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)


        self.root = root

        self.menu_map_dis = [a[7:] for a in glob("Cartes/*")]
        self.menu_label = tk.Label(self, text="S\u00E9lectionnez une carte parmi celles-ci :")


        self.menu_button = tk.Button(self, text="Valider", command=self.get_map)


        self.menu_liste = tk.Listbox(self, selectmode=tk.SINGLE, height=len(self.menu_map_dis)+1, width=35)
        i = 1
        for carte in self.menu_map_dis :
            self.menu_liste.insert(i, carte)
            i += 1

        self.menu_label.pack()
        self.menu_liste.pack()
        self.menu_button.pack(side=tk.RIGHT)



    def get_map (self) :

        if self.menu_liste.curselection() != () :
            self.root.com["carte"] = self.menu_liste.get(self.menu_liste.curselection()[0])
            self.root.change_page("main_menu", "in_game")

            self.root.in_game.play()





class InGameInterface(tk.Frame) :

    def __init__(self, root, **kwargs) :


        self.root = root

        tk.Frame.__init__(self, root, width=0, height=0, **kwargs)
        
        self.fenetre = tk.Frame(self, borderwidth=0, background="#bbb")
        self.fenetre.pack()

        self.ZOOM = 2

        self.play_canvas = tk.Canvas(self.fenetre, width=0, height=0, background="#bbb", highlightthickness=0)
        
        self.coords = [self.psimg(4),self.psimg(2)]
        self.rlcoords = [4,2]




        self.r = {"pers" : True, "cam" : True}
        self.rls = {"pers" : True, "cam" : True} # passe en True quand KeyRelease
        self.touche_save = {"pers" : None, "cam" : None}
        self.touche = {"pers" : None, "cam" : None}

        self.bg2move = 8
        self.dirsave = None

        
        self.play_canvas.focus_set()
        self.play_canvas.bind("<KeyPress>", self.clavier_press)
        self.play_canvas.bind("<KeyRelease>", self.clavier_release)
        self.play_canvas.pack()


    def play(self) :

        
        self.root.attributes('-fullscreen', True)

        global create_bg
        width_tab, height_tab, self.list_globale = create_bg(self.root.com["carte"])

        self.play_canvas["width"] = width_tab*self.ZOOM
        self.play_canvas["height"] = height_tab*self.ZOOM

        self.pos_bgrl = [width_tab*self.ZOOM//2, height_tab*self.ZOOM//2]



        self.bg_img = tk.PhotoImage(file="Images/bg.png").zoom(self.ZOOM, self.ZOOM)
        self.bg = self.play_canvas.create_image(self.pos_bgrl[0], self.pos_bgrl[1], image=self.bg_img)

        self.pers_img = tk.PhotoImage(file="Images/pers.png").zoom(self.ZOOM, self.ZOOM)
        self.pers = self.play_canvas.create_image(self.psimg(4), self.psimg(2), image=self.pers_img)

        






    def psimg (self, pos) :
        return (4+8*pos)*self.ZOOM

    def bgimg(self, pos) :
        return (8*pos)*self.ZOOM





    def clavier_press (self, event) :
        touche = event.keysym
        if touche == "Escape" : self.quit()


        if touche.lower() in "zqsd" :

            if self.r["pers"] :
                self._pers_evt(touche)
            else :
                self.touche_save["pers"] = event


        if touche.lower() in "oklm" :

            if self.r["cam"] :
                self._bg_evt(touche)      
            else :
                self.touche_save["cam"] = event


    def _bg_evt (self, touche) :
        self.r["cam"] = False
        self.touche_save["cam"] = None
        self.touche["cam"] = touche.lower()
        self.rls["cam"] = False


        if self.touche["cam"] == "l" :
            self.move_bg(0, -1)
            
        elif self.touche["cam"] == "o" :
            self.move_bg(0, 1)

        elif self.touche["cam"] == "k" :
            self.move_bg(1, 0)

        elif self.touche["cam"] == "m" :
            self.move_bg(-1, 0)

        else :
            self.r["cam"] = True            
            

    def _pers_evt (self, touche) :
        self.r["pers"] = False
        self.touche_save["pers"] = None
        self.touche["pers"] = touche.lower()

            
        self.rls["pers"] = False
           
            
        if self.touche["pers"] == "z" :           
            self.move_pers(0, -1)
                        
        elif self.touche["pers"] == "s" :
            self.move_pers(0, 1)

        elif self.touche["pers"] == "d" :         
            self.move_pers(1, 0)
                        
        elif self.touche["pers"] == "q" :         
            self.move_pers(-1, 0)

        else :
            self.r["pers"] = True





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
            self.r["pers"] = True


    def _todo_after_movepers(self, posorneg, xory) :
        

        self.coords[xory] += posorneg[xory] * 8 * self.ZOOM
        self.rlcoords[xory] += posorneg[xory]

        if not self.rls["pers"] :
            self.after(6, self.move_pers, posorneg[0], posorneg[1])
        else :
            self.r["pers"] = True
            if self.touche_save["pers"] is not None :
                if self.touche_save["pers"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["pers"])


    def _movepers(self, n_2move, posorneg, xory, nb) :

        self.play_canvas.coords(self.pers, self.coords[0]+n_2move[0], self.coords[1]+n_2move[1])

        n_2move[xory] += posorneg[xory] * self.ZOOM
        nb -= 1
        if nb != 0 :
            self.after(12, self._movepers, n_2move, posorneg, xory, nb)
        else :
            self.after(6, self._todo_after_movepers, posorneg, xory)






        
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

        if not self.rls["cam"] :
            self.after(16, self._movebg, posorneg, xory)
        else :
            self.r["cam"] = True
            if self.touche_save["cam"] is not None :
                if self.touche_save["cam"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["cam"])






    def clavier_release(self, event):
        
        if event.keysym.lower() in "zqsd" :
            self.rls["pers"] = True

            if self.touche_save["pers"] is not None :
                if event.keysym.lower() == self.touche_save["pers"].keysym.lower() :
                    self.touche_save["pers"] = None
        
        elif event.keysym.lower() in "olmk" :
            self.rls["cam"] = True

            if self.touche_save["cam"] is not None :
                if event.keysym.lower() == self.touche_save["cam"].keysym.lower() :
                    self.touche_save["cam"] = None


        


        





root = Root()
root.title("Labyrinth")

root.main_menu.pack()


print(perf_counter()-t1)

root.mainloop()
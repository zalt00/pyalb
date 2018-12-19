# -*- coding: utf-8 -*-

from time import perf_counter
t1 = perf_counter()

import numpy as np
import tkinter as tk
from Images.init_images import LabObj, PNGS, save_img, create_bg
from glob import glob
import os
import logging as lg
from logging.handlers import RotatingFileHandler
from json import load as jsload


CWD = r"C:\Users\Hélène Le Berre\Documents\Programation\pyalb\pyalb\src\Labyrinth2"
os.chdir(CWD)


temps = set() # fichiers temporaires



logger = lg.getLogger()
logger.setLevel(lg.DEBUG)

formatter = lg.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = RotatingFileHandler('labyrinth.log', 'a', 1000000, 1)

file_handler.setLevel(lg.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)





class Root(tk.Tk) :

    def __init__(self) :

        super().__init__()


        self.in_game = InGameInterface(self)
        self.main_menu = MainMenuInterface(self)

        self.com = dict()


    def change_page(self, actual, new) :
        
        getattr(self, actual).pack_forget()
        getattr(self, new).pack(fill="both", expand=True)
        






class MainMenuInterface(tk.Frame) :

    def __init__(self, root, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)


        self.root = root
        


        self.menu_map_dis = dict()

        for a in glob("Cartes/*.json") :
            
            b = a[7:-5]
            self.menu_map_dis[b] = a
        

        self.menu_label = tk.Label(self, text="S\u00E9lectionnez une carte parmi celles-ci :")


        self.menu_button = tk.Button(self, text="Valider", command=self.get_map)


        self.menu_liste = tk.Listbox(self, selectmode=tk.SINGLE, height=len(self.menu_map_dis)+1, width=35)
        i = 1
        for carte in self.menu_map_dis.keys() :
            self.menu_liste.insert(i, carte)
            i += 1

        self.menu_label.pack()
        self.menu_liste.pack()
        self.menu_button.pack(side=tk.RIGHT)



    def get_map (self) :

        if self.menu_liste.curselection() != () :

            a = self.menu_liste.get(self.menu_liste.curselection()[0])
            json_path = self.menu_map_dis[a]


            with open(json_path, "r", encoding="utf8") as data :
                data_dict = jsload(data) # jsload -> json.load

            self.root.com["data"] = data_dict
            self.root.change_page("main_menu", "in_game")

            logger.info('Game started with the map called "{}".'.format(json_path))

            self.root.in_game.play()





class InGameInterface(tk.Frame) :

    def __init__(self, root, **kwargs) :


        self.root = root

        tk.Frame.__init__(self, root, width=0, height=0, **kwargs)
        
        self.fenetre = tk.Frame(self, borderwidth=0, background="#bbb")
        self.fenetre.pack(expand=True, fill="both")

        self.ZOOM = 2

        self.play_canvas = tk.Canvas(self.fenetre, height=self["height"], background="#bbb", highlightthickness=0)
        
        self.coords = [0, 0]
        self.rlcoords = [0, 0]

        self.pos_bgrl = [0, 0]


        self.r = {"pers" : True, "cam" : True} # permet d'eviter l'appuyage prolongé de windows sur une touche
        self.rls = {"pers" : True, "cam" : True} # passe en True quand KeyRelease
        self.touche_save = {"pers" : None, "cam" : None} # permet de faire des virages fluides, sans pause
        self.touche = {"pers" : None, "cam" : None}

        
        self.play_canvas.focus_set()
        self.play_canvas.bind("<KeyPress>", self.clavier_press)
        self.play_canvas.bind("<KeyRelease>", self.clavier_release)
        self.play_canvas.pack(expand=True, fill="both")



    def play(self) :

        
        self.root.attributes('-fullscreen', True)

        carte = self.root.com["data"]["map_path"]

        self.rlcoords[0] = self.root.com["data"]["pers_x"]
        self.rlcoords[1] = self.root.com["data"]["pers_y"]

        self.coords[0] = self.psimg(self.root.com["data"]["pers_x"])
        self.coords[1] = self.psimg(self.root.com["data"]["pers_y"])


        global create_bg
        width_tab, height_tab, self.list_globale = create_bg(carte, "Images/bg.png", temps)

        self.pos_bgrl[0] = width_tab*self.ZOOM//2
        self.pos_bgrl[1] = height_tab*self.ZOOM//2


        self.bg_img = tk.PhotoImage(file="Images/bg.png").zoom(self.ZOOM, self.ZOOM)
        self.bg = self.play_canvas.create_image(self.pos_bgrl[0], self.pos_bgrl[1], image=self.bg_img)


        self.doors = dict() # pour raccourcir
        self.dr = dict() # dictionnaire des positions des portes
        self.act = dict()


        for name, door in self.root.com["data"]["doors"].items() :
            
            self.doors[name] = door

            self.doors[name]["door"]["img"] = tk.PhotoImage(file=self.doors[name]["door"]["app"]).zoom(self.ZOOM)
            x, y = self.doors[name]["door"]["pos_x"], self.doors[name]["door"]["pos_y"]

            self.doors[name]["door"]["img_pos"] = [self.psimg(x), self.psimg(y)]
            # ^ position sur l'image, evite une desyncro avec le mouvement de la cam
            self.doors[name]["door"]["obj"] = (
                self.play_canvas.create_image(self.psimg(x), self.psimg(y), image=self.doors[name]["door"]["img"])
            )
            self.dr[x, y] = name
            self.act[x, y] = lambda self, pos : self._door_isactivate(self.dr[pos])


            self.doors[name]["button"]["img"] = tk.PhotoImage(file=self.doors[name]["button"]["app"]).zoom(self.ZOOM)
            x, y = self.doors[name]["button"]["pos_x"], self.doors[name]["button"]["pos_y"]

            self.doors[name]["button"]["img_pos"] = [self.psimg(x), self.psimg(y)]
            self.doors[name]["button"]["obj"] =(
                self.play_canvas.create_image(self.psimg(x), self.psimg(y), image=self.doors[name]["button"]["img"])
            )

            self.dr[x, y] = name
            self.act[x, y] = lambda self, pos : self._but_activate(self.dr[pos])

            


        self.pers_img = tk.PhotoImage(file="Images/pers.png").zoom(self.ZOOM, self.ZOOM)
        self.pers = self.play_canvas.create_image(self.coords[0], self.coords[1], image=self.pers_img)



    def _but_activate(self, door_pair_name) :

        if self.doors[door_pair_name].get("button_activate/disactivate", False) :

            if self.doors[door_pair_name]["activated"] :
                self.doors[door_pair_name]["activated"] = 0
            else :
                self.doors[door_pair_name]["activated"] = 1


        else :
            self.doors[door_pair_name]["activated"] = 1 # activate -> 0:porte fermee, 1:porte ouverte
        return True

    def _door_isactivate(self, door_pair_name) :

        if self.doors[door_pair_name]["activated"] :
            return True
        
        else :
            return False



    def psimg (self, pos) :
        return (4+8*pos)*self.ZOOM



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
            xb, yb = self.rlcoords[0]+1, self.rlcoords[1]
            if self.list_globale[yb][xb].tag != "mur" and (
                self.act.get((xb, yb), lambda *args : True)(self, (xb, yb))
            ):

                n_2move = [2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True
        
        elif x < 0 :
            xb, yb = self.rlcoords[0]-1, self.rlcoords[1]
            if self.list_globale[yb][xb].tag != "mur" and (
                self.act.get((xb, yb), lambda *args : True)(self, (xb, yb))
            ):

                n_2move = [-2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y > 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]+1
            if self.list_globale[yb][xb].tag != "mur" and (
                self.act.get((xb, yb), lambda *args : True)(self, (xb, yb))
            ):

                n_2move = [0, 2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y < 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]-1
            if self.list_globale[yb][xb].tag != "mur" and (
                self.act.get((xb, yb), lambda *args : True)(self, (xb, yb))
            ):

                n_2move = [0, -2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True



        if not mur :
           
            self._movepers(n_2move, posorneg, xory, 8)

        else :
            if not self.rls["pers"] :
                self.after(50, self._mur_keytest)
            else :
                self.r["pers"] = True
                if self.touche_save["pers"] is not None :
                    if self.touche_save["pers"].keysym.lower() != self.touche :
                        self.clavier_press(self.touche_save["pers"])
            


    def _mur_keytest(self) : 
        "Permet d'\u00E9viter de devoir s'arr\u00EAter apres \u00EAtre entr\u00E9 dans un mur."

        if self.rls["pers"] :
            self.r["pers"] = True
            if self.touche_save["pers"] is not None :
                if self.touche_save["pers"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["pers"])

        else :
            self.after(50, self._mur_keytest)
        



    
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

        for name in self.doors : # syncro des portes et bouttons
            
            for ele in ["door", "button"] : # ele -> door or button

                self.doors[name][ele]["img_pos"][xory] += posorneg[xory] * self.ZOOM *4
                x = self.doors[name][ele]["img_pos"][0]
                y = self.doors[name][ele]["img_pos"][1]

                self.play_canvas.coords(self.doors[name][ele]["obj"], x, y)

        

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


logger.info("This programme has taken {} to setup.".format(perf_counter()-t1))

root.mainloop()

for temp in temps :
    os.remove(temp)
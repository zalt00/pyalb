# -*- coding: utf-8 -*-

from time import perf_counter
t1 = perf_counter()

import numpy as np
import tkinter as tk
from Images.imgs_manip import LabObj, PNGS, save_img, create_bg
from glob import glob
import os
import logging as lg
from logging.handlers import RotatingFileHandler
from json import load as jsload
from PIL import Image
import tkinter.font as tkFont


# CWD = r"C:\Users\Timelam\git\pyalb\pyalb\src\Labyrinth2"
# os.chdir(CWD)


temps = set() # fichiers temporaires



logger = lg.getLogger()
logger.setLevel(lg.DEBUG)

formatter = lg.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = RotatingFileHandler('labyrinth.log', 'a', 1000000, 1)

file_handler.setLevel(lg.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)





class Root(tk.Tk) :

    def __init__(self, *args, **kwarks) :

        super().__init__(*args, **kwarks)


        self.in_game = InGameInterface(self)
        self.main_menu = MainMenuInterface(self, borderwidth=0, highlightthickness=0)

        self.com = dict()


    def change_page(self, actual, new) :
        
        getattr(self, actual).pack_forget()
        getattr(self, new).pack(fill="both", expand=True)
        






class MainMenuInterface(tk.Frame) :

    def __init__(self, root, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)


        self.root = root
        
        self.root.bind_all("<KeyPress-Escape>", lambda *a : self.quit())

        self.menu_map_dis = dict()

        for a in glob("Cartes/*.json") :
            
            b = a[7:-5]
            self.menu_map_dis[b] = a
        

        self.canvas = tk.Canvas(self)

        self.img = tk.PhotoImage(file="Images/main_menu_bg_resized.png")
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")

        self.canvas.pack(fill="both", expand=True)

        # self.img_txt = tk.PhotoImage(file="Images/txt_main_menu.png")
        # self.canvas.create_image(
        #     root.winfo_screenwidth() // 2,
        #     root.winfo_screenheight() // 2 + root.winfo_screenheight() // 4,
        #     image = self.img_txt
        # )
        
        self.img_txt = tk.PhotoImage(file="Images/txt_main_menu.png")

        self.button_start = tk.Button(
            self.canvas,
            command=self.start,
            image=self.img_txt
        )
        self.canvas.focus_set()

        self.window = self.canvas.create_window(
            root.winfo_screenwidth() // 2,
            root.winfo_screenheight() // 2 + root.winfo_screenheight() // 4,
            window=self.button_start
        )
        # self.menu_label = tk.Label(self, text="S\u00E9lectionnez une carte parmi celles-ci :")


        # self.menu_button = tk.Button(self, text="Valider", command=self.get_map)


        # self.menu_liste = tk.Listbox(self, selectmode=tk.SINGLE, height=len(self.menu_map_dis)+1, width=35)
        # i = 1
        # for carte in self.menu_map_dis.keys() :
        #     self.menu_liste.insert(i, carte)
        #     i += 1

        # self.menu_label.pack()
        # self.menu_liste.pack()
        # self.menu_button.pack(side=tk.RIGHT)

    def start(self, *args) :

        self.img_txt = None

        self.map_choice_frame = tk.Frame(self.canvas)

        self.button_list = list()
        

        for i, carte in enumerate(self.menu_map_dis.keys()) :

            self.button_list.append(tk.Button(
                self.map_choice_frame,
                text=carte,
                command=lambda path=carte : self.get_map(path),
                width=50
            ))

            self.button_list[i].pack()




        self.canvas.itemconfigure(
            self.window,
            window=self.map_choice_frame
        )


    def get_map (self, carte) :

        json_path = self.menu_map_dis[carte]


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

        self.play_canvas = tk.Canvas(self.fenetre, height=self["height"], background="#bbb", highlightthickness=0)
        
        self.coords = [0, 0]
        self.rlcoords = np.zeros(2, dtype=np.int)

        self.pos_bgrl = [0, 0]


        self.r = {"pers" : True, "cam" : True} # permet d'eviter l'appuyage prolongé de windows sur une touche
        self.rls = {"pers" : True, "cam" : True} # passe en True quand KeyRelease
        self.touche_save = {"pers" : None, "cam" : None} # permet de faire des virages fluides, sans pause
        self.touche = {"pers" : None, "cam" : None}

        
        self.play_canvas.focus_set()
        self.play_canvas.bind("<KeyPress>", self.clavier_press)
        self.play_canvas.bind("<KeyRelease>", self.clavier_release)
        self.play_canvas.pack(expand=True, fill="both")

        self.true = {"ontouch": lambda *a : True}

        self.animations = dict()
        for animations in glob("Images\\Animations\\*\\*a.png") : # chargement des animations

            a = animations.split("\\")
            if not a[2] in self.animations :
                self.animations[a[2]] = list()

            self.animations[a[2]].append(tk.PhotoImage(file=animations))
        # self.animations -> nom_de_lanimation : liste des tk.Photoimage de l'animation dans l'ordre


    def play(self) :

        

        carte = self.root.com["data"]["map_path"]

        self.rlcoords[0] = self.root.com["data"]["pers_x"]
        self.rlcoords[1] = self.root.com["data"]["pers_y"]

        self.coords[0] = self.psimg(self.root.com["data"]["pers_x"])
        self.coords[1] = self.psimg(self.root.com["data"]["pers_y"])


        global create_bg
        width_tab, height_tab, self.list_globale = create_bg(carte, "Images/bg.png", temps)

        self.pos_bgrl[0] = width_tab//2
        self.pos_bgrl[1] = height_tab//2


        self.bg_img = tk.PhotoImage(file="Images/bg.png")
        self.bg = self.play_canvas.create_image(self.pos_bgrl[0], self.pos_bgrl[1], image=self.bg_img)


        self.entities = self.root.com["data"]["entities"]
        self.act = dict() # cf en-dessous de la def de change_state

        options = {

            "door" : self._case_door,
            "button" : self._case_button
        }

        self.but_modes = {

            "activate" : self._but_activate,
            "switch" : self._but_switch,

            "multiactivate" : self._but_multiactivate,
            "multiswitch" : self._but_multiswitch
        }


        for entity_type, ele in self.entities.items() : # loads entities

            for entity_name in ele :

                entity = self.entities[entity_type][entity_name]

                x, y = entity["coords"]
                entity["img_on"] = tk.PhotoImage(file=entity["app_on"]) # apparence quand desactive
                entity["img_off"] = tk.PhotoImage(file=entity["app_off"]) # apparence quand active

                if entity["activated"] :
                    entity["obj"] = self.play_canvas.create_image(self.psimg(x), self.psimg(y), image=entity["img_on"])
                else :
                    entity["obj"] = self.play_canvas.create_image(self.psimg(x), self.psimg(y), image=entity["img_off"])

                entity["type"] = entity_type
                entity["onimg_coords"] =  [self.psimg(x), self.psimg(y)]
                entity["change_state"] = lambda entity=entity : self._change_img(entity)
                # change_state correspond a l'action visuelle relative au changement d'etat (animations, etc), 
                # tandis que self.act donne a partir de coordonnees une action a effectuer lors du contact de l'entity sur le joueur


                options[entity_type]((x, y), entity)

            


        self.pers_img = tk.PhotoImage(file="Images/pers.png")
        self.pers = self.play_canvas.create_image(self.coords[0], self.coords[1], image=self.pers_img)



    
    def _change_img(self, entity) :
        
        if entity["activated"] :
            
            if entity["on_animation"] :
                self.after(8, self.play_animation, entity["on_animation"], entity, entity["img_on"])
            else :
                self.play_canvas.itemconfigure(entity["obj"], image=entity["img_on"])


        else :

            if entity["off_animation"] :
                self.after(8, self.play_animation, entity["off_animation"], entity, entity["img_off"])
            else :
                self.play_canvas.itemconfigure(entity["obj"], image=entity["img_off"])



    def _case_door(self, coords, entity) :

        self.act[coords] = lambda entity=entity : entity["activated"]


    def _case_button(self, coords, entity) :
        
        self.act[coords] = lambda entity=entity : self.but_modes[entity["mode"]](entity)



    def _but_activate(self, entity) :

        a = entity["args"].split("/")

        target = self.entities[a[0]][a[1]]

        if not target["activated"] :
            target["activated"] = 1
            target.get("change_state", lambda *a : None)()

        if not entity["activated"] :
            entity["activated"] = 1
            entity.get("change_state", lambda *a : None)()
        

        return True


    def _but_switch(self, entity) :

        a = entity["args"].split("/")

        target = self.entities[a[0]][a[1]]

        target["activated"] = not target["activated"]
        entity["activated"] = not entity["activated"]
        target.get("change_state", lambda *a : None)()
        entity.get("change_state", lambda *a : None)()


        return True


    def _but_multiswitch(self, entity) :

        for arg in entity["args"] :

            a = arg.split("/")
            target = self.entities[a[0]][a[1]]

            target["activated"] = not target["activated"]
            target.get("change_state", lambda *a : None)()

        entity["activated"] = not entity["activated"]
        entity.get("change_state", lambda *a : None)()

        return True




    def _but_multiactivate(self, entity) :

        for arg in entity["args"] :

            a = arg.split("/")
            target = self.entities[a[0]][a[1]]

            if not target["activated"] :
                target["activated"] = 1
                target.get("change_state", lambda *a : None)()

        if not entity["activated"] :
            entity["activated"] = 1
            entity.get("change_state", lambda *a : None)()

        return True




    def play_animation(self, animation_args, entity, last_img=None, animation_lt=None, i=0) :
        
        animation_name = animation_args[0]
        speed = animation_args[1]


        if i == 0 :
            animation_lt = self.animations[animation_name]
            try :
                if animation_args[2] != "reverse" :
                    raise IndexError
            except IndexError :
                animation_lt = self.animations[animation_name]
            else :
                animation_lt = self.animations[animation_name][::-1]


        if i == len(self.animations[animation_name]) :
            if last_img is not None :
                self.play_canvas.itemconfigure(entity["obj"], image=last_img)
        else :
            self.play_canvas.itemconfigure(entity["obj"], image=animation_lt[i])
            self.after(speed, self.play_animation, animation_args, entity, last_img, animation_lt, i+1)





    def psimg (self, pos) :
        return (4+8*pos)*2



    def clavier_press (self, event) :
        touche = event.keysym.lower()
        if touche == "escape" : self.quit()
        

        if touche in "zqsd" :

            if self.r["pers"] :
                self._pers_evt(touche)
            else :
                self.touche_save["pers"] = event


        if touche in "oklm" :

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


    def entity_test(self, x, y) :

        
        return self.act.get((x, y), lambda : True)()


    def move_pers(self, x, y) :
        
        mur = False

        posorneg = x, y # positive or negative

        if x > 0 :
            xb, yb = self.rlcoords[0]+1, self.rlcoords[1]
            if self.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True
        
        elif x < 0 :
            xb, yb = self.rlcoords[0]-1, self.rlcoords[1]
            if self.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [-2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y > 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]+1
            if self.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [0, 2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y < 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]-1
            if self.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [0, -2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True



        if not mur :
           
            self._movepers(n_2move, posorneg, xory, 8)

        else :
            if not self.rls["pers"] :
                self.after(128, self._mur_keytest)
            else :
                self.r["pers"] = True
                if self.touche_save["pers"] is not None :
                    if self.touche_save["pers"].keysym.lower() != self.touche :
                        self.clavier_press(self.touche_save["pers"])
            


    def _mur_keytest(self) : 
        "Permet d'\u00E9viter un arr\u00EAt apr\u00E8s rencontre avec un mur."

        if self.rls["pers"] :
            self.r["pers"] = True
            if self.touche_save["pers"] is not None :
                if self.touche_save["pers"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["pers"])

        else :
            self.after(128, self._mur_keytest)
        



    
    def _todo_after_movepers(self, posorneg, xory) :
        

        self.coords[xory] += posorneg[xory] * 16
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

        n_2move[xory] += posorneg[xory] * 2
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
            
        self.coords[xory] += posorneg[xory] * 8
        self.play_canvas.coords(self.pers, self.coords[0], self.coords[1])

        self.pos_bgrl[xory] += posorneg[xory] * 8
        self.play_canvas.coords(self.bg, self.pos_bgrl[0], self.pos_bgrl[1])

        for entity_type, ele in self.entities.items() : # syncro des portes et boutons
            
            for entity_name in ele :
                
                entity = self.entities[entity_type][entity_name]

                entity["onimg_coords"][xory] += posorneg[xory] * 8
                x, y = entity["onimg_coords"]

                self.play_canvas.coords(entity["obj"], x, y)

        

        if not self.rls["cam"] :
            self.after(16, self._movebg, posorneg, xory)
        else :
            self.r["cam"] = True
            if self.touche_save["cam"] is not None :
                if self.touche_save["cam"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["cam"])






    def clavier_release(self, event):
        
        touche = event.keysym.lower()

        if touche in "zqsd" :
            self.rls["pers"] = True

            if self.touche_save["pers"] is not None :
                if event.keysym.lower() == self.touche_save["pers"].keysym.lower() :
                    self.touche_save["pers"] = None
        
        elif touche in "olmk" :
            self.rls["cam"] = True

            if self.touche_save["cam"] is not None :
                if event.keysym.lower() == self.touche_save["cam"].keysym.lower() :
                    self.touche_save["cam"] = None


        







root = Root()
root.title("Labyrinth")
root.attributes('-fullscreen', True)

root.main_menu.pack(fill="both", expand=True)


logger.info("This programme has taken {} to setup.".format(perf_counter()-t1))

root.mainloop()

for temp in temps :
    os.remove(temp)
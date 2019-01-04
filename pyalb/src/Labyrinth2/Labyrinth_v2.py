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
import dynamic_entity as dyent
import static_entity as stent


# CWD = r"C:\Users\Timelam\git\pyalb\pyalb\src\Labyrinth2"
# os.chdir(CWD)

NO_COLLISION = True


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

        self.start_txt = self.canvas.create_text(
            root.winfo_screenwidth() // 8 *7,
            root.winfo_screenheight() // 7 *5,
            text="Start",
            fill="white",
            font=["Consolas", -45, "bold"]
        )

        self.canvas.bind("<Button-1>", self.click)

        self.img_but = tk.PhotoImage(file="Images/Buttons/button.png")

        # self.button_start = tk.Button(
        #     self.canvas,
        #     command=self.start,
        #     image=self.img_but,
        #     relief="flat",
        #     borderwidth=0,
        #     background="black"
        # )
        # self.canvas.focus_set()

        # self.window = self.canvas.create_window(
        #     root.winfo_screenwidth() // 2,
        #     root.winfo_screenheight() // 2 + root.winfo_screenheight() // 4,
        #     window=self.button_start
        # )
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

    def click(self, evt) :

        item = self.canvas.find_closest(evt.x, evt.y)
        
        if item[0] == self.canvas.find_withtag(self.start_txt)[0] :
            self.start()


    def start(self, *args) :

        self.canvas.delete(self.start_txt)

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




        self.window = self.canvas.create_window(
            root.winfo_screenwidth() // 2,
            root.winfo_screenheight() // 4 *3,
            window=self.map_choice_frame
        )

        self.canvas.delete(self.start_txt)



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
        
        self.coords = np.zeros(2, dtype=np.int)
        self.rlcoords = np.zeros(2, dtype=np.int)

        self.pos_bg = np.zeros(2, dtype=np.int)


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

        self.pos_bg[0] = width_tab//2
        self.pos_bg[1] = height_tab//2
        self.defaultposbg = np.copy(self.pos_bg)

        self.bg_img = tk.PhotoImage(file="Images/bg.png")
        self.bg = self.play_canvas.create_image(self.pos_bg[0], self.pos_bg[1], image=self.bg_img)



        st = self.root.com["data"].get("static_entities", {})
        self.static_entities = dict()
        self.stentcoords = dict() # <entity coords> : entity

        for entity_type, ele in st.items() :

            for entity_name in ele :
                
                ent_options = st[entity_type][entity_name]
                entity = getattr(stent, entity_type)(self, **ent_options)

                self.static_entities[entity_type + "/" + entity_name] = entity

                self.stentcoords[tuple(ent_options["rlcoords"])] = entity




        


        self.dynamic_entities = dict()
        self.dyentcoords = dict()
        dy = self.root.com["data"].get("dynamic_entities", {}) # pour raccourcir

        for entity_type, ele in dy.items() :

            for entity_name in ele :
                
                ent_options = dy[entity_type][entity_name]
                entity = getattr(dyent, entity_type)(self, **ent_options)



                self.dynamic_entities[entity_type + "/" + entity_name] = entity
                
                self.dyentcoords[tuple(ent_options["rlcoords"])] = entity










        self.pers_img = tk.PhotoImage(file="Images/pers.png")
        self.pers = self.play_canvas.create_image(self.coords[0], self.coords[1], image=self.pers_img)



        self.screen = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        oos = np.array((width_tab, height_tab)) - np.array(self.screen) # oos = out of screen
        self.maxposbg = self.defaultposbg - oos

        self.test_persorcam_move = { # permet de tester si une coordonnee dans une certaine direction depasse le tier de l'ecran
            (0, -1) : lambda new_coords: (new_coords[1] > self.screen[1] // 3) or self.defaultposbg[1] == self.pos_bg[1],
            (0, 1) : lambda new_coords: ((new_coords[1] < self.screen[1] * 2 // 3) or
                self.maxposbg[1] == self.pos_bg[1]),

            (1, 0) : lambda new_coords: ((new_coords[0] < self.screen[0] * 2 // 3) or
                self.maxposbg[0] == self.pos_bg[0]),
            (-1, 0) : lambda new_coords: (new_coords[0] > self.screen[0] // 3) or self.defaultposbg[0] == self.pos_bg[0]
        } # si vrai, le personnage doit se deplacer




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
            new_rlcoords = self.rlcoords + (0, -1)
            new_coords = self.coords + (0, -16)
            ispers = new_coords[1] > self.screen[1] // 3
            self.move_pers(0, -1, new_rlcoords, new_coords, ispers)

        elif self.touche["pers"] == "s" :
            new_rlcoords = self.rlcoords + (0, 1)
            new_coords = self.coords + (0, 16)
            ispers = new_coords[1] < self.screen[1] * 2 // 3
            self.move_pers(0, 1, new_rlcoords, new_coords, ispers)

        elif self.touche["pers"] == "d" :
            new_rlcoords = self.rlcoords + (1, 0)
            new_coords = self.coords + (16, 0)
            ispers = new_coords[0] < self.screen[0] * 2 // 3
            self.move_pers(1, 0, new_rlcoords, new_coords, ispers)
                        
        elif self.touche["pers"] == "q" :
            new_rlcoords = self.rlcoords + (-1, 0)
            new_coords = self.coords + (-16, 0)
            ispers = new_coords[0] > self.screen[0] // 3
            self.move_pers(-1, 0, new_rlcoords, new_coords, ispers)

        else :
            self.r["pers"] = True


    def entity_test(self, x, y) :

        
        a = self.stentcoords.get((x, y), None)
        if a is not None :
            return a.contact()
        return True


    def move_pers(self, x, y, new_rlcoords, new_coords, ispers) :
        
        mur = False

        ispers = self.test_persorcam_move[(x, y)](new_coords)

        way = np.array((x, y), dtype=np.int)

        
        xb, yb = new_rlcoords
        if not (self.list_globale[yb][xb].tag != "mur" and 
            self.entity_test(xb, yb)
        ) :

            # n_2move = [2, 0] # x puis y
            # xory = 0 # 0 pour x, 1 pour y
            mur = True


        if NO_COLLISION :
            mur = False


        if not mur :
           

            n_2move = way*2

            if not ispers:
                self._movecam(n_2move, way, 8)
            else :
                self._movepers(n_2move, way, 8)

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
        



    
    def _todo_after_moving(self, way, ispers=True) :
        
        if ispers :
            self.coords += way * 16
        else :
            self.pos_bg -= way * 16
        self.rlcoords += way

        if not self.rls["pers"] :
            new_rlcoords = self.rlcoords + way
            new_coords = self.coords + way * 16
            ispers = self.test_persorcam_move[tuple(way)](new_coords)
            self.after(6, self.move_pers, *way, new_rlcoords, new_coords, ispers)
        else :
            self.r["pers"] = True
            if self.touche_save["pers"] is not None :
                if self.touche_save["pers"].keysym.lower() != self.touche :
                    self.clavier_press(self.touche_save["pers"])


    def _movepers(self, n_2move, way, nb) :

        self.play_canvas.move(self.pers, n_2move[0], n_2move[1])

        nb -= 1
        if nb != 0 :
            self.after(12, self._movepers, n_2move, way, nb)
        else :
            self.after(6, self._todo_after_moving, way)

    

    def _movecam(self, n_2move, way, nb) :

        self.play_canvas.move(self.bg, -n_2move[0], -n_2move[1])

        nb -= 1
        if nb != 0 :
            self.after(12, self._movecam, n_2move, way, nb)
        else :
            self.after(6, self._todo_after_moving, way, False)



        
    def move_bg(self, x, y) :
        
        way = np.array((x, y))
        



        self._movebg(way)


    def _movebg(self, way) :
            
        self.coords += way * 8
        self.play_canvas.coords(self.pers, self.coords[0], self.coords[1])

        self.pos_bg += way * 8
        self.play_canvas.coords(self.bg, self.pos_bg[0], self.pos_bg[1])

        for element in self.static_entities.values(), self.dynamic_entities.values() : # syncro des entites statiques
            
            for entity in element :


                entity.coords += way * 8
                x, y = entity.coords

                self.play_canvas.coords(entity.item, x, y)

        



        


        if not self.rls["cam"] :
            self.after(16, self._movebg, way)
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
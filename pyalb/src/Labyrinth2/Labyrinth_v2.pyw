# -*- coding: utf-8 -*-

import logging as lg
import os
import pickle
import tkinter as tk
from glob import glob
from json import load as jsload
from logging.handlers import RotatingFileHandler
from threading import enumerate as enumerate_threads
from time import perf_counter

import numpy as np
from PIL import Image

import Entities.dynamic_entity as dyent
import Entities.static_entity as stent
import Xbox_controller_threads as xcth
from event_handlers import KeyboardHandler, XboxControllerHandler
from Images.imgs_manip import PNGS, LabObj, create_bg, save_img

t1 = perf_counter()



# CWD = r"C:\Users\Timelam\git\pyalb\pyalb\src\Labyrinth2"
# os.chdir(CWD)

ISKEYBOARD = False

NO_COLLISION = False

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

        self.bind_all("<KeyPress-Delete>", lambda *a : self.quit())


    def change_page(self, actual, new) :
        
        getattr(self, actual).pack_forget()
        getattr(self, new).pack(fill="both", expand=True)


    def reinitialise(self, attr, new_class, **kwargs) :
        
        getattr(self, attr).destroy()
        setattr(self, attr, new_class(self, **kwargs))
        






class MainMenuInterface(tk.Frame) :

    def __init__(self, root, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)


        self.root = root
        

        self.menu_map_dis = dict()

        for a in glob("Cartes/*.json") :
            
            b = a[7:-5]
            self.menu_map_dis[b] = a
        

        self.canvas = tk.Canvas(self)

        self.img = tk.PhotoImage(file="Images/main_menu_bg_resized.png")
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")

        self.canvas.pack(fill="both", expand=True)


        self.start_txt = self.canvas.create_text(
            root.winfo_screenwidth() // 7,
            root.winfo_screenheight() // 7 *5,
            text="Start",
            fill="white",
            activefill="gray",
            font=["Lucida", 38],
            tag="text"
        )

        self.quit_txt = self.canvas.create_text(
            root.winfo_screenwidth() // 7,
            root.winfo_screenheight() // 7 *5 + 100,
            text="Quit ",
            fill="white",
            activefill="gray",
            font=["Lucida", 38],
            tag="text"
        )



        self.canvas.bind("<Button-1>", self.click)




    def click(self, evt) :

        item = self.canvas.find_closest(evt.x, evt.y)
        
        if item :
            if item[0] == self.canvas.find_withtag(self.start_txt)[0] :
                self.start()
            elif item[0] == self.canvas.find_withtag(self.quit_txt)[0] :
                self.root.quit()


    def start(self, *args) :

        self.canvas.delete("text")

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
        

        self.play_canvas = tk.Canvas(self, height=self["height"], background="#bbb", highlightthickness=0)
        
        self.coords = np.zeros(2, dtype=np.int)
        self.rlcoords = np.zeros(2, dtype=np.int)

        self.pos_bg = np.zeros(2, dtype=np.int)


        self.rls = {"pers" : True, "cam" : True} # passe en True quand KeyRelease

        
        self.play_canvas.focus_set()
        self.play_canvas.pack(expand=True, fill="both")



        with open('data', 'rb') as data_file :
            unpickler = pickle.Unpickler(data_file)
            data = unpickler.load()

        self.sensibilities = data['controller_sensibility']

        if ISKEYBOARD :
            self.controls = data['keyboard_controls']
        else :
            self.controls = data['controller_controls']





        self.animations = dict()
        for animations in glob("Images\\Animations\\*\\*a.png") : # chargement des animations

            a = animations.split("\\")
            if not a[2] in self.animations :
                self.animations[a[2]] = list()

            self.animations[a[2]].append(tk.PhotoImage(file=animations))
        # self.animations -> nom_de_lanimation : liste des tk.Photoimage de l'animation dans l'ordre

        self.static_entities = dict()
        self.stentcoords = dict() # <entity coords> : entity

        self.dynamic_entities = dict()
        self.dyentcoords = dict()


    def play(self) :

        

        carte = self.root.com["data"]["map_path"]

        self.rlcoords[0] = self.root.com["data"]["pers_x"]
        self.rlcoords[1] = self.root.com["data"]["pers_y"]

        self.coords[0] = self.psimg(self.root.com["data"]["pers_x"])
        self.coords[1] = self.psimg(self.root.com["data"]["pers_y"])


        global create_bg
        width_tab, height_tab, list_globale = create_bg(carte, "Images/bg.png", temps)

        self.global_tab = np.array(list_globale)

        self.pos_bg[0] = width_tab//2
        self.pos_bg[1] = height_tab//2
        self.defaultposbg = np.copy(self.pos_bg)


        self.screen = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        oos = np.array((width_tab, height_tab)) - np.array(self.screen) # oos = out of screen
        self.maxposbg = self.defaultposbg - oos

        self.test_persorcam_move = { # permet de tester si une coordonnee dans une certaine direction depasse le tier de l'ecran
            (0, -1) : lambda new_coords: (new_coords[1] > self.screen[1] * 11 // 30) or self.defaultposbg[1] == self.pos_bg[1],
            (0, 1) : lambda new_coords: ((new_coords[1] < self.screen[1] * 19 // 30) or
                self.maxposbg[1] == self.pos_bg[1]),

            (1, 0) : lambda new_coords: ((new_coords[0] < self.screen[0] * 19 // 30) or
                self.maxposbg[0] == self.pos_bg[0]),
            (-1, 0) : lambda new_coords: (new_coords[0] > self.screen[0] * 11 // 30) or self.defaultposbg[0] == self.pos_bg[0]
        } # si vrai, le personnage doit se deplacer, si faux, la camera doit se deplacer dans l'autre sens



        self.bg_img = tk.PhotoImage(file="Images/bg.png")
        self.bg = self.play_canvas.create_image(self.pos_bg[0], self.pos_bg[1], image=self.bg_img)

        self.entities = list()


        st = self.root.com["data"].get("static_entities", {})

        for entity_type, ele in st.items() :

            for entity_name in ele :
                
                ent_options = st[entity_type][entity_name]
                entity = getattr(stent, entity_type)(self, **ent_options)

                self.static_entities[entity_type + "/" + entity_name] = entity
                self.entities.append(entity)

                self.stentcoords[tuple(ent_options["rlcoords"])] = entity




        


        dy = self.root.com["data"].get("dynamic_entities", {}) # pour raccourcir

        for entity_type, ele in dy.items() :

            for entity_name in ele :
                
                ent_options = dy[entity_type][entity_name]
                entity = getattr(dyent, entity_type)(self, **ent_options)



                self.dynamic_entities[entity_type + "/" + entity_name] = entity
                self.entities.append(entity)

                self.dyentcoords[tuple(ent_options["rlcoords"])] = entity


        if ISKEYBOARD :
            self.event_handler = KeyboardHandler(self.keys_handler, self.key_release)
            self.play_canvas.bind("<KeyPress>", self.event_handler.key_press)
            self.play_canvas.bind("<KeyRelease>", self.event_handler.key_release)
            self.play_canvas.focus_set()
        else :
            self.event_handler = XboxControllerHandler(self.keys_handler, self.key_release)
            self.thread = xcth.ListeningThread(self.sensibilities, self.event_handler.key_input)
            self.thread.start()






        self.pers_img = tk.PhotoImage(file="Images/pers.png")
        self.pers = self.play_canvas.create_image(self.coords[0], self.coords[1], image=self.pers_img)






    def psimg (self, pos) :
        return (4+8*pos)*2



    def keys_handler(self, key) :
        if key == self.controls["return_to_main_menu"] : self.reinitialise()

        elif key in self.controls["pers_controls"].values() :

            self._pers_evt(key)


        elif key in self.controls["cam_controls"].values() :
            pass # todo
            # if self.r["cam"] :
            #     self._bg_evt(key)      
            # else :
            #     self.key_save["cam"] = key


    # def _bg_evt (self, key) :
    #     self.r["cam"] = False
    #     self.key_save["cam"] = None
    #     self.key["cam"] = key.lower()
    #     self.rls["cam"] = False


    #     if self.key["cam"] == "l" :
    #         self.move_bg(0, -1)
            
    #     elif self.key["cam"] == "o" :
    #         self.move_bg(0, 1)

    #     elif self.key["cam"] == "k" :
    #         self.move_bg(1, 0)

    #     elif self.key["cam"] == "m" :
    #         self.move_bg(-1, 0)

    #     else :
    #         self.r["cam"] = True            
            

    def _pers_evt (self, key) :

            
        self.rls["pers"] = False
           
            
        if key == self.controls["pers_controls"]["up"] :
            new_rlcoords = self.rlcoords + (0, -1)
            new_coords = self.coords + (0, -16)
            ispers = self.test_persorcam_move[(0, -1)](new_coords)
            self.move_pers(0, -1, new_rlcoords, new_coords, ispers)

        elif key == self.controls["pers_controls"]["down"] :
            new_rlcoords = self.rlcoords + (0, 1)
            new_coords = self.coords + (0, 16)
            ispers = self.test_persorcam_move[(0, 1)](new_coords)
            self.move_pers(0, 1, new_rlcoords, new_coords, ispers)

        elif key == self.controls["pers_controls"]["right"] :
            new_rlcoords = self.rlcoords + (1, 0)
            new_coords = self.coords + (16, 0)
            ispers = self.test_persorcam_move[(1, 0)](new_coords)
            self.move_pers(1, 0, new_rlcoords, new_coords, ispers)
                        
        elif key == self.controls["pers_controls"]["left"] :
            new_rlcoords = self.rlcoords + (-1, 0)
            new_coords = self.coords + (-16, 0)
            ispers = self.test_persorcam_move[(-1, 0)](new_coords)
            self.move_pers(-1, 0, new_rlcoords, new_coords, ispers)

        else :
            self.event_handler.end_of_animation()


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
        if not (self.global_tab[yb, xb].tag != "mur" and 
            self.entity_test(xb, yb)
        ) :

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

            self.event_handler.end_of_animation()

    
    def _todo_after_moving(self, way, ispers=True) :
        
        if ispers :
            self.coords += way * 16
        else :
            self.pos_bg -= way * 16
            for entity in self.entities :
                entity.coords -= way * 16

        self.rlcoords += way



        if not self.rls["pers"] :
            new_rlcoords = self.rlcoords + way
            new_coords = self.coords + way * 16
            ispers = self.test_persorcam_move[tuple(way)](new_coords)
            self.after(6, self.move_pers, *way, new_rlcoords, new_coords, ispers)
        
        elif self.event_handler.saved_key != "" :
            self.event_handler.key = self.event_handler.saved_key
            self.event_handler.saved_key = ""
            self.keys_handler(self.event_handler.key)
        else :
            self.event_handler.end_of_animation()



    def _movepers(self, n_2move, way, nb) :

        self.play_canvas.move(self.pers, n_2move[0], n_2move[1])

        nb -= 1
        if nb != 0 :
            self.after(16, self._movepers, n_2move, way, nb)
        else :
            self.after(10, self._todo_after_moving, way)

    

    def _movecam(self, n_2move, way, nb) :

        self.play_canvas.move(self.bg, -n_2move[0], -n_2move[1])
        self.play_canvas.move("Entity", -n_2move[0], -n_2move[1])

        nb -= 1
        if nb != 0 :
            self.after(16, self._movecam, n_2move, way, nb)
        else :
            self.after(10, self._todo_after_moving, way, False)



        
    # def move_bg(self, x, y) :
        
    #     way = np.array((x, y))
        



    #     self._movebg(way)


    # def _movebg(self, way) :
            
    #     self.coords += way * 8
    #     self.play_canvas.move(self.pers, *(way*8))

    #     self.pos_bg += way * 8
    #     self.play_canvas.move(self.bg, *(way*8))

    #     self.play_canvas.move("Entity", *(way*8))

    #     for entity in self.entities :
    #         entity.coords -= way * 8



    #     if not self.rls["cam"] :
    #         self.after(16, self._movebg, way)
    #     else :
    #         self.r["cam"] = True
    #         if self.key_save["cam"] is not None :
    #             if self.key_save["cam"].keysym.lower() != self.key :
    #                 self.keys_handler(self.key_save["cam"])






    def key_release(self, key):
        

        if key in self.controls["pers_controls"].values() :
            self.rls["pers"] = True

        
        elif key in self.controls["cam_controls"].values() :
            self.rls["cam"] = True

        else :
            self.event_handler.end_of_animation()




    def reinitialise(self, *args) :
        
        self.root.reinitialise("in_game", InGameInterface)
        self.root.reinitialise("main_menu", MainMenuInterface)

        self.root.change_page("in_game", "main_menu")


    def destroy(self) :
        thread = getattr(self, 'thread', None)
        if thread is not None :
            thread.stop = True
        tk.Frame.destroy(self)
        







root = Root()
root.title("Labyrinth")
root.attributes('-fullscreen', True)

root.main_menu.pack(fill="both", expand=True)


logger.info("This programme has taken {} to setup.".format(perf_counter()-t1))

root.mainloop()

for temp in temps :
    os.remove(temp)


for thread in enumerate_threads() : # stop remaining threads (only usefull if something forces the game to shutdown)
    if isinstance(thread, xcth.ListeningThread) :
        thread.stop = True
        print("Si ce message persiste, veuillez appuyer sur un bouton de votre controlleur.")
        logger.warning('''The game didn't shutdown properly. Please use the "quit" option in the main menu to quit the game''')
        thread.join()

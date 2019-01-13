# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
import Entities.behaviour.entity_behaviour as ebh


class DynamicEntity :


    def __init__(self, interface, **options) :
        
        self.ismoving = False

        self.rlcoords = np.array(options["rlcoords"])

        self.coords = np.array(options.get("coords", self.psimg(self.rlcoords)))
        
        self.speed = options.get("speed", 16)

        self.way = options.get("way", "north")


        self.canvas = interface.play_canvas
        self.inter = interface
        # self.canvas = canvas
        # self.rlcoords = np.array(rlcoords, dtype=np.int)

        # self.coords = self.psimg(self.rlcoords) if coords==None else coords  
        
        self.item = "must be replaced by the id of the canvas item"



    def _todo_after_move(self, way) :
        

        self.coords += way * 16
        self.rlcoords += way
        self.ismoving = False


    def _move(self, n_2move, way, nb) :

        self.canvas.move(self.item, n_2move[0], n_2move[1])

        nb -= 1
        if nb != 0 :
            self.canvas.after(self.speed, self._move, n_2move, way, nb)
        else :
            self.canvas.after(self.speed, self._todo_after_move, way)


    def entity_test(self, x, y) :

        
        a = self.inter.stentcoords.get((x, y), None)
        if a is not None :
            return a.contact()
        return True


    def move_entity(self, x, y, new_rlcoords) :
        
        self.ismoving = True
        mur = False

        way = np.array((x, y), dtype=np.int)

        
        xb, yb = new_rlcoords
        if not (self.inter.global_tab[yb, xb].tag != "mur" and 
            self.entity_test(xb, yb)
        ) :

            # n_2move = [2, 0] # x puis y
            # xory = 0 # 0 pour x, 1 pour y
            mur = True


        if not mur :
           

            n_2move = way*2
            self._move(n_2move, way, 8)

        else :
            self.ismoving = False




    def psimg (self, pos) :
        return (4+8*pos)*2




class Bourpi(DynamicEntity) :


    def __init__(self, interface, **options) :

        DynamicEntity.__init__(self, interface, **options)

        img_path = "Images/entityImages/Bourpi/default_app.png"

        self.img = tk.PhotoImage(file=img_path)
        self.item = self.canvas.create_image(self.coords[0], self.coords[1], image=self.img, tag="Entity")
        
        args = list()
        kwargs = dict()

        if isinstance(options["behaviour"], list) :
            behaviour = options["behaviour"][0]

            if options["behaviour"][1] == "kwargs" :
                kwargs = options["behaviour"][2]
                try :
                    args = options["behaviour"][3:]
                except IndexError :
                    pass

            else :
                args = options["behaviour"][1:]

        else :
            behaviour = options["behaviour"]



        # Syntaxe :
        # string seule -> nom de du comportement
        # liste -> nom du comportement en premiere position, puis :
        #    - les autres argument args
        #         OU
        #    - chaine "kwargs" en deuxieme position, suivi du dictionnaire des kwargs en troisieme,
        #    suivit eventuellement d'arguments supplementaires args
        #    - pour certains comportements il est necessaire d'avoir un argument 'secondary_behaviour' en kwargs


        try :
            secondary_behaviour = getattr(ebh, kwargs["secondary_behaviour"])
        except KeyError :
            pass
        else :
            kwargs["secondary_behaviour"] = secondary_behaviour


        self.behaviour = getattr(ebh, behaviour)(self, *args, **kwargs)









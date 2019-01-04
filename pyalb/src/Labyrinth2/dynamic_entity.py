# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
from numpy.random import randint, choice


class DynamicEntity :


    def __init__(self, interface, **options) :
        
        self.ismoving = False

        self.rlcoords = np.array(options["rlcoords"])

        self.coords = np.array(options.get("coords", self.psimg(self.rlcoords)))
        
        self.speed = options.get("speed", 16)

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
        if not (self.inter.list_globale[yb][xb].tag != "mur" and 
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
        
        exec("self.comportement = {}(self)".format(options["comportement"]))








class Comportement :

    def __init__(self, entity) :
        self.entity = entity





class RandomMoving(Comportement) :

    def __init__(self, entity, arrlen=100, imediatly_run=True) :
        Comportement.__init__(self, entity)

        self.arrlen = arrlen
        self.depxory = randint(0, 2, self.arrlen)
        self.depposneg = choice((1, -1), self.arrlen)
        self.i = 0

        if imediatly_run :
            self.run()


    
    def new_way(self):
        
        stop = False # Never True, "while True" would be the same.
        while not stop :
    
            if self.i < self.arrlen :
                results = np.zeros(2, dtype=np.int)

                xory = self.depxory[self.i]
                results[xory] = self.depposneg[self.i]
                self.i+=1

                return results

            else :

                self.arrlen *= 2
                self.depxory = randint(0, 2, self.arrlen)
                self.depposneg = choice((1, -1), self.arrlen)
                self.i=0
            


    def run(self, recall=True) :

        if not self.entity.ismoving :
            way = self.new_way()
            new_rlcoords = self.entity.rlcoords + way
            self.entity.move_entity(*way, new_rlcoords)

        if recall :
            self.entity.inter.after(24, self.run)
        

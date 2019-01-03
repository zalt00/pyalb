# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
from numpy.random import randint, choice


class DynamicEntity :


    def __init__(self, interface, **options) :
        
        self.ismoving = False

        self.rlcoords = np.array(options["rlcoords"])

        self.coords = np.array(options.get("coords", self.psimg(self.rlcoords)))
        

        self.canvas = interface.play_canvas
        self.inter = interface
        # self.canvas = canvas
        # self.rlcoords = np.array(rlcoords, dtype=np.int)

        # self.coords = self.psimg(self.rlcoords) if coords==None else coords  
        
        self.item = "must be replaced by the id of the canvas item"



    def _todo_after_move(self, posorneg, xory) :
        

        self.coords[xory] += posorneg[xory] * 16
        self.rlcoords[xory] += posorneg[xory]
        self.ismoving = False


    def _move(self, n_2move, posorneg, xory, nb) :

        self.canvas.coords(self.item, self.coords[0]+n_2move[0], self.coords[1]+n_2move[1])

        n_2move[xory] += posorneg[xory] * 2
        nb -= 1
        if nb != 0 :
            self.canvas.after(12, self._move, n_2move, posorneg, xory, nb)
        else :
            self.canvas.after(6, self._todo_after_move, posorneg, xory)


    def entity_test(self, x, y) :

        
        a = self.inter.stentcoords.get((x, y), None)
        if a is not None :
            return a.contact()
        return True


    def move_entity(self, x, y) :
        
        self.ismoving = True
        mur = False

        posorneg = x, y # positive or negative

        if x > 0 :
            xb, yb = self.rlcoords[0]+1, self.rlcoords[1]
            if self.inter.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True
        
        elif x < 0 :
            xb, yb = self.rlcoords[0]-1, self.rlcoords[1]
            if self.inter.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [-2, 0] # x puis y
                xory = 0 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y > 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]+1
            if self.inter.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [0, 2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True

        elif y < 0 :
            xb, yb = self.rlcoords[0], self.rlcoords[1]-1
            if self.inter.list_globale[yb][xb].tag != "mur" and (
                self.entity_test(xb, yb)
            ) :

                n_2move = [0, -2] # x puis y
                xory = 1 # 0 pour x, 1 pour y
            else :
                mur = True



        if not mur :
           
            self._move(n_2move, posorneg, xory, 8)

        else : 
            self.ismoving = False



    def psimg (self, pos) :
        return (4+8*pos)*2




class Bourpi(DynamicEntity) :


    def __init__(self, interface, **options) :

        DynamicEntity.__init__(self, interface, **options)

        img_path = "Images/entityImages/Bourpi/default_app.png"

        self.img = tk.PhotoImage(file=img_path)
        self.item = self.canvas.create_image(self.coords[0], self.coords[1], image=self.img)
        
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
            a = self.new_way()
            self.entity.move_entity(*a)

        if recall :
            self.entity.inter.after(24, self.run)
        

# -*- coding: utf-8 -*-

import tkinter as tk

import numpy as np
from numpy.random import choice, randint

import Entities.behaviour.visual_tracking as vt


class Behaviour :

    def __init__(self, entity, *args, **kwargs) :
        self.entity = entity

    def run(self, *args, **kwargs) :
        pass


class RandomMoving(Behaviour) :

    def __init__(self, entity, arrlen=100, imediatly_run=True) :
        Behaviour.__init__(self, entity)

        self.arrlen = arrlen
        self.depxory = randint(0, 2, self.arrlen)
        self.depposneg = choice((1, -1), self.arrlen)
        self.i = 0

        self.tuple2way = {
            (0, -1) : "north",
            (0, 1) : "south",
            (-1, 0) : "east",
            (1, 0) : "west"
        }


        if imediatly_run :
            self.run()


    
    def new_way(self):
        
        if self.i >= self.arrlen :
            self.arrlen *= 2
            self.depxory = randint(0, 2, self.arrlen)
            self.depposneg = choice((1, -1), self.arrlen)
            self.i=0

        results = np.zeros(2, dtype=np.int)

        xory = self.depxory[self.i]
        results[xory] = self.depposneg[self.i]
        self.i+=1

        return results, self.tuple2way[tuple(results)]
            


    def run(self, recall=True) :

        if not self.entity.ismoving :

            new_way = self.new_way()
            way_array = new_way[0]
            self.entity.way = new_way[1]
            new_rlcoords = self.entity.rlcoords + way_array
            if self.entity.inter.global_tab[tuple(new_rlcoords)[::-1]].tag == "mur" :
                self.run(False)
            else :
                self.entity.move_entity(*way_array, new_rlcoords)

        if recall :
            self.entity.inter.after(24, self.run)



class VisualTracking(Behaviour) :

    def __init__(self, entity, secondary_behaviour, imediatly_run=True) :
        Behaviour.__init__(self, entity)
        vt.BaseCell.tab = self.entity.inter.global_tab

        self.secondary_behaviour = secondary_behaviour(self.entity, imediatly_run=False)

        self.north = dict(
            front=(-1, 0),
            left=(0, -1),
            right=(0, 1)
        )

        self.south = dict(
            front=(1, 0),
            left=(0, 1),
            right=(0, -1)
        )
        
        self.west = dict(
            front=(0, -1),
            left=(1, 0),
            right=(-1, 0)
        )

        self.east = dict(
            front=(0, 1),
            left=(-1, 0),
            right=(1, 0)
        )

        self.last_known_coords = None

        if imediatly_run :
            self.run()


    def run(self, recall=True) :
        result = tuple()
        if not self.entity.ismoving :
            result, aux_results = self.searching()

            if result is not None :
                
                
                entity_way = getattr(self, self.entity.way)

                y, x = entity_way[result[0]]
                self.entity.move_entity(x, y, self.entity.rlcoords + (x, y))

                self.last_known_coords = result[1]
                vt.BaseCell.aux_target_coords["last_known_coords"] = self.last_known_coords

                
            elif (self.last_known_coords == self.entity.rlcoords[::-1]).all() :
                self.secondary_behaviour.run(recall=False)
                vt.BaseCell.aux_target_coords.pop("last_known_coords", None)


            elif "last_known_coords" in aux_results.keys():
                entity_way = getattr(self, self.entity.way)

                y, x = entity_way[aux_results["last_known_coords"]]
                self.entity.move_entity(x, y, self.entity.rlcoords + (x, y))
            else :
                self.secondary_behaviour.run(recall=False)

        if recall :
            self.entity.canvas.after(150, self.run)


    def searching(self) :

        x, y = self.entity.rlcoords
        xb, yb = self.entity.inter.rlcoords

        vt.define_variables(
            target_coords=(yb, xb),
            **getattr(self, self.entity.way)
        )

        
        vt.BaseCell.cells[y, x] = vt.Base((y, x))
        vt.BaseCell.cells[y, x].start()

        return vt.BaseCell.result, vt.BaseCell.aux_results
        

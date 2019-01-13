# -*- coding: utf-8 -*-

import numpy as np


def define_variables(**options) :

    """needed :

        tab : array-like,
        front, left and right : tuple,
        target_coords : tuple
    """

    for attr, value in options.items() :
        setattr(BaseCell, attr, value)




class BaseCell :
    cells = dict()
    result = None
    aux_results = dict()
    tab = np.empty(0) # to redefine
    front = np.zeros(2, dtype=np.int)
    left = np.zeros(2, dtype=np.int)
    right = np.zeros(2, dtype=np.int)
    aux_target_coords = dict()
    target_coords = np.zeros(2, dtype=np.int)



class Cell(BaseCell) :
    
    def __init__(self, coords, base) :
        self.coords = np.asarray(coords, dtype=np.int)
        self.base = base
        

        
        if (self.coords == BaseCell.target_coords).all() :
            self.target_touched()

        for name, aux_coords in BaseCell.aux_target_coords.items() :
            if (self.coords == aux_coords).all() :
                BaseCell.aux_results[name] = self.base
        
        self.new_cell()
        
        
    def new_cell(self) :
        
        
        if BaseCell.result is None :

            new_coords = tuple(self.coords + BaseCell.front)
            if BaseCell.tab[new_coords].tag != "mur" :
                BaseCell.cells[new_coords] = FrCell(new_coords, self.base)
                
            return True
        return False
    
    
                
    def target_touched(self) :
        BaseCell.result = (self.base, self.coords)
        BaseCell.cells.clear()




class FrCell(Cell) :
    pass



class LtCell(Cell) :
    
    def new_cell(self) :
        
        execute = Cell.new_cell(self)
        
        if execute :

            new_coords_left = tuple(self.coords + BaseCell.front + BaseCell.left)
            if BaseCell.tab[new_coords_left].tag != "mur" :
                BaseCell.cells[new_coords_left] = LtCell(new_coords_left, self.base)



class RtCell(Cell) :
    
    def new_cell(self) :
        
        execute = Cell.new_cell(self)
        
        if execute :


            new_coords_right = tuple(self.coords + BaseCell.front + BaseCell.right)
            if BaseCell.tab[new_coords_right].tag != "mur" :
                BaseCell.cells[new_coords_right] = RtCell(new_coords_right, self.base)




class Base(BaseCell) :
    
    def __init__(self, coords) :
        
        self.coords = np.asarray(coords, dtype=np.int)
    
    def start(self) :
        
        BaseCell.result = None
        BaseCell.cells.clear()
        BaseCell.aux_results.clear()

        new_coords_front = self.coords + BaseCell.front
        new_coords_frleft = tuple(new_coords_front + BaseCell.left)
        new_coords_frright = tuple(new_coords_front + BaseCell.right)
        coords_left = self.coords + BaseCell.left
        coords_right = self.coords + BaseCell.right
        new_coords_front = tuple(new_coords_front)
        
        if BaseCell.tab[new_coords_front].tag != "mur" :
            BaseCell.cells[new_coords_front] = FrCell(new_coords_front, "front")

        if BaseCell.tab[new_coords_frleft].tag != "mur" :
            way = "left" if BaseCell.tab[tuple(coords_left)].tag != "mur" else "front"
            BaseCell.cells[new_coords_frleft] = LtCell(new_coords_frleft, way)

        if BaseCell.tab[new_coords_frright].tag != "mur" :
            way = "right" if BaseCell.tab[tuple(coords_right)].tag != "mur" else "front"
            BaseCell.cells[new_coords_frleft] = RtCell(new_coords_frright, way)
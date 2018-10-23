# -*-coding:utf-8 -*


'''
Created on 23 oct. 2018

@author: Timelam
'''

from ClassesLab import *




def Move(direction, pos_obj_x, pos_obj_y, tab):
    
    if direction == "z" :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y - 1
    elif direction == "d" :
        nxt_pos_x = pos_obj_x + 1
        nxt_pos_y = pos_obj_y
    elif direction == "s" :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y + 1
    elif direction == "q" :
        nxt_pos_x = pos_obj_x - 1
        nxt_pos_y = pos_obj_y
    else :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y
        
    if tab[nxt_pos_x, nxt_pos_y].tag == "mur":
        return (pos_obj_x, pos_obj_y)
    else :
        return (nxt_pos_x, nxt_pos_y)
        
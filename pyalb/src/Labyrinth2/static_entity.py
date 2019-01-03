# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np

class StaticEntity :

    def __init__(self, interface, **options) :


        self.interface = interface
        self.canvas = interface.play_canvas

        self.rlcoords = np.array(options["rlcoords"], dtype=np.int)
        self.coords = options.get("coords", self.psimg(self.rlcoords))

        self.app_on = tk.PhotoImage(file=options.get("app_on", "Images/PNGS/_ _nth.png"))
        self.app_off = tk.PhotoImage(file=options.get("app_off", "Images/PNGS/_ _nth.png"))

        self.activated = bool(options.get("activated", False))

        self.on_animation = options.get("on_animation", False)
        self.off_animation = options.get("off_animation", False)

        x, y = self.coords
        if self.activated :
            self.item = self.canvas.create_image(x, y, image=self.app_on)
        else :
            self.item = self.canvas.create_image(x, y, image=self.app_off)




    def psimg(self, pos) :
        return (4+8*pos)*2



    def play_animation(self, animation, last_img, animation_lt=None, i=0) :
        

        animation_name = animation[0]
        speed = animation[1]


        if animation_lt is None :
            animation_lt = self.interface.animations[animation_name]
            try :
                if animation[2] != "reverse" :
                    raise IndexError
            except IndexError :
                animation_lt = self.interface.animations[animation_name]
            else :
                animation_lt = self.interface.animations[animation_name][::-1]


        if i == len(self.interface.animations[animation_name]) :
            self.canvas.itemconfigure(self.item, image=last_img)
        else :
            self.canvas.itemconfigure(self.item, image=animation_lt[i])
            self.canvas.after(speed, self.play_animation, animation, last_img, animation_lt, i+1)



    def change_state(self) :

        if self.activated :
            if self.off_animation :
                self.play_animation(self.off_animation, self.app_off)
            else :
                self.canvas.itemconfigure(self.item, image=self.app_off)
            self.activated = False

        else :
            if self.on_animation :
                self.play_animation(self.on_animation, self.app_on)
            else :
                self.canvas.itemconfigure(self.item, image=self.app_on)
            self.activated = True

    
    def refresh_pos(self) :
        self.canvas.coords(self.item, self.coords[0], self.coords[1])



    def contact(self) :
        "method called when the player hits this entity"
        return True





class Door(StaticEntity) :

    def contact(self) :
        return self.activated




class Button(StaticEntity) :

    def __init__(self, interface, **options) :

        StaticEntity.__init__(self, interface, **options)
        
        self.target = set()

        if type(options["args"]) == str :
            self.target.add(interface.static_entities[options["args"]])

        else :
            for path2target in options["args"] :
                self.target.add(interface.static_entities[path2target])


    def contact(self) :
        return True




class ButtonSwitch(Button) :

    def contact(self) :

        self.change_state()

        for target in self.target :
            target.change_state()

        return True

        

class ButtonActivate(Button) :

    def contact(self) :

        if not self.activated :
            self.change_state()

        for target in self.target :
            if not target.activated :
                target.change_state()

        return True
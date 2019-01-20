# -*- coding: utf-8 -*-

class EventHandler :

    def __init__(self, key_press_func, key_release_func) :

        self.key_press_func = key_press_func
        self.key_release_func = key_release_func




class KeyboardHandler(EventHandler) :


    def __init__(self, key_press_func, key_release_func) :
        """To connect with tkinter event binding"""
        EventHandler.__init__(self, key_press_func, key_release_func)

        self.r = True # is False while holding
        self.saved_key = ""

    def key_press(self, evt) :
        """evt -> tkinter keypress event"""
        key = evt.keysym.upper()
        if self.r :
            self.saved_key = ""
            self.r = False
            self.key = key
            self.key_press_func(self.key)

        elif key != self.key :
            self.saved_key = key



    def key_release(self, evt) :

        key = evt.keysym.upper()
        if key == self.key :
            self.key_release_func(self.key)
        elif key == self.saved_key :
            self.saved_key = ""

    def end_of_animation(self) :
        """trigger de l'objet en reponse au release pour attendre la fin de l'animation"""
        self.r = True



class XboxControllerHandler(EventHandler) :

    def __init__(self, key_press_func, key_release_func, sensibilities) :
        """To connect with Xbox_controller_threads Reading thread event handler"""
        EventHandler.__init__(self, key_press_func, key_release_func)

        self.sensibilities = sensibilities
        self.isreleasing = False # permet de reconnaitre un release avec un joystick
        self.saved_key = ""


    def key_input(self, evt) :
        """evt -> xbox controller event"""
        self.key = evt.code.upper()
        if evt.ev_type == "Key" :
            if evt.state :
                self.key_press_func(self.key)
            else :
                self.key_release_func(self.key)

        if evt.ev_type == "Absolute" :
            if (abs(evt.state) >= self.sensibilities[self.key]) and (not self.isreleasing):
                self.isreleasing = True
                a = '+' if evt.state > 0 else "-"
                self.key_press_func(self.key + a)

            if (abs(evt.state) <= self.sensibilities[self.key]) and self.isreleasing :
                self.isreleasing = False
                a = '+' if evt.state > 0 else "-"
                self.key_release_func(self.key + a)

    def end_of_animation(self) :
        pass
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

    def __init__(self, key_press_func, key_release_func) :
        """To connect with Xbox_controller_threads Reading thread event handler"""
        EventHandler.__init__(self, key_press_func, key_release_func)

        self.saved_key = ""
        self.r = True
        self.key = ""


    def key_input(self, evt, simple_state=None, releasing=False):


        if simple_state is not None :
            sign = '+' if simple_state > 0 else '-'
            key = (evt.code + sign).upper()
        else :
            key = evt.code.upper()


        if not releasing :
            self.key_press(key)
        else :
            self.key_release(key)


    def key_press(self, key) :

        if self.r :
            self.r = False
            self.key = key
            self.saved_key = ""
            self.key_press_func(self.key)
        else :
            self.saved_key = key


    def key_release(self, key) :
        
        if key == self.key :
            self.key_release_func(self.key)
        elif key == self.saved_key :
            self.saved_key = ""


    def end_of_animation(self) :
        self.r = True
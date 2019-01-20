# -*- coding: utf-8 -*-

from collections import deque

from inputs import devices


class Base :

    xinput_queue = deque()

    def __init__(self, frame) :
        self.frame = frame

class Listening(Base) :

    def __init__(self, frame) :
        super().__init__(frame)

        self.gamepad = devices.gamepads[0]

        self.stop = False


    def run(self) :

        xinput = self.gamepad.read()[0]
        if xinput.ev_type != "Sync" :
            Base.xinput_queue.append(xinput)

        if not self.stop :
            self.frame.after(30, self.run)




class Reading(Base) :

    def __init__(self, frame, event_handler) :
        super().__init__(frame)

        self.stop = False
        self.event_handler = event_handler


    def run(self) :
        
        
        try :
            xinput = Base.xinput_queue[0]
        except IndexError :
            pass
        else :
            Base.xinput_queue.popleft()
            self.event_handler(xinput)

        if not self.stop :
            self.frame.after(30, self.run)

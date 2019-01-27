# -*- coding: utf-8 -*-

from inputs import devices

gamepad = devices.gamepads[0]

sensibilities = {
    
    "ABS_X" : 30000,
    "ABS_RX" : 30000,
    "ABS_Y" : 30000,
    "ABS_RY" : 30000,
    
    "ABS_Z" : 254,
    "ABS_RZ" : 254
}



def event_handler(evt, simple_state=None, releasing=False) :
    if releasing :
        print(evt.code, simple_state, "Releasing")
    else :
        print(evt.code, simple_state)



def main(sensibilities=sensibilities, eveny_handler=event_handler) :
    kb = devices.keyboards[0]
    print(kb.read())


if __name__ == '__main__' :
    main()

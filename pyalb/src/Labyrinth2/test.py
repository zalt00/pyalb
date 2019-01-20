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
    stop = False
    activated = dict()

    while not stop :
        xinput = gamepad.read()[0]
        if xinput.code == "BTN_SELECT" and xinput.state == 1:
            stop = True
        elif xinput.ev_type == 'Absolute' :
            if xinput.state > 0 :
                state = 1
            else :
                state = -1
                
            if abs(xinput.state) >= sensibilities[xinput.code] :

                if not activated.get(xinput.code + str(state), False) :
                    activated[xinput.code + str(state)] = True
                    event_handler(xinput, state, False)
                    
            elif activated.get(xinput.code + str(state), False) :
                activated[xinput.code + str(state)] = False
                event_handler(xinput, state, True)

        elif xinput.ev_type == 'Key' :
            event_handler(xinput, releasing=not xinput.state)


if __name__ == '__main__' :
    main()

# -*- coding: utf-8 -*-

import pickle



keyboard_controls = {

            
    "pers_controls" : {
        "up" : "Z",
        "down" : "S",
        "right" : "D",
        "left" : "Q",
    },

    "cam_controls" : {
        "cam_up" : "O",
        "cam_down" : "L",
        "cam_right" : "M",
        "cam_left" : "K",
    },

    "return_to_main_menu" : "ESCAPE"

}


controller_controls = {
            
    "pers_controls" : {
        "up" : "ABS_Y+",
        "down" : "ABS_Y-",
        "right" : "ABS_X+",
        "left" : "ABS_X-",
    },

    "cam_controls" : {
        "up" : "ABS_RY+",
        "down" : "ABS_RY-",
        "right" : "ABS_RX+",
        "left" : "ABS_RX-",
    },

    "return_to_main_menu" : "BTN_SELECT"

}


controller_sensibility = {

    "ABS_Y" : 23000,
    "ABS_X" : 23000,
    "ABS_RY" : 23000,
    "ABS_RX" : 23000,

    "ABS_Z" : 254,
    "ABS_RZ" : 254,

    "ABS_HAT0Y" : 0,
    "ABS_HAT0X" : 0

}


data = {

    "keyboard_controls" : keyboard_controls,
    "controller_controls" : controller_controls,
    "controller_sensibility" : controller_sensibility
}

with open("data", 'wb') as data_file :
    pickler = pickle.Pickler(data_file)
    pickler.dump(data)
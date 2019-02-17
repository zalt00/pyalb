#! C:\Users\HeleneLeBerre\envs\setup_level.py\python.exe
# -*- coding: utf-8 -*-


import numpy as np
import pickle


a = np.zeros((100, 50), dtype=np.uint16)

level_dict = dict()

level_dict['screens_data'] = dict()

positions = np.array((0,), dtype=np.uint16)
level_dict['screens_data']['position'] = positions

level_dict['screens_data']['screens'] = a,



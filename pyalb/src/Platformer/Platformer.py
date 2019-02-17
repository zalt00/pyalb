#! C:\Users\HeleneLeBerre\envs\setup_level.py\python.exe
# -*- coding: utf-8 -*-


import pickle
import sys
import numpy as np
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from PIL import Image, ImageTk
from glob import iglob
import os
from setup_level import load_blocks, parse_level, properly_resize_img


class Viewer(tk.Frame):

    def __init__(self, master, **kwargs):
        super(Viewer, self).__init__(master, **kwargs)

        self.root = master
        self.root.attributes('-fullscreen', True)

        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self)
        self.canvas['highlightthickness'] = 0
        self.canvas.pack(fill='both', expand=True)

        self.main_menu_displayer = None
        self.game_displayer = None

    def display_main_menu(self):

        self.main_menu_displayer = self.MainMenuDisplayer(self)

    class MainMenuDisplayer:

        def __init__(self, mmviewer):

            self.canvas = mmviewer.canvas

            self.mmbg_img = tk.PhotoImage(file='Images/bg.png')
            mmviewer.canvas.create_image(0, 0, image=self.mmbg_img, anchor='nw')

            self.screenwidth = mmviewer.screenwidth
            self.screenheight = mmviewer.screenheight

            self.mmviewer = mmviewer
            self.level_choice_displayer = None

            self.display_text()

        def display_text(self):

            self.canvas.create_text(
                self.screenwidth // 7,
                self.screenheight // 7 * 5 - 100,
                text="New Game",
                fill="white",
                activefill="gray",
                font=["Lucida", 38],
                tags=("text", 'new_game')
            )

            self.canvas.create_text(
                self.screenwidth // 7 - 40,
                self.screenheight // 7 * 5,
                text="Options",
                fill="white",
                activefill="gray",
                font=["Lucida", 38],
                tags=("text", 'options')
            )

            self.canvas.create_text(
                self.screenwidth // 7 - 80,
                self.screenheight // 7 * 5 + 100,
                text="Quit",
                fill="white",
                activefill="gray",
                font=["Lucida", 38],
                tags=("text", 'quit')
            )

        def delete_text(self):
            self.canvas.delete('text')

    class GameDisplayer:

        def __init__(self):
            pass


class Controller:

    def __init__(self, model, viewer):

        self.model = model
        self.viewer = viewer

        self.n_x = 20
        self.n_y = None

        self.level_img = None
        self.array_level_img = None

        self.mainmenu_controller = None
        self.ingame_controller = None

        self.create_mainmenu()
        self.viewer.display_main_menu()

        self.binfos = None

    def load_level(self, path):

        with open(path, 'rb') as level_file:
            unpickler = pickle.Unpickler(level_file)
            level = unpickler.load()

        array_map = level.get('array_map', None)
        if array_map is None:
            raise KeyError('Loaded dictionary must have an "array_map" key.')

        blocks = load_blocks()
        aunresized_level_img, self.model.solid_blocks_array = parse_level(array_map, blocks)

        unresized_level_img = Image.fromarray(aunresized_level_img)

        self.level_img = properly_resize_img(unresized_level_img, self.viewer.screenheight, 50)
        self.binfos = '50|h' #  number | h (height) or w (width)

        level_data = level.get('level_data', None)
        if level_data is None:
            raise KeyError('Loaded dictionary must have an "level_data" key.')

        self.model.load_lvldata(level_data)

        print(0)

    def create_mainmenu(self):
        self.mainmenu_controller = self.MainMenu(self)

    class MainMenu:

        def __init__(self, main_controller):

            main_viewer = main_controller.viewer

            main_viewer.display_main_menu()
            main_viewer.canvas.bind('<Button-1>', self.click)
            main_viewer.canvas.focus_set()

            self.current_menu = 'main'

            self.viewer = main_viewer
            self.main_controller = main_controller

        def click(self, evt):
            item = self.viewer.canvas.find_closest(evt.x, evt.y)

            if item and item != self.viewer.main_menu_displayer.mmbg_img:
                tags = self.viewer.canvas.gettags(item[0])
                try:
                    try:
                        getattr(self, tags[1])(tags[2])
                    except TypeError:
                        getattr(self, tags[1])()
                except IndexError:
                    pass

        def new_game(self):
            self.current_menu = None
            print('new_game')
            self.start()

        def options(self):
            print('options')

        def quit(self):
            self.viewer.quit()
            sys.exit()

        def start(self):
            self.viewer.main_menu_displayer.canvas.delete('all')
            del self.viewer.main_menu_displayer

            self.main_controller.start_game()
            del self.main_controller.mainmenu_controller

    def start_game(self):
        self.viewer.game_displayer = self.viewer.GameDisplayer()
        self.ingame_controller = self.InGame(self)

    class InGame:

        def __init__(self, main_controller):

            self.controller = main_controller
            self.viewer = main_controller.viewer
            self.model = main_controller.model

            self.player = self.Player(self.viewer, Image.open('pers.png'))

            level_img = main_controller.level_img
            if level_img is None:
                raise self.LevelNotLoadedError('Level must be loaded before the game starts.')
            else:
                self.level_img = ImageTk.PhotoImage(level_img)

            n, horw = self.controller.binfos.split('|')
            n = int(n)
            onscreen_bsize = self.viewer.screenheight / n if horw == 'h' else self.viewer.screenwidth / n
            base_levelimg_coords = self.player.coords + tuple(
                int(round(a / 2 - onscreen_bsize / 2)) for a in level_img.size)
            self.level_img_coords = base_levelimg_coords - self.model.player_coords * onscreen_bsize

            self.viewer.canvas.create_image(*self.level_img_coords, image=self.level_img)

            self.viewer.canvas.tag_raise('player')

        class LevelNotLoadedError(Exception):
            pass

        class Player:

            def __init__(self, igviewer, img, on_screen_coords='center'):

                self.viewer = igviewer

                self.img = ImageTk.PhotoImage(img)
                if on_screen_coords == 'center':
                    self.coords = np.array(
                        (self.viewer.screenwidth // 2, self.viewer.screenheight // 2),
                        dtype=np.int32
                    )
                else:
                    self.coords = np.array(on_screen_coords, dtype=np.int32)
                    if not isinstance(self.coords, np.ndarray):
                        raise TypeError('Coordinates must be a np.ndarray instance.')
                    if not len(self.coords.flat) == 2:
                        raise ValueError('Coordinates\' length must be 2.')

                self.viewer.canvas.create_image(*self.coords, image=self.img, tags=['player'])


class Model:

    def __init__(self):

        self.solid_blocks_array = None
        self.player_coords = None
        self.static_entities = None
        self.dynamic_entities = None

    def load_lvldata(self, data):
        try:
            self.player_coords = np.array(data['player_coords'], dtype=np.int32)

        except KeyError as e:
            #  add logger
            raise e

        self.static_entities = data.get('static_entities', None)
        if self.static_entities is not None:
            self.load_static_entities()

    def load_static_entities(self):
        pass


if __name__ == '__main__':

    root = tk.Tk()
    pr_viewer = Viewer(root)
    pr_model = Model()
    controller = Controller(pr_model, pr_viewer)
    pr_viewer.pack(fill='both', expand=1)
    controller.load_level('Levels/test/level_test.lvl')

    root.mainloop()

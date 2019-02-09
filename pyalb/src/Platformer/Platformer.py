#! C:\Users\HeleneLeBerre\envs\setup_level.py
# -*- coding: utf-8 -*-


import pickle
import sys
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

        def display_level_choice(self):
            self.delete_text()
            self.level_choice_displayer = self.LevelChoiceDisplayer(self.mmviewer)

        class LevelChoiceDisplayer:

            def __init__(self, mmviewer):

                self.canvas = mmviewer.canvas
                self.screenheight = mmviewer.screenheight
                self.screenwidth = mmviewer.screenwidth
                self.thumbnails = list()
                self.thumbnails_gray_border = list()

                self.load_thumbnails('Levels')
                self.display_thumbnails()

            def load_thumbnails(self, path):

                for directory in os.listdir(path):

                    for thumbnail_path in iglob('{}/{}/*_thumbnail.png'.format(path, directory)):
                        normpath = os.path.normpath(thumbnail_path)
                        image_pil = Image.open(normpath)
                        self.thumbnails.append((ImageTk.PhotoImage(image=image_pil), normpath))

                    for thumbnail_path in iglob('{}/{}/*_grayborder-thumbnail.png'.format(path, directory)):
                        normpath = os.path.normpath(thumbnail_path)
                        gbimage_pil = Image.open(normpath)
                        self.thumbnails_gray_border.append(ImageTk.PhotoImage(image=gbimage_pil))

            def display_thumbnails(self):

                if self.thumbnails:

                    for i, image in enumerate(self.thumbnails):
                        img_coords = int((i + 1) * self.screenwidth / 10), self.screenheight // 5 * 4

                        lvl_name = os.path.split(image[1])[-1][:-14]
                        self.canvas.create_image(
                            *img_coords,
                            image=image[0],
                            activeimage=self.thumbnails_gray_border[i],
                            tags=('thumbnail', 'start', lvl_name)
                        )


class Controller:

    def __init__(self, model, viewer):

        self.model = model
        self.viewer = viewer

        self.n_x = 20
        self.n_y = None

        self.level_img = None
        self.array_level_img = None

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

        level_data = level.get('level_data', None)
        if level_data is None:
            raise KeyError('Loaded dictionary must have an "level_data" key.')

        self.model.load_lvldata(level_data)

        print(0)

    class MainMenu:

        def __init__(self, main_viewer):

            main_viewer.display_main_menu()
            main_viewer.canvas.bind('<Button-1>', self.click)
            main_viewer.canvas.focus_set()

            self.current_menu = 'main'

            self.viewer = main_viewer

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
            self.current_menu = 'select_level'
            self.viewer.main_menu_displayer.display_level_choice()
            print('new_game')

        def options(self):
            print('options')

        def quit(self):
            self.viewer.quit()
            sys.exit()

        def start(self, lvl):

            print(lvl)


class Model:

    def __init__(self):

        self.solid_blocks_array = None
        self.player_coords = None
        self.static_entities = None
        self.dynamic_entities = None

    def load_lvldata(self, data):
        try:
            self.player_coords = data['player_coords']

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
    viewer = Viewer(root)
    model = Model()
    controller = Controller(model, viewer)
    viewer.pack(fill='both', expand=1)
    controller.load_level('Levels/test/level_test.lvl')

    mainmenu = controller.MainMenu(viewer)

    root.mainloop()

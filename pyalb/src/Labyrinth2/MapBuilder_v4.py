# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from json import load as jsload
from glob import glob
import numpy as np
from time import perf_counter
from Images.imgs_manip import LabObj, PNGS, save_img, create_bg, img_load
import logging as lg
from logging.handlers import RotatingFileHandler
import os






# CWD = r'C:\Users\Timelam\git\pyalb\pyalb\src\Labyrinth2'
# os.chdir(CWD)




SHAPES_TAB = (320, 320, 3) # dimension de la "zone de dessin", les deux premier sont deux multiples de 16, le dernier est 3

temps = set() # ensemble des fichiers temporaires


logger = lg.getLogger()
logger.setLevel(lg.DEBUG)

formatter = lg.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = RotatingFileHandler('map_builder.log', 'a', 1000000, 1)

file_handler.setLevel(lg.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




if SHAPES_TAB[0] % 16 != 0 or SHAPES_TAB[1] % 16 != 0 or SHAPES_TAB[2] != 3 :

    a = SHAPES_TAB[0]//16*16
    b = SHAPES_TAB[1]//16*16
    c = 3
    
    SHAPES_TAB = a, b, c

    logger.warning('SHAPES_TAB\'s value is invalid, his value is replaced by "{}".'.format(SHAPES_TAB))





class Interface(tk.Frame) :
    
    def __init__(self, root, shapes_tab, **kwargs):
        
        tk.Frame.__init__(self, root, **kwargs)

        self.define_controls()


        self.car = dict() # permet de conserver les caractères après déassignement de toutes les clefs du self.imgs
        self.tab = np.zeros(shapes_tab, dtype=np.uint8) # tab pour tableau

        self.file_name = askopenfilename(master=self, title="Ouvrir une carte où appuyez sur Annuler", filetypes=[('txt files','.txt'),('all files','.*')])

        root.attributes('-fullscreen', True)

        try:
            with open(self.file_name, "r", encoding="utf8") as fch :
                width, height, lt = create_bg(fch, "Images/bg_mpbuilder.png")

        except FileNotFoundError:
            logger.info("File {} not found".format(self.file_name))


        else:
            for y, eley in enumerate(lt) :
                yb = y*16+8

                for x, elex in enumerate(eley) :

                    xb = x*16+8
                    self.car[xb, yb] = elex.app


            tab2 = img_load("Images/bg_mpbuilder.png")

            a = np.array(shapes_tab, dtype=np.int) < np.array(tab2.shape, dtype=np.int) # compare shapes
            
            if len(np.nonzero(a)) != 0 : # si les dimensions debordent
                self.tab = tab2
            else :
                self.tab[:height, :width, :3] = tab2
                logger.warning("New tab's shape doesn't match with SHAPE_TAB")

        
        save_img(self.tab, "Images/bg_mpbuilder.png", temps)
    

        self.imgs = dict()


        self.canvas = tk.Canvas(self)
        self.canvas.bind("<KeyPress>", self.keypress)
        self.coords = np.array([8, 8], dtype=np.int)

        self._bg = tk.PhotoImage(file="Images/bg_mpbuilder.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self._bg, tags="img_bg")

        self.canvas.pack(expand=True, side="left", fill="both")
        self.canvas.focus_set()

        self.cur_img = tk.PhotoImage(file="Images/curseur.png")
        self.curseur = self.canvas.create_image(8, 8, image=self.cur_img)

        self.pngs = PNGS("Images/PNGS")

        self.imgs_paths = dict()

        for ele in self.pngs :
            
            self.imgs_paths[ele.app] = ele

        self.info_var = tk.StringVar()
        self.info_var.set("Hello")


        self.info_coords = self.canvas.create_text(
            root.winfo_screenwidth()-28,
            root.winfo_screenheight()-48,
            text="x=0\ny=0",
            font=('Helvetica', -20, 'bold')
        )


        self.todel = set() # set permettant de savoir quelles portions de la grande matrice supprimer après un escape
        # (les "delete" sur une carte composée d'un seule image grace à escape ne vont d'apparence 
        # rien faire jusqu'au prochain return)

        self.black = np.zeros((16, 16, 3), dtype=np.uint8)



        self.menubar = tk.Menu(self)

        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Save", command=self.save)
        self.menu1.add_command(label="Save as", command=self.save_as)
        self.menu1.add_separator()
        self.menu1.add_command(label="Close", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.menu1)

        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Open controls", command=lambda : os.system("open_controls.bat"))
        self.menu2.add_command(label="Refresh controls", command=self.define_controls)
        self.menubar.add_cascade(label="Controls", menu=self.menu2)

        root.configure(menu=self.menubar)



    def define_controls(self) :
        "Parses controls_mapbuilder.json and puts it into self.ctrls dictionnary "
        with open("controls_mapbuilder.json", "r", encoding="utf8") as data :
            self.ctrls = jsload(data)






    def keypress(self, evt):
        
        touche = evt.keysym
        
        if not (touche in ["Up", "Right", "Left", "Down", "Delete", "Shift_L", 'Caps_Lock', 'Escape', "Return"]) :
            
            
            if touche in self.ctrls :
                key_ch = self.ctrls[touche] # touche deduite grace au json
                
                coords = tuple(self.coords)
                srch = glob("Images/PNGS/{}".format(self.imgs_paths[key_ch].name))
                img_tab = self.imgs_paths[key_ch].code

                self.imgs[coords] = {
                    "image" : tk.PhotoImage(file=srch[0]), 
                    "key" : key_ch,
                    "tab" : img_tab
                }

                self.todel.discard(coords)

                self.canvas.create_image(*coords, image=self.imgs[coords]["image"])

                self.car[coords] = key_ch
                self.canvas.tag_raise(self.curseur)
            
            else :
                logger.debug('Key "{}" is invalid.'.format(touche))

        else :

            def todo_else() :
                pass
            
            option = {
                "Up" : lambda : self._move_cursor([0, -16]),
                "Down" : lambda : self._move_cursor([0, 16]),
                "Left" : lambda : self._move_cursor([-16, 0]),
                "Right" : lambda : self._move_cursor([16, 0]),
                "Return" : self.refresh_bg,
                "Delete" : self.delete
            }

            option.get(touche, todo_else)()


    def _move_cursor(self, way) :

        self.coords += np.array(way)

        a = self.coords < 8
        for ele in np.nonzero(a) :
            self.coords[ele] = 8

        self.canvas.coords(self.curseur, *tuple(self.coords))

        self.canvas.itemconfigure(self.info_coords, text="x={}\ny={}".format(*(self.coords-8)//16))


    def delete(self) :

        coords = tuple(self.coords)
        
        self.car.pop(coords, "car")
        self.imgs.pop(coords, "imgs")

        
        self.todel.add(coords)
        logger.info("Invisble delete until next Return.")


    def refresh_bg(self) :

        for coords in self.imgs.keys() :
            
            x = coords[0]-8
            y = coords[1]-8
            try :
                self.tab[y:y+16, x:x+16, :3] = self.imgs[coords]["tab"]
            except ValueError as e:
                logger.error("Given coords are out of bounds.")
                raise e

        for coordsb in self.todel :

            x = coordsb[0]-8
            y = coordsb[1]-8
            self.tab[y:y+16, x:x+16, :3] = self.black

        save_img(self.tab, "Images/bg_mpbuilder.png")
        self._bg = tk.PhotoImage(file="Images/bg_mpbuilder.png")
        self.canvas.itemconfigure("img_bg", image=self._bg)

        self.imgs.clear()



    def _tostr(self) :

        x, y = max(self.car.keys())
        xb, yb = (x-8)//16+1, (y-8)//16+1
        tab = np.zeros((yb, xb), dtype=np.str)

        logger.info("Shapes of the saved tab : {}".format((xb, yb)))

        for key, letter in self.car.items() :
            keyb = tuple([(k-8)//16 for k in key])
            keyc = keyb[1], keyb[0]
            tab[keyc] = letter
        

        tab_str = "\n".join(["".join(a) for a in tab.tolist()]) + "\n"

        return tab_str
        

    def save(self) :

        if self.file_name == "" :
            self.save_as()

        else :
            to_write = self._tostr()

            with open(self.file_name, "w", encoding="utf8") as map_file :
                map_file.write(to_write)




    def save_as(self) :

        self.file_name = asksaveasfilename(title="Sauvegarder sous :", filetypes=[('txt files','.txt'),('all files','.*')])

        to_write = self._tostr()

        with open(self.file_name, "w", encoding="utf8") as map_file :
            map_file.write(to_write)
        



root = tk.Tk()


inter = Interface(root, SHAPES_TAB)
inter.pack(fill="both", expand=True)
root.mainloop()


for temp in temps :
    os.remove(temp)  
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.image as mpimg
from glob import glob



class LabObj :
    
    
    def __init__(self, code, tag, app, name) :
        
        self.code = code
        self.tag = tag
        self.app = app
        self.name = name


def PNGS (path) :
    fch = glob("{}/*.png".format(path))
    
    pngs = list()
    
    for image in fch :
        image_tab = mpimg.imread(image)

        if image_tab.shape[2] == 4 :
            image_tab = image_tab[:,:,:3]
            
        if image_tab.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
            image_tab = (image_tab * 255).astype(np.uint8)
        

        
        img_name = image.split("\\")
        img_name = img_name[-1]
        
        image_obj = LabObj(image_tab, img_name[3:6], img_name[1], img_name)
        
        pngs.append(image_obj)

    

    return pngs



def img_load(name) :
    image_tab = mpimg.imread(name)

    if image_tab.shape[2] == 4 :
            image_tab = image_tab[:,:,:3]
            
    if image_tab.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
        image_tab = (image_tab * 255).astype(np.uint8)

    return image_tab



def save_img (img, name, var=None) :


    mpimg.imsave(name, img)

    if var is not None : # ajoute le nom du fichier a l'ensemble des fichiers temporaires
        var.add(name)



def create_bg(choosen_map, file_name, var=None) :

    r"""file_name
    nom du fichier temporaire"""

    if type(choosen_map) == str :
        with open(choosen_map, "r", encoding="utf8") as fichier:
            carte = fichier.read()
    
    else :
        carte = choosen_map.read()


    l = 0
    list_globale = [[]]
    list_globale_tab = []
    list_ligne_tab = list()



    pngs = PNGS("Images/PNGS")

    for caract in carte :
        
        if caract == "\n" :
            

            
            list_globale_tab.append(np.concatenate(list_ligne_tab, axis=1))
            list_globale.append([])
            list_ligne_tab = []
            l += 1
            
        else :
            
            for tile in pngs :
                
                if caract == tile.app:
                    list_globale[l].append(tile)
                    list_ligne_tab.append(tile.code)
            


    tab = np.concatenate(list_globale_tab, axis=0)


    save_img(tab, file_name, var)


    height_tab = tab.shape[0]
    width_tab = tab.shape[1]
    return width_tab, height_tab, list_globale

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.image as mpimg
from glob import glob



class LabObj :
    
    
    def __init__(self, code, tag, app) :
        
        self.code = code
        self.tag = tag
        self.app = app



def PNGS (path) :
    fch = glob("{}/*".format(path))
    
    pngs = list()
    
    for image in fch :
        image_tab = mpimg.imread(image)
        if image_tab.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
            image_tab = (image_tab * 255).astype(np.uint8)
        
        if image_tab.shape[2] == 4 :
            image_tab = image_tab[:,:,:3]
        
        img_name = image.split("\\")
        img_name = img_name[len(img_name)-1]
        
        if image.endswith("_nth.png"):
            image_obj = LabObj(image_tab, "void", img_name[1])
        else :
            image_obj = LabObj(image_tab, "mur", img_name[0])
        
        pngs.append(image_obj)

    

    return pngs


def save_img (img) :

    mpimg.imsave("Images/bg.png", img)

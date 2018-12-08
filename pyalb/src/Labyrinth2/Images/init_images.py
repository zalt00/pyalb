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
        
        image_obj = LabObj(image_tab, img_name[3:6], img_name[1])
        
        pngs.append(image_obj)

    

    return pngs


def save_img (img) :

    mpimg.imsave("Images/bg.png", img)

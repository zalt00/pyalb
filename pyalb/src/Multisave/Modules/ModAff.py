# -*-coding:Latin-1 -*
'''

Created on 22 sept. 2018

@author: Hélène Le Berre
'''

import glob

def SavePrint():
    b=list()
    a=glob.glob("multisave_save/*")
    for chemin in a:
        b += chemin.split("\\")
        b.remove("multisave_save")
    print("Sauvegardes existantes : {}".format(", ".join(b)))
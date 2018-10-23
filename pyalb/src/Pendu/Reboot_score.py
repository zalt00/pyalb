import pickle
import os

with open("score","wb") as fichier :
    hey = {}
    my = pickle.Pickler(fichier)
    my.dump(hey)

os.system("pause")
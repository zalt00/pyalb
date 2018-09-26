# -*-coding:Latin-1 -*

from random import randrange
inlist = list()

with open("donnee.txt", "r") as fichier : ###ligne 5à10 : récupération des données du document txt###
    thgs = fichier.read()
liste1 = thgs.split("\nEssais = ")
essais = liste1[len(liste1)-1]
del liste1[len(liste1)-1]
liste1=liste1[0].split("\n")

a = randrange(len(liste1)) ###coversion du mot choisi en une liste de lettres###
mot_choisi = liste1[a]
for lettre in mot_choisi :
    inlist += lettre


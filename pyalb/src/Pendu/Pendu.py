# -*-coding:Latin-1 -*

from random import randrange
from builtins import enumerate
import pickle

name = input("Saisir votre prénom : ")
with open("score", "rb") as fichier :
    my = pickle.Unpickler(fichier)
    scoredict = my.load()
    try :
        score = scoredict[name]
    except :
        scoredict[name] = int(0)
print("votre score :", scoredict[name])
     
with open("donnee.txt", "r") as fichier : ###ligne 5à10 : récupération des données du document txt###
    thgs = fichier.read()
liste1 = thgs.split("\nEssais =")
essais = liste1[len(liste1)-1]
del liste1[len(liste1)-1]
liste1=liste1[0].split("\n")
del(thgs) ###variables : essais = nb d'essais ; liste1= liste des mots

inlist = list()
a = randrange(len(liste1)) ###conversion du mot choisi en une liste de lettres###
mot_choisi = liste1[a]
for lettre in mot_choisi :
    inlist.append(lettre)
del(lettre)
del(a) ###inlist = mot converti en lettres ; liste1 = mot aléa ; pré

listaff = list() ###listaff = ******
for a in inlist :
    listaff.append("*")
del(a)

print(*listaff, sep = "")
essais = int(essais)  ###vif du programme, quand lettre_choisie == une lettre, affichage de la lettre###
while essais != 0 and "*" in listaff : ###tant que listaff n'est pas pleine et essais != 0
    lettre_choisie = input() 
    raté = False 
    for i,lettre in enumerate(inlist) :
        if lettre == lettre_choisie :
            listaff[i] = lettre
            inlist[i]= "786451"
            raté = True
    if raté == False :
        essais -= 1
        print("raté ! plus que {} essais !".format(essais))
    print(*listaff, sep = "")
    
score = int()
if essais == 0 :
    print("perdu")
else : 
    print("vous avez gagné!")
    scoredict[name] += 1
    print("votre score :", scoredict[name])
    with open("score", "wb") as fichier :
        my = pickle.Pickler(fichier)
        my.dump(scoredict)
    
    
    
    
# -*-coding:Latin-1 -*

from random import randrange
from builtins import enumerate
import pickle
import os

name = input("Saisir votre pseudonyme : ")
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

essais = int(essais)
keep = True
print("Vous avez {} essais".format(essais))
while essais != 0 and "*" in listaff :
    print(*listaff, sep = "")
    essais = int(essais)  ###vif du programme, quand lettre_choisie == une lettre, affichage de la lettre###
    while essais != 0 and "*" in listaff and keep == True: ###tant que listaff n'est pas pleine et essais != 0
        lettre_choisie = input() 
        if lettre_choisie == "settings" :
            keep = False
        else :
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
    if keep == False :
        print("Tapez 0 pour avoir la liste des joueurs et leur score\nTapez 1 pour supprimer un joueur\nTapez 2 pour reprendre")
    while essais != 0 and "*" in listaff and keep == False:
        settings = input()
        if settings == "0" :
            for player, sc in scoredict.items():
                print("Le joueur {} a un score de {}".format(player,sc))
        elif settings == "1" :
            player_del = input("Saisir nom du joueur à supprimer: ")
            try :
                if name == player_del :
                    print("Erreur - Impossible de supprimer la sauvegarde en cours")
                else :
                    del(scoredict[player_del])
                    with open("score", "wb") as fichier :
                        my = pickle.Pickler(fichier)
                        my.dump(scoredict[player_del])
                    print("Joueur {} supprimé avec succès".format(player_del))
            except KeyError:
                    print("Erreur - Nom introuvable")
        elif settings == "2" :
            keep = True
        

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
    
os.system("pause")
# -*-coding:Latin-1 -*


    


dic = dict()
chx = False
alld = str()
alldlt = list()
frlt = list()
from os import system, rename
from os import remove as rmfl

try :
    rmfl("Trié.txt")
except:
    print("- Fichier \"Trie.txt\" inexistant -")


with open("A trier.txt", "w") as hi :
    print("- Fichier créé -\n")

print("Entrez votre texte dans le fichier \"A trier\" \n\
Le trie ne prend pas en compte les maj et les déterminants,\n\
les caractères spéciaux sont mis à la fin\n\
Le trie sera implanté dans un nouveau fichier \"Trie\"\n\
Appuyez sur n'importe quelle touche pour continuer, le programme se fermera alors.\n ")
system("pause")

with open("A trier.txt", "r") as fichier:
    rec = fichier.read()
ltmot = rec.split("\n")

err = False
while not err : ###retire les str vides
    try :
        ltmot.remove(str())
    except ValueError:
        err = True


for i,mot in enumerate(ltmot) : ###boucle ajoutant ltmot dans un dictionnaire, avec un mot allemand en clé        
    if chx :       ###dans le cas où le mot allemand est défini, clé -> alld, valeur -> fr
        dic[alld] = mot
        chx= False
    else :         ###dans le cas où on doit définir le mot allemand
        alld = "hey"  #permet de savoir si il y a eu changements
        if mot[:4] == "der " : #si der, passage à  la fin en °der (pour un meilleur tri)
            alld = mot[4:] + "°der"
        elif mot[:4] == "die " : #même chose pour die
            alld = mot[4:] + "°die"
        elif mot[:4] == "das " : #das
            alld = mot[4:] + "°das"
        if alld is "hey" : #si aucun changement
            if mot[0].isupper() : #passage en minuscules avec # à  la fin (pour un meilleur tri)
                alld = mot.lower() + "#"
            else : #aucun changement
                alld = mot
        else :
            alld = alld.lower() + "#" #passage en minuscule si déjà  modifié par der/die/das
        alldlt.append(alld)
        chx = True

alldlt.sort() ###tri

for element in alldlt : ###tri des mots français de manière à  correspondre au tri allemand
    for fri in dic.keys():
        if element ==fri :
            frlt.append(dic[fri])
            
for i,mot in enumerate(alldlt) : ###maj & déterminant pour la liste triée
    if mot.endswith("#"):
        mot = mot[:-1].capitalize()
    if mot.endswith("°der"):
        mot = "der " + mot[:-4]
    elif mot.endswith("°die"):
        mot = "die " + mot[:-4]
    elif mot.endswith("°das"):
        mot = "das " + mot[:-4]
    alldlt[i] = mot

alldsr = "\n".join(alldlt) ###conversion en une chaîne de caractères avc saut de ligne entre chaques mots
frsr = "\n".join(frlt)

with open("A trier.txt", "w") as fichier:
    fichier.write("{}\n\n{}".format(alldsr,frsr))


try :
    rename("A trier.txt","Trié.txt")
except OSError as e :
    print("Erreur : {} - {}.".format(e.filename, e.strerror))
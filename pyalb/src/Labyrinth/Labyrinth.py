# -*-coding:utf-8 -*

from ClassesLab import *
from FuncLab import Move
from os import system
from msvcrt import getch

#a = LabTra(5,6)






SE = LabObj("┏━", tag="mur")
h = LabObj("━━", tag="mur")
SO = LabObj("━┓", tag="mur")
vO = LabObj("┃ ", tag="mur")
vE = LabObj(" ┃", tag="mur")
NE = LabObj("┗━", tag="mur")
NO = LabObj("━┛", tag="mur")
nth = LabObj("  ", tag="vide")
hey = LabObj("<■", tag="pers")




with open('carte.txt', 'r', encoding="utf8") as fichier :
    crt_str = fichier.read()

crt_split = crt_str.split("\n")
L_crt = len(crt_split)
l_crt = int(len(crt_split[0]) / 2)
a = LabTra(l_crt, L_crt)



continuer = True
l = 0
L = 0
while l != l_crt or L!= L_crt-1:
    if crt_str[0]== '\n':
        l=0
        L+=1
        crt_str = crt_str[1:]
    bloc = crt_str[:2]
    if bloc == SE.txt :#
        a[l,L] = SE
        l +=1
        crt_str = crt_str[2:]
    elif bloc == h.txt :#
        a[l,L] = h
        l +=1
        crt_str = crt_str[2:]
    elif bloc == SO.txt :#
        a[l,L] = SO
        l +=1
        crt_str = crt_str[2:]
    elif bloc == vO.txt :#
        a[l,L] = vO
        l +=1
        crt_str = crt_str[2:]
    elif bloc == vE.txt :#
        a[l,L] = vE
        l +=1
        crt_str = crt_str[2:]
    elif bloc == NE.txt :#
        a[l,L] = NE
        l +=1
        crt_str = crt_str[2:]
    elif bloc == NO.txt :#
        a[l,L] = NO
        l +=1
        crt_str = crt_str[2:]
    elif bloc == nth.txt :#
        a[l,L] = nth
        l +=1
        crt_str = crt_str[2:]
    elif bloc == hey.txt :
        a[l,L] = hey
        l +=1
        crt_str = crt_str[2:]
    else :
        raise ValueError ("la valeur ne correspond pas aux modèles")




print (a)



current_pos_x = 3
current_pos_y = 1
touche = str()

while touche != "quit":
    
    touche = getch()
    touche = touche.decode("utf-8")
    
    nouvelle_pos = Move(touche, current_pos_x, current_pos_y, a)
    a[current_pos_x, current_pos_y] = nth
    a[nouvelle_pos] = hey
    current_pos_x, current_pos_y = tuple(nouvelle_pos)
    system("cls")
    print(a)



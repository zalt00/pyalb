# -*-coding:utf-8 -*

from ClassesLab import *
from FuncLab import Move
from os import system
from msvcrt import getch

#a = LabTra(5,6)






SE = LabObj("┏", tag="mur")
h = LabObj("━", tag="mur")
SO = LabObj("┓", tag="mur")
v = LabObj("┃", tag="mur")
NE = LabObj("┗", tag="mur")
NO = LabObj("┛", tag="mur")
nth = LabObj(" ", tag="vide")
hey = LabObj("■", tag="pers")




with open('carte.txt', 'r', encoding="utf8") as fichier :
    crt_str = fichier.read()

crt_split = crt_str.split("\n")
L_crt = len(crt_split)
l_crt = int(len(crt_split[0]))
a = LabTra(l_crt, L_crt)



continuer = True
l = 0
L = 0
while l != l_crt or L!= L_crt-1:
    bloc = crt_str[0]
    if bloc == '\n':
        l=0
        L+=1
        crt_str = crt_str[1:]
    elif bloc == SE.txt :#
        a[l,L] = SE
        l +=1
        crt_str = crt_str[1:]
    elif bloc == h.txt :#
        a[l,L] = h
        l +=1
        crt_str = crt_str[1:]
    elif bloc == SO.txt :#
        a[l,L] = SO
        l +=1
        crt_str = crt_str[1:]
    elif bloc == v.txt :#
        a[l,L] = v
        l +=1
        crt_str = crt_str[1:]
    elif bloc == NE.txt :#
        a[l,L] = NE
        l +=1
        crt_str = crt_str[1:]
    elif bloc == NO.txt :#
        a[l,L] = NO
        l +=1
        crt_str = crt_str[1:]
    elif bloc == nth.txt :#
        a[l,L] = nth
        l +=1
        crt_str = crt_str[1:]
    elif bloc == hey.txt :
        a[l,L] = hey
        l +=1
        crt_str = crt_str[1:]
    else :
        raise ValueError ("la valeur ne correspond pas aux modèles")






current_pos_x, current_pos_y = a.find(hey)


touche = str()

Quitter = False


while not Quitter :
    
    system("cls")
    print("Appuyez sur la touche 'echap' pour ouvrir le menu", a, sep='\n\n')
    
    
    
    
    while touche != "\x1b" and not Quitter:
         
        touche = getch()
        touche = touche.decode("utf-8")
        if touche != "\x1b" :
            
            
            try :
                nouvelle_pos = Move(touche, current_pos_x, current_pos_y, a)
                a[current_pos_x, current_pos_y] = nth
                a[nouvelle_pos] = hey
                current_pos_x, current_pos_y = tuple(nouvelle_pos)
                system("cls")
                print("Appuyez sur la touche 'echap' pour ouvrir le menu", a, sep="\n\n")
                
                
            except IndexError:
                Quitter = True
                a[current_pos_x, current_pos_y] = nth
                system("cls")
                print("Appuyez sur la touche 'echap' pour ouvrir le menu", a, sep="\n\n")
                print("Vous avez atteint la sortie !")
                system("pause")



    if touche == "\x1b" :
        system("cls")
        print("0 - quitter\n1 - reprendre")
        chtrl = getch()
        chtrl = chtrl.decode("utf-8")
        if chtrl == "0" :
            Quitter = True
        elif chtrl == "1" :
            touche = ""
    
    
    
    
    
    
    
    
    
    

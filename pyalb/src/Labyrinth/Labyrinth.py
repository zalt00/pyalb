# -*-coding:utf-8 -*


from Modules.FuncLab import * #ce module a besoin d'importer les autres pour fonctionner, importer ClassLab et VarLab une deuxième fois serait inutile
from os import system
from msvcrt import getch
from glob import glob
from pickle import Pickler, Unpickler

try :
    with open("Données/save", "rb") as fichier :
        my = Unpickler(fichier)
        score_dict = my.load()
except Exception :
    score_dict = {}



cartes = glob("cartes/*") ###toutes les cartes sont mises dans un dictionnaire (crt_str_in2dict)
        
        
crt_str_in2dict = dict()
for crt in cartes :
    with open(crt, 'r', encoding="utf8") as fichier :
        crt_str_in2dict[crt] = fichier.read()



for name, crt_str in crt_str_in2dict.items():
    crt_split = crt_str.split("\n")
    L_crt = len(crt_split)
    l_crt = int(len(crt_split[0]))
    crt_str_in2dict[name] = (crt_str, l_crt, L_crt) 

crt_toprint = [ele[7:-4] for ele in cartes]




quit_game = False

while not quit_game : #boucle globale, menu principal
    #system("cls")
    
    print("Le Labyrinth\n", "'entr\u00E9e' - jouer", "'echap' - quitter le jeu", "'espace' - option des sauvegardes", sep="\n")
    play = getch()
    system("cls")
    
    
    if play == b"\r" :
        
        
       
        
        dis = False
        while not dis:
            print("cartes disponibles : {}".format(crt_toprint[0]), *crt_toprint[1:], sep=", ")
            chs_name = input("choisir une carte : ")
            chs_name = 'cartes\\{}'.format(chs_name)
            if not chs_name.endswith('.txt') :
                chs_name += '.txt'
            if chs_name in crt_str_in2dict:
                dis = True
            else :
                print("\nErreur - nom '{}' invalide\n".format(chs_name))
            
            
            
        tpl_err_a = Parseur(crt_str_in2dict[chs_name][0], crt_str_in2dict[chs_name][1], crt_str_in2dict[chs_name][2])
        
        a = tpl_err_a[0]
        err = tpl_err_a[1]
        
        
        
        
        
        
        
        
        try :
            
            current_pos_x = int(score_dict[chs_name][0])
            current_pos_y = int(score_dict[chs_name][1])
            
            system('cls')
            print("Reprendre partie existante ?\n\n0 - Oui\n1 - Non")
            reprendre = getch()
            
            assert(reprendre == b"0")
            
            pos_x_tormv, pos_y_tormv  = a.find(hey)
            a[pos_x_tormv, pos_y_tormv] = nth
            
            a[current_pos_x, current_pos_y] = hey
            
        except Exception :
            current_pos_x, current_pos_y = a.find(hey)
        
        touche = str()
        
        Quitter = False
        
        while not Quitter : #boucle de jeu
            
            system("cls")
            print("Appuyez sur la touche 'echap' pour ouvrir le menu\n", *err, a, sep='\n')
            
            
            
            
            while touche != b"\x1b" and not Quitter: #boucle en jeu
                 
                touche = getch()
                
                if touche != b"\x1b" :
                    
                    
                    try :
                        nouvelle_pos = Move(touche, current_pos_x, current_pos_y, a)
                        a[current_pos_x, current_pos_y] = nth
                        a[nouvelle_pos] = hey
                        current_pos_x, current_pos_y = tuple(nouvelle_pos)
                        system("cls")
                        print("Appuyez sur la touche 'echap' pour ouvrir le menu\n", *err, a, sep="\n")
                        
                        
                    except IndexError:
                        Quitter = True
                        a[current_pos_x, current_pos_y] = nth
                        try :
                            del (score_dict[chs_name])
                        except KeyError :
                            print("Erreur - sauvegarde inexistante")
                        finally :
                            system("cls")
                            print("Appuyez sur la touche 'echap' pour ouvrir le menu\n", *err, a, sep="\n")
                            print("Vous avez atteint la sortie !\nAppuyez sur n'importe quelle touche pour revenir au menu principal")
                            getch()
        
        
        
            if touche == b"\x1b" : #menu en jeu
                system("cls")
                print("0 - sauvegarder et revenir au menu principal\n1 - reprendre")
                chtrl = getch()
                
                if chtrl == b"0" :
                    score_dict[chs_name] = (current_pos_x, current_pos_y)
                    Quitter = True
                else :
                    touche = b""
    
    
    
    
    
    
    
    elif play == b" " :
        
        
        if score_dict == {} :
            

            print("Aucune sauvegarde trouv\u00E9e.\n\nAppuyez sur n'importe quelle touche pour revenir au menu...")
            getch()
            
            
        else :
            
            print("Sauvegardes existantes :\n")
        
            toprt = list(score_dict.items())
            toprt = [(k[7:-4],j) for k,j in toprt]
            print(*toprt, "\ns - supprimer une sauvegarde", "autre - retour au menu", sep = "\n")
            sup = getch()
        
            if sup == b"s" :
                
                system("cls")
                print("Sauvegardes existantes :\n", *toprt, "Entrez le nom de la sauvegarde \u00E0 supprimer : ", sep="\n")
                tormv = input()
                try :
                    del(score_dict["cartes\\{}.txt".format(tormv)])
                    print("Sauvegarde supprim\u00E9e avec succ\u00E8s.\n\nAppuyez sur n'importe quelle touche pour revenir au menu...")
                except KeyError :
                    print("Erreur - la sauvegarde {} n'exixte pas\n\nAppuyez sur n'importe quelle touche pour revenir au menu...".format(tormv))
                getch()
                
                
                
                
    
    elif play == b"\x1b" : #quitter
        system("cls")
        print("Quitter le jeu ?\n", "0 - oui", "1 - non", sep="\n")
        quit_confirmation = getch()
        
        if quit_confirmation == b"0" :
            quit_game = True








with open("Données/save", "wb") as fichier :
        my = Pickler(fichier)
        my.dump(score_dict)
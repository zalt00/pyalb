# -*-coding:utf-8 -*


'''
Created on 23 oct. 2018

@author: Timelam
'''

try :
    from Modules.ClassesLab import *
    from Modules.VarLab import *
except :
    from ClassesLab import *
    from VarLab import *





def Move(direction, pos_obj_x, pos_obj_y, tab):
    
    if direction == b"z" :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y - 1
    elif direction == b"d" :
        nxt_pos_x = pos_obj_x + 1
        nxt_pos_y = pos_obj_y
    elif direction == b"s" :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y + 1
    elif direction == b"q" :
        nxt_pos_x = pos_obj_x - 1
        nxt_pos_y = pos_obj_y
    else :
        nxt_pos_x = pos_obj_x
        nxt_pos_y = pos_obj_y
        
    if tab[nxt_pos_x, nxt_pos_y].tag == "mur":
        return (pos_obj_x, pos_obj_y)
    else :
        return (nxt_pos_x, nxt_pos_y)
        


###########################################


def Parseur(crt_str, l_crt, L_crt):
    
    
    
    """fonction parcourant une chaine de caracteres et qui renvoie un tableau ; prend en para la chaine et les dimensions l puis L du tableau"""
    
    
    
    
    

    
    a = LabTra(l_crt, L_crt)

    err = []
    l = 0
    L = 0
    while l != l_crt or L!= L_crt-1:
        try :
            bloc = crt_str[0]
        except IndexError:
            err.append(ValueError ("Erreur - \u00E9diteur de texte invalide"))
            bloc = " "
        if bloc == '\n':
            l=0
            L+=1
            crt_str = crt_str[1:]
        else :
            
            continuer = True
            i = 0
            while continuer :
                if modeles[i].txt == bloc:
                    a[l,L] = modeles[i]
                    l +=1
                    crt_str = crt_str[1:]
                    continuer = False
                
                elif len(modeles)-1 == i :
                    err.append(ValueError ("Erreur - la valeur '{}' ne correspond pas aux modèles".format(bloc)))
                    a[l,L] = nth
                    l +=1
                    crt_str = crt_str[1:]
                    continuer = False
                else :
                    i +=1
            
            

    return (a, err)


















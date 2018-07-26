# -*-coding:Latin-1 -*

def div(a):
    """fonction renvoyant la liste des diviseurs d'un nomhre mis en paramètre"""
    liste= []
    i = 0
    while i != a :
        i += 1
        if a % i == 0 :
            liste += [i]
    return(liste)

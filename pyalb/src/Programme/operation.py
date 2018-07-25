
def div(a) :    
    i = 0
    liste = []
    
    while len(liste) <= a :
        liste += [len(liste)]
    
    liste.remove(0)
    
    while len(liste) != i :
        if a % liste[i] == 0 :
            i +=1
        else :
            del(liste[i])
    
    return(liste)
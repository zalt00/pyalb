# -*-coding:Latin-1 -*

from Test import operation

c=0
while str(c) != "quit" :    
    c = input("Saisir un nombre : ")
    try :
        operation.div(int(c), 0)
    except :
        if str(c) == "quit" :
            print ("Au revoir")
        else :
            print("Valeur incorrecte, réessayez")
    



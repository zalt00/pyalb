# -*-coding:Latin-1 -*
import math
from random import randrange

b=0
d=40 #argent

while d != 0 :
    print("vous avez ",d, "$")
    a = int(input("Numero sur lequel parier : ")) #num    
    b = int(input("Mise : ")) #Mise
    if b>d :
        print("Mise supérieure à votre argent")
    else :    
        c = randrange(50) #aléa

        print("le numéro est : ",c)

        if c == a :
            d += b
            print("vous avez gagné ",b, "$")
        elif a % 2 == c % 2 :
                d += math.ceil(b / 2)
                print("vous avez gagné", math.ceil(b/2), "$")
        else :
            d -= b
            print("vous avez perdu", b, "$")
            
print("Vous n'avez plus d'argent !")
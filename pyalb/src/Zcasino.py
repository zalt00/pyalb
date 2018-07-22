# -*-coding:Latin-1 -*
import math
from random import randrange

a=0
b=0
c=0
d=1000 #argent

while d != 0: #boucle, arrête quand le joueur n'a plus d'argent
    
    print("vous avez ",d, "$") #argent actuel
    
    a = int(input("Numero sur lequel parier : ")) #numéro
    if a>49 or a<0 : #test de convenabilité du numéro
        print("le numéro doit être compris entre 0 et 49 inclus") #erreur sur ce test, vers fin de boucle
    else : #aucune erreur , continuation du programme
        
        b = int(input("Mise : ")) #Mise
        if b>d or b<0: #test de convenabilité de la mise
            print("La mise ne doit pas être supérieure à votre argent, ni inferieur à 0") #erreur sur ce test, vers fin du programme  
        else :    #aucune erreur, continuation du programme
            
            c = randrange(50) #aléa
    
            print("le numéro est : ",c) #affichage du numéro gagnant
    
            if c == a : #prime 25x
                d += b*25
                print("vous avez gagné ",b*25, "$")
                
            elif a % 2 == c % 2 : #prime 1,5
                    d += math.ceil(b / 2)
                    print("vous avez gagné", math.ceil(b/2), "$")
                    
            else : #perdu
                d -= b
                print("vous avez perdu", b, "$")
            
#fin de boucle
print("Vous n'avez plus d'argent !")
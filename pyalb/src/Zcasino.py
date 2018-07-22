# -*-coding:Latin-1 -*

from random import randrange

a = int(input("Numero sur lequel parier : "))
b = int(input("Mise : "))
c = randrange(50)
print("le numéro est : ",c)

if c == a :
    b *= 2
    print("vous avez gagné ",b, "$")
elif a % 2 == c % 2 :
    print("todo2")
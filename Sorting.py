# -*-coding:utf-8 -*

class Sorting :
    
    """tpl est un tuple contenant mot allemand, mot français ;
    si ll alors langue : alld sinon fr ;
    attribut tr est une chaine de caracteres sans article et Maj, avc que la mot de la langue choisie."""
    
    
    def __init__(self, tpl, ll = True) :
        
        
        tpl = tuple(tpl)
        self.bs = tpl
        
        _i= 0
        _keep=True
        
        if ll:
            tt = ["der ", "die ", "das "]
            _a = 0
            
        else :
            tt = ["la ", "le ", "l'", "l’"]
            _a = 1
        
        while _keep:
                le = len(tt[_i])
                if str(tpl[_a]).casefold()[:le] == tt[_i] :
                    self.tr = str(tpl[_a]).casefold()[le:]
                    _keep = False
                
                else :
                    self.tr = str(tpl[_a]).casefold()
                
                if _i == len(tt)-1 :
                    _keep = False
                
                _i += 1



##### FIN DE CLASSE #####



from operator import attrgetter
from os import system, rename
from glob import glob as glb


fch = glb("Results/*")

if not "Results\\To be sorted.txt" in fch :
    with open("Results/To be sorted.txt", "w") as fichier:
        print ("- File successfully created -")

print("\n\nPaste your text into the file named \"To be sorted.txt\" in the folder \"Results\"")
print("Then choose the language that the program will sort : 'fr' (French) or 'ge' (German)")
print("Finally, press enter. If the program closes, something wrong happened.\n")
chtrl = input("Select your language :")

fichier = open("Results/To be sorted.txt", "r")
fichier_txt = fichier.read()
fichier.close()
lt = fichier_txt.split("\n")


err = False
while not err:
    try :
        lt.remove("")
    except :
        err = True


alld = str()
lt_tosort = list()
ctn = False
for mot in lt :
    if ctn :
        a = (alld, mot)
        lt_tosort.append(a)
        ctn = False
    else :
        alld = mot
        ctn = True


if chtrl == "fr" : 
    lt_tosort = [Sorting(c, ll = False) for c in lt_tosort]
else :
    lt_tosort = [Sorting(c) for c in lt_tosort]


lt_tosort.sort(key=attrgetter('tr'))
lt_sorted = [tuple(f.bs) for f in lt_tosort]

alldlt=list()
frlt = list()

for element in lt_sorted :
    alldlt.append(element[0])
    frlt.append(element[1])


lt_sorted = "\n".join(alldlt) + "\n\n" + "\n".join(frlt)

with open("Results/Sorted.txt", "w") as fichier:
    fichier.write(lt_sorted)
    print ("- File successfully sorted -")

print("The text has been sorted in the file \"Sorted\"\n")
z = input("Do you want to rename this file or quit? (rename/quit) : ")

if z == "rename" :
    new_name = input("Write the new name (don't write .txt at the end) : ")
    rename("Results/Sorted.txt","Results/{}".format(new_name + ".txt"))
    print ("\n- File successfully renamed -")
    system("pause")
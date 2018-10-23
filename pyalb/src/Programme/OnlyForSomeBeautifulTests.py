class Gens :
    
    def __init__(self, prenom, nom):
        
        self.nom = nom
        self.prenom = prenom
        self._age = 14
    
    
    def _get_age(self):
        
        return self._age
    
    
    def _set_age(self, new_age):
        
        self._age = new_age
    
    
    age = property(_get_age, _set_age)



moi = Gens("Amedee", "Le Berre")

print(moi.age)
print(moi.nom)
print(moi.prenom)

moi.nom = "Le Berre"
moi.age = 45
print(moi.age)
print(moi.nom)









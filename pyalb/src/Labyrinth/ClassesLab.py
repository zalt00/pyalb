# -*-coding:utf-8 -*

'''
Created on 22 oct. 2018

@author: Timelam
'''






#########################################################################################################################
class LabTra :
    
    
    
    def __init__(self, l, L):
        
        self.tra = list()
        _l = list()
        self.l = l
        self.L = L
        
        while l > 0 : ###largeur
            _l.append(None)

            l -= 1

        
        
        while L > 0 : ###creation du terrain
            self.tra.append(_l)

            L -= 1
        
        ### x est dans y, x,y
        ### l horizontal, L vertical
        
    
    
    
    
    def __str__(self):
        
        
        tra = list(self.tra)
        
        for i,ele in enumerate(tra) :
            st = str()
            for eleb in ele :
                st += str(eleb)
            tra[i] = st
            
        
        
        
        ReprnStr = '\n'.join(tra)
        
        return ReprnStr
    
    
    
    
    
    def __setitem__ (self, p, obj):
        
        x = p[0]
        y = p[1]
        
        largeurs = list(self.tra[y])
        
        largeurs[x] = obj
        self.tra[y] = largeurs
    
    
    
    
    
    
    def __getitem__ (self, p):
        
        return self.tra[p[1]][p[0]]
    
    
    
    
    def __iter__ (self):
        
        tortn = list()
        for ele in self.tra :
            for eleb in ele :
                tortn.append(eleb)
        return iter(tortn)
    
    
    
    
    
    def pos(self):
        
        tortn = list()
        for L, ele in enumerate(self.tra) :
            for l, eleb in enumerate(ele) :
                tortn.append((l, L, eleb))
        return tortn
    
    
    
    
    def find(self, obj):
        
        for l, L, ele in self.pos() :
            if ele is obj :
                return l, L
        
        
        
        
    def __contains__(self, obj):
        
        for a in self:
            
            if a == obj :
                return True
        return False
#########################################################################################################################













#########################################################################################################################
class LabObj :
    
    
    def __init__(self, txt, tag):
        
        self.txt = txt
        self.tag = tag
    
    
    
    def __str__(self):
        
        return str(self.txt)





















# -*-coding:utf-8 -*

class OrgDict :
    
    """dictionnaire ordonne"""


    def __init__(self, dic={}, **args):
        
        cle = []
        val = []
        
        if args != {} :
            dic = dict(args)
        
        for a, b in dic.items():
            cle.append(a)
            val.append(b)
        
        self.cle = cle
        self.val = val
        
        
    def __getitem__(self, i):
        
        
        for k,v in enumerate(self.cle):
            if v == i:
                return self.val[k]
    
    
    def __setitem__(self, i, valeur):
        
        find = False
        for k,v in enumerate(self.cle) :
            if v == i :
                self.val[k] = valeur
                find = True
        
        if not find :
            self.cle.append(i)
            self.val.append(valeur)
    
    
    def __delitem__(self, i):
        
        for k,v in enumerate(self.cle) :
            if v == i :
                del (self.cle[k])
                del (self.val[k])
    
    
    
    
    def keys(self):
        
        return self.cle
    
    
    def values(self):
        
        return self.val
    
    
    def items(self):
        
        i = 0
        lt = list()
        while i != len(self.cle) :
            lt.append((self.cle[i], self.val[i]))
            i += 1
        return lt
    
    
    
    
    def __str__(self):
        
        str_dic = "{"
        for a,b in self.items() :
            if str_dic != "{":
                str_dic += ', '
            str_dic += "%s : %s" % (repr(a),repr(b))
        str_dic += "}"
        return str_dic
    
    
    
    
    def __contains__(self, i):
        
        return i in self.cle
    
    
    
    
    def __len__(self):
        
        return len(self.cle)
    
    
    
    def sort(self, key = None, reverse = False):
        

        clesr = list(self.cle)
        clesr.sort(key = key, reverse = reverse)
        vlsr = list()
        
        for a in clesr :
            for i,b in enumerate(self.cle) :
                if b == a:
                    vlsr.append(self.val[i])
        
        self.cle = list(clesr)
        self.val = list(vlsr)
    
    
    
    
    def __iter__(self):
        
        return iter(self.cle)
    
    
    
    
    def __iadd__(self, diio):
        
        for ele, eleb in diio.items():
            self.cle.append(ele)
            self.val.append(eleb)

        return self
        
    def __add__(self, dio):
        
        dic = dict()
        for k,v in self.items() :
            dic[k] = v
        for k,v in dio.items() :
            dic[k] = v
        return OrgDict(dic)
    

    
    
    
    
    

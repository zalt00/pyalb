def div(b, a=0):
    """fonction affichant l'ensemble des diviseurs d'un nombre"""
    while a != b :
        a += 1
        if b % a == 0 :
            print(a)
            
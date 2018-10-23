# -*-coding:utf-8 -*

from ClassesLab import *

a = LabTra(5,6)

SE = "┏━"
h = "━━"
SO = "━┓"
vO = "┃ "
vE = " ┃"
NE = "┗━"
NO = "━┛"
nth = "  "
hey = "<>"

if False :
    a[0,0] = "┏"
    a[1,0] = "━━━"
    a[2,0] = "┓  "
    a[0,1] = "┃"
    a[1,1] = " 0 "
    a[2,1] = "┃"
    a[0,2] = "┗"
    a[1,2] = "━━━"
    a[2,2] = "┛"

a[0,0] = SE
a[1,0] = h
a[2,0] = h
a[3,0] = h
a[4,0] = SO
a[0,1] = vO
a[1,1] = nth
a[2,1] = nth
a[3,1] = hey
a[4,1] = vE
a[0,2] = NE
a[1,2] = h
a[2,2] = SO
a[3,2] = nth
a[4,2] = vE
a[0,3] = SE
a[1,3] = h
a[2,3] = NO
a[3,3] = nth
a[4,3] = vE
a[0,4] = vO
a[1,4] = nth
a[2,4] = nth
a[3,4] = nth
a[4,4] = vE
a[0,5] = NE
a[1,5] = h
a[2,5] = h
a[3,5] = h
a[4,5] = NO
print (a)

from os import system
system("pause")

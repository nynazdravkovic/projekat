

# -*- coding: utf-8 -*-
"""
Created on Thu May 10 23:41:01 2018

@author: nina
"""
import random
import numpy
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import json
from math import sqrt

brojJedinki=100
brojCiklusa=100
koeficijentKrosovera=0.05
brojGeneracija=1000
cc=3
cd=0
dc=5
dd=1
razliciteStrategije=64
matrica= numpy.zeros([brojGeneracija,64], dtype=int)
strategije=list(range(0,63))


    

def bit (broj, m):
    a=((1<<m) & broj)>>m
    return a



def birajClan(niz, peti, sesti):
    if peti==0:
        if sesti==0:
            clan=bit(niz,5)
        else:
            clan=bit(niz,4)
    else:
        if sesti==0:
            clan=bit(niz,3)
        else:
            clan=bit(niz,2)
    return clan



def svakaSaSvakom():#pravim praznu matricu poena
    populacija1=[]
    matricaPoena=numpy.zeros([64,64], dtype=int)
    for i in range (64): #pravim strategije
        populacija1.append(i)
    istorijaSukoba = numpy.zeros([64,64], dtype=int)
    for j1 in range(64):
        for j2 in range(j1, 64):
            for x in range(brojCiklusa):
                if x==0:
                    petij1=bit(populacija1[j1],1)
                    sestij1=bit(populacija1[j1],0)
                    petij2=bit(populacija1[j2],1)
                    sestij2=bit(populacija1[j2],0)
                    
                else:
                    petij1=istorijaSukoba[j1][j2]
                    petij2=istorijaSukoba[j2][j1]
                    sestij1=petij2
                    sestij2=petij1
                clan1=birajClan(populacija1[j1], petij1, sestij1)
                clan2=birajClan(populacija1[j2], petij2, sestij2)
                istorijaSukoba[j1][j2]=clan1
                istorijaSukoba[j2][j1]=clan2                
                
                if (clan1==1):
                    if (clan2==1):
                        if j1!=j2:
                            matricaPoena[j1][j2]=matricaPoena[j1][j2]+cc
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+cc
                        else:
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+cc
                        
                    else:
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+cd
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+dc

                else:
                    if (clan2==1):
                        matricaPoena[j1][j2]=matricaPoena[j1][j2]+dc
                        matricaPoena[j2][j1]=matricaPoena[j2][j1]+cd
                    else:
                        if j1!=j2:
                            matricaPoena[j1][j2]=matricaPoena[j1][j2]+dd
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+dd
                        else:
                            matricaPoena[j2][j1]=matricaPoena[j2][j1]+dd
    return (matricaPoena)
    


def kreirajPopulaciju():
    for x in range(37):
        strategije.append(random.choice(strategije))
    return (strategije)

def dodavanjePoena(pop):
    poeni=numpy.zeros(brojJedinki)
    for i1 in range (brojJedinki):
        for i2 in range (i1, brojJedinki):
            a = pop[i1]
            b = pop[i2]
            poeni[i1]=poeni[i1] + matricaPoena[a][b]
            poeni[i2]=poeni[i2] + matricaPoena[b][a]
    return(poeni)


def razmnozavanje(poeni,pop):
    #lpoeni=list(poeni)
    populacija2=deepcopy(pop)
    populacija2=[x for _, x in sorted(zip(poeni,populacija2))]
    populacija2=populacija2[::-1]
    poeni=sorted(poeni)
    lpoeni=poeni[::-1]
    for n in range (5):
        populacija2.append(populacija2[n])
        lpoeni.append(poeni[-n])
    populacija2=[x for _, x in sorted(zip(lpoeni,populacija2))]
    populacija2=populacija2[5:]
    pop=deepcopy(populacija2)
    return (pop)


def mutacije(pop,koef):
    for i in range (brojJedinki):
        a=random.uniform(0,1)
        if a<=koef:
            b=random.randint(0,5)#random prelomno mesto
            pop[i]=pop[i]^(1<<b)
    return(pop)

def krosover(pop):
    for i in range (brojJedinki):
        g=random.uniform(0,1)
        if g<=koeficijentKrosovera:
                a=random.randint(0,brojJedinki-1)  
                b=random.randint(0,brojJedinki-1)
                c=random.randint(0,6)  #biramo mesto na kome se lome strategije  
                mask=(1<<(c+1))-1
                donji1=pop[a] & mask
                donji2=pop[b] & mask
                gornji1=pop[a]-donji1
                gornji2=pop[b]-donji2
                pop[a]=gornji1+donji2
                pop[b]=gornji2+donji1
    return(pop)

def column(matrix, k):
    return [row[k] for row in matrix]


def genetskiAlgoritam(koef, matrica,f): 
    vreme=list(range(0,brojGeneracija))
    populacija=kreirajPopulaciju()
    nizSrednjihPoena=[]
    #minOdstupanje=7000
    for t in range (brojGeneracija):
        poeni=dodavanjePoena(populacija)
        populacija=razmnozavanje(poeni,populacija)
        populacija=mutacije(populacija,koef)
#        print(populacija)
        populacija=krosover(populacija)
        nizSrednjihPoena.append (numpy.mean(poeni)/(99*brojCiklusa))                
        for k in range (brojJedinki):
            for i in range (0,64):
                if populacija[k]==i:
                    matrica[t][i][f]=matrica[t][i][f]+1
        matrica[t][0][f]+=matrica[t][1][f]+matrica[t][2][f]+matrica[t][3][f]+matrica[t][4][f]+matrica[t][5][f]+matrica[t][6][f]+matrica[t][8][f]+matrica[t][9][f]+matrica[t][11][f]+matrica[t][12][f]+matrica[t][13][f]
        #matrica[t][0]=matrica[t][0]/12
        #grupa1
        matrica[t][16][f]=(matrica[t][16][f]+matrica[t][18][f]+matrica[t][19][f])#/3
        matrica[t][58][f]=(matrica[t][58][f]+matrica[t][57][f]+matrica[t][56][f])#/3
        #grupa2
        matrica[t][15][f]=(matrica[t][15][f]+matrica[t][14][f])#/2
        #tft
        matrica[t][21][f]=(matrica[t][21][f]+matrica[t][23][f])#/2
        matrica[t][41][f]=(matrica[t][41][f]+matrica[t][43][f])#/2
        #gtft
        matrica[t][52][f]=(matrica[t][52][f]+matrica[t][53][f]+matrica[t][55][f])#/3
        matrica[t][33][f]=(matrica[t][34][f]+matrica[t][35][f]+matrica[t][33][f])#/3
        #grupa3
        matrica[t][20][f]=(matrica[t][20][f]+matrica[t][22][f])#/2
        matrica[t][59][f]=(matrica[t][59][f]+matrica[t][40][f])#/2
        #grupa5
        matrica[t][24][f]=(matrica[t][24][f]+matrica[t][27][f])#/2
        matrica[t][42][f]=(matrica[t][42][f]+matrica[t][26][f])#/2
        #grupa4
        #pavlov
        matrica[t][36][f]=(matrica[t][36][f]+matrica[t][39][f]+matrica[t][26][f])#/3
        matrica[t][25][f]=(matrica[t][25][f]+matrica[t][37][f]+matrica[t][38][f])#/3
        #flipflop
        matrica[t][48][f]=(matrica[t][48][f]+matrica[t][49][f])#/2
        matrica[t][50][f]=(matrica[t][50][f]+matrica[t][51][f])#/2
        matrica[t][63][f]=(matrica[t][63][f]+matrica[t][15][f]+matrica[t][62][f]+matrica[t][30][f]+matrica[t][31][f]+matrica[t][61][f]+matrica[t][29][f]+matrica[t][60][f]+matrica[t][44][f]+matrica[t][46][f]+matrica[t][47][f]+matrica[t][14][f])#/12
        matrica[t][1][f]=0
        matrica[t][2][f]=0   
        matrica[t][3][f]=0
        matrica[t][4][f]=0
        matrica[t][5][f]=0
        matrica[t][6][f]=0
        matrica[t][8][f]=0
        matrica[t][9][f]=0
        matrica[t][11][f]=0
        matrica[t][12][f]=0
        matrica[t][13][f]=0
        matrica[t][14][f]=0
        matrica[t][15][f]=0
        matrica[t][19][f]=0
        matrica[t][18][f]=0
        matrica[t][22][f]=0
        matrica[t][23][f]=0
        matrica[t][27][f]=0
        matrica[t][29][f]=0
        matrica[t][30][f]=0
        matrica[t][31][f]=0
        matrica[t][34][f]=0
        matrica[t][35][f]=0
        matrica[t][37][f]=0
        matrica[t][38][f]=0
        matrica[t][39][f]=0
        matrica[t][42][f]=0
        matrica[t][43][f]=0
        matrica[t][44][f]=0
        matrica[t][46][f]=0
        matrica[t][47][f]=0
        matrica[t][49][f]=0
        matrica[t][51][f]=0
        matrica[t][53][f]=0
        matrica[t][55][f]=0
        matrica[t][57][f]=0
        matrica[t][58][f]=0
        matrica[t][60][f]=0
        matrica[t][61][f]=0
        matrica[t][62][f]=0           
##ovde se plotuje histogram poena 
#    plt.hist(poeni/ (99*brojCiklusa))
#    plt.ylabel('Broj jedinki')
#    plt.xlabel('Poeni')
#    plt.title('Grafik zastupljenosti poena u generaciji')
#    plt.show()
    #k=numpy.rot90(matrica)
    return nizSrednjihPoena, matrica



def sve(koeficijentMutacije):
    srednja=[]
    o=list(range(64))
    matricaZastupljenosti= numpy.zeros([brojGeneracija,64,10], dtype=int)
    a1=numpy.zeros([brojGeneracija,64], dtype=int)
    b1=numpy.zeros([brojGeneracija,64], dtype=int)
    vreme=list(range(brojGeneracija))
    for x in range (10):
        k=x
        s=[]
        s1=[]
        g=genetskiAlgoritam(koeficijentMutacije, matricaZastupljenosti,k) 
        #prviMinimum=-1
        matrica=g[1]
        srednjaVrednost=g[0]
        srednja.append(srednjaVrednost)
        
    numpy.rot90(srednja,3)
    for x in range (brojGeneracija):
        n=column(srednja,x)
        m=numpy.mean(n)
        m1=numpy.std(n)/sqrt(10)
        s.append(m)
        s1.append(m1)
    plt.plot(vreme,s)
    plt.errorbar(vreme, s, s1)
    axes = plt.gca()
    axes.set_ylim([0,5])
    plt.ylabel('Srednji poeni')
    plt.xlabel('Generacija')
    plt.title('Grafik srednjih poena po generaciji')
    plt.show()
    for x in range (brojGeneracija):
        for y in range (64):
            a=numpy.mean(matrica[x][y])
            b=numpy.std(matrica[x][y])/sqrt(10)
            a1[x][y]=a
            b1[x][y]=b
    plt.bar(o,a1[brojGeneracija-1])
    plt.ylabel('Zastupljenost strategije')
    plt.xlabel('Različite stretgije')
    plt.title('Grafik zastupljenosti strategija u posledjoj generaciji')
    plt.show()
    for i in range (64):
        plt.plot(vreme,column(a1,[0]),label='uvek izdaj')
        plt.errorbar(vreme,column(a1,[0]),column(b1,[0]))
    #    plt.gca().legend('uvek izdaj')
#        plt.plot(vreme,column(a1,[15]))
#        plt.errorbar(vreme,column(a1,[15]),column(b1,[15]))
    #    plt.gca().legend('grupa 1')
#        plt.plot(vreme,column(a1,[16]))    
#        plt.errorbar(vreme,column(a1,[16]),column(b1,[16]))
    #    plt.gca().legend('grupa 2')
#        plt.plot(vreme,column(a1,[20]))
#        plt.errorbar(vreme,column(a1,[20]),column(b1,[20]))
    #    plt.gca().legend('grupa 3')
        plt.plot(vreme,column(a1,[21]), label='TFT')    
        plt.errorbar(vreme,column(a1,[21]),column(b1,[21]))
    #    plt.gca().legend('TFT')
#        plt.plot(vreme,column(a1,[24]))
#        plt.errorbar(vreme,column(a1,[24]),column(a1,[24]))
    #    plt.gca().legend('grupa 5')
        plt.plot(vreme,column(a1,[25]), label='pavlov')
        plt.errorbar(vreme,column(a1,[25]),column(b1,[25]))
    #    plt.gca().legend('Pavlov')
        plt.plot(vreme,column(a1,[33]), label='GTFT')
        plt.errorbar(vreme,column(a1,[33]),column(b1,[33]))
    #    plt.gca().legend('GTFT')
        plt.plot(vreme,column(a1,[36]), label='pavlov')
        plt.errorbar(vreme,column(a1,[36]),column(b1,[36]))
    #    plt.gca().legend('Pavlov')
        plt.plot(vreme,column(a1,[41]), label='TFT' )
        plt.errorbar(vreme,column(a1,[41]),column(b1,[41]))
    #    plt.gca().legend('TFT')
#        plt.plot(vreme,column(a1,[42]))
#        plt.errorbar(vreme,column(a1,[42]),column(b1,[42]))
    #    plt.gca().legend('grupa 5')
        plt.plot(vreme,column(a1,[48]),label='flip flop')
        plt.errorbar(vreme,column(a1,[48]),column(b1,[48]))
    #    plt.gca().legend('flip flop')
        plt.plot(vreme,column(a1,[50]),label='flip flop')
        plt.errorbar(vreme,column(a1,[50]),column(b1,[50]))
    #    plt.gca().legend('flip flop')
        plt.plot(vreme,column(a1,[52]),label='GTFT')    
        plt.errorbar(vreme,column(a1,[52]),column(b1,[52]))
    #    plt.gca().legend('GTFT')
#        plt.plot(vreme,column(a1,[58]))
#        plt.errorbar(vreme,column(a1,[58]),column(b1,[58]))
    #    plt.gca().legend('grupa 1')
#        plt.plot(vreme,column(a1,[59]))
#        plt.errorbar(vreme,column(a1,[59]),column(b1,[59]))
    #    plt.gca().legend('grupa 3')
        plt.plot(vreme,column(a1,[63]),label='uvek saradjuj')    
        plt.errorbar(vreme,column(a1,[63]),column(b1,[63]))
    #    plt.gca().legend('uvek sarađuj')

#        putanja=(r'C:\Users\nina\Desktop\projekat2018\svaka1\grafik')
#        b=putanja + str(i) + '.jpg'
#        ''.join(b)   ￼
#    plt.gca().legend([ 'uvek izdaj','tft','Pavlov','gtft','Pavlov','tft','flip flop','flip flop','gtft', 'uvek sarađuj' ],loc='lower right', ncol = 2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel('zastupljenst u drustvu [%]')
    plt.xlabel('t [generacija]')
    plt.title('Grafik zastupljenosti srategija po generaciji')
#    print('radim')
    plt.savefig(r'C:\Users\nina\Desktop\projekat2018\greskapojedinacno')
    plt.show()
    
#    for x in range (brojGeneracija):
#        plt.plot(vreme,column(a1,[x]))
#        plt.errorbar(vreme,column(a1,[x]),column(b1,[x]))
#    axes = plt.gca()
#    axes.set_ylim([0,5])
#    plt.ylabel('poeni jedinki')
#    plt.xlabel('Generacija')
#    plt.title('Grafik poena strategija po generaciji')
#    plt.show()
    
matricaPoena=svakaSaSvakom()    


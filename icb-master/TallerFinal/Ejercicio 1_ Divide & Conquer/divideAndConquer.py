# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 08:34:48 2020

@author: sol
"""

import math
import time
import random
import matplotlib.pyplot as plt
import numpy as np


"""PUNTO 1"""

def listaDePuntos(fn):
    arch_entrada = fn[0]
    with open(arch_entrada, 'r') as entrada:  # Abre los archivos de entrada (en modo R:Read) y el de salida (en modo W:Write)
        lineaDeEntrada=[]
        for linea in entrada:
            linea = linea.strip('\n')       # Elimina el salto de línea del final
            linea=linea.split(' ')
            coord = (float(linea[0]),float(linea[1]))           
            lineaDeEntrada.append(coord) # Se agrega la lista de campos de la línea a la lista de líneas completa
    return lineaDeEntrada


"""PUNTO 2"""

def distancia(a,b):
    '''Mide distancia entre dos puntos'''
    return (math.sqrt( ((a[0]-b[0])**2)+ ((a[1]-b[1])**2)) )

def distanciaMinima(l):
    '''fuerza bruta: devuelve distancia mínima y los puntos a que corresponde'''
    p=l[0]
    q=l[1]
    m=distancia(p,q)
    #si "a" tiene dos valores, hallar distancia
    if len(l)==2:
        dist=distancia(l[0],l[1])
        if dist<m:
            p,q=l[0],l[1]
            m=dist
    #si hay más de dos puntos, buscar distancia entre todos y compararlos con el menor valor enontrado 
    #hasta entonces
    else:
        for x in range(0,len(l)-1):
            for y in range (x+1, len(l)):
                if m>distancia(l[x],l[y]):
                    m=distancia(l[x],l[y])
                    p,q = l[x],l[y]        
    return m,p,q


"""PUNTO 3"""

def franjaMasCercana(franja, d):   
    '''Una función auxiliar para buscar la distancia entre los puntos mas cercanos de una franja'''
    val_min = d   # iniciamos con el minimo valor como d
      # tomamos todos los puntos y probamos los proximos puntos
    #hasta que la diferencia entre coordanadas 'y' sea mas chica que d
    franja.sort(key = lambda val: val[1])    #ordanamos en y
    for i in range(len(franja)): 
        j = i + 1
        while j < len(franja) and (franja[j][1] - franja[i][1]) < val_min: 
            val_min = distancia(franja[i], franja[j]) 
            j += 1
    return val_min

def aux(l): 
    '''funcion recursiva que toma la lista ordenada en X y encuentra los puntos màs cercanos '''
    n=len(l)
    #si la cantidad de puntos es 3 o menos, fuerza bruta 
    if n <= 3:  
        return distanciaMinima(l)[0] 
    else:
    #encuentro la mediana  
        med = n // 2
        punto_medio = l[med] 
    # dividimos el problema creando dos listas y llamamos la recursion 
        izq = aux(l[:med]) 
        der = aux(l[med:]) 
    # encuentra la menor de las dos distancias  
        d = min(izq, der) 
    # construimos la franja que contiene puntos a una distancia menor que 'd' de la mediana
        franja = []  
        for i in range(n):  
            if abs(l[i][0] - punto_medio[0]) < d:  
                franja.append(l[i]) 
  #devuelve el mínimo de la lista completa    
    return min(d, franjaMasCercana(franja, d)) 
  
def distanciaMinimaDyC(l,algoritmo): 
    '''primero ordena la lista y luego llama a la auxiliar 'aux' (que encuentra la menor distancia)'''
    ordenamiento(l,algoritmo)
    return aux(l)   

def ordenamiento(l,algoritmo): 
    '''auxiliar que ordena las x de la lista segun distintos algoritmos'''
    if algoritmo=="merge":
        mergeSort(l)
    elif algoritmo=="up":
        upsort(l)
    else: #ordeno con el algoritmo de python segun el valor de X
        l=sorted(l, key=lambda val: val[0])
    return l

"""ALGORITMOS DE ORDENAMIENTO"""

def maxPos(a,d,h):
    '''auxiliar para upsort'''
    maxPos=d
    for i in range (d,h+1):
        if a[i]>a[maxPos]:
            maxPos=i
    return maxPos

def upsort (a):
    actual=len(a)-1
    m  = 0
    while(actual>0) :
        m =maxPos(a,0,actual)
        a[m],a[actual]=a[actual],a[m]
        actual-=1
    return a
   
def mergeSort(a):
    if len(a) >1:
        mid = len(a)//2 #identificar la mitad
        L = a[:mid] #divido en dos mitades
        R = a[mid:]  
        mergeSort(L) # primera mitad
        mergeSort(R) # Segunda
        i = j = k = 0
        # Copio la data en dos arrays temporales
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                a[k] = L[i]
                i+=1
            else:
                a[k] = R[j]
                j+=1
            k+=1
        # Chequeo que ningun elemento haya quedado afuera
        while i < len(L):
            a[k] = L[i]
            i+=1
            k+=1
        while j < len(R):
            a[k] = R[j]
            j+=1
            k+=1
    return a

def medirTiempos(fn,*args):
    inicio= time.time()
    fn(*args)
    return time.time() - inicio

def tupla_aleatoria(N,maximo):
    '''genera tuplas de N puntos,con coordenadas en x e y entre 0 y MAX'''
    lista=[]
    for i in range (N):
        x=round(random.random()*maximo,4)
        y=round(random.random()*maximo,4)
        lista.append((x,y))
    return lista
   
#para chequear que devuelvan el mismo resultado
A=tupla_aleatoria(1000,10)
if distanciaMinima(A)[0]==distanciaMinimaDyC(A,"up")==distanciaMinimaDyC(A,"merge")==distanciaMinimaDyC(A,"py"):
    print("todos los métodos devuelven la misma distancia euclidea") 
    
"""PUNTO 4"""
#genero una lista de tuplas aleatorias de N puntos. el elemento lista_tuplas[i] va a ser una tupla con puntos[i] aleatorios con valores entre 0 y 10
#para cada elemento de lista_tuplas, mido el tiempo que tarda en medir la distancia euclidea minima con los diferentes métodos, repito la prueba 4 veces
tiempos=[]
lista_tuplas=[]

puntos=[10,50,100,250,500,700,850,1000,1250,1500,2000,2500,3000,4000,10000,25000]
for i in range (len(puntos)):
    lista_tuplas.append(tupla_aleatoria(puntos[i],10))
    for j in range (4):
        tiempos.append(medirTiempos(distanciaMinima,lista_tuplas[-1]))
        tiempos.append(medirTiempos(distanciaMinimaDyC,lista_tuplas[-1],"up"))
        tiempos.append(medirTiempos(distanciaMinimaDyC,lista_tuplas[-1],"merge"))
        tiempos.append(medirTiempos(distanciaMinimaDyC,lista_tuplas[-1],"py"))

mediciones = np.array(tiempos) 
meds = mediciones.reshape(4, 16, 4) #(cantidad repeticiones, cantidad puntos, cantidad metodos)

fig = plt.figure()

plt.title('Distancia Euclídea')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
medias = np.mean(meds[:,:,:], axis=0)
stds   = np.std(meds[:,:,:], axis=0)
               
plt.errorbar(x=puntos, y=medias[:,0], label='fuerza bruta')
plt.errorbar(x=puntos, y=medias[:,1], label='D&C upsort')
plt.errorbar(x=puntos, y=medias[:,2], label='D&C mergesort')
plt.errorbar(x=puntos, y=medias[:,3], label='D&C python')

#plt.xlim(90,2010) # Esto en fn de cuantos puntos elijamos


plt.xlabel('log numero de puntos')
plt.ylabel('log tiempo de ejecución [seg]')

plt.legend(loc='best')

#Grabamos el archivo de salida
plt.savefig('multmatrices_grafico.pdf')




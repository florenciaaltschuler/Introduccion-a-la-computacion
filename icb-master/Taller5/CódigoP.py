# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import time
import random
import sys
global N
N = 10

def matrizCeros(N):
    lista=N*[0.0]
    matriz=[]
    for i in range (N):
        matriz.append(lista)
    return matriz

def matrizAleatoria(a):
    for i in range (len(a)):
        for j in range (len(a[i])):
            a[i][j]=random.random()
    return 

def multMatrices(a, b, res):
    if isinstance(a, np.matrix):
        res=np.matmul(a, b)
    else:
        for i in range (len(res)): #fila res
            for j in range (len(res[i])): #columna res
                for n in range (len(a[i])):
                    res[i][j]+=a[i][n]*b[n][j]
    return res
    
def medirTiempos(fn,*args):
    inicio= time.time()
    fn(*args)
    return time.time() - inicio

def realizarExperimento():
    a=matrizCeros(N)
    b=matrizCeros(N)
    c=matrizCeros(N)
    matrizAleatoria(b)
    matrizAleatoria(a)
    print("Tiempo total listas (s): ",medirTiempos(multMatrices,a,b,c))
    c=np.matrix(matrizCeros(N),dtype=np.float)        
    a=np.matrix(a,dtype=np.float)
    b=np.matrix(b,dtype=np.float)
    return print('Tiempo total numpy (s): ',medirTiempos(multMatrices,a,b,c))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    realizarExperimento()




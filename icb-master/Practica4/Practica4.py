# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 22:19:16 2019

@author: Flor
"""

def listsum(list):
    theSum = 0
    for i in list :
        theSum = theSum + i
    return theSum

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1)+fib(n-2) 

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

def sumatoriaPotenciasDeDos(n1, n2): 
    if n1==n2:
        return 2**n2
    else:
        return 2**n1+sumatoriaPotenciasDeDos(n1+1, n2)

def sumaImpares(n):
    if n==1:
        return 0
    elif n%2==0:
        return n-1+ sumaImpares(n-1)
    else:
        return n-2+sumaImpares(n-2)
    
def sumaDigitos(n):
    if n<10:
        return n
    else:
        return n%10+sumaDigitos(n//10)
    
def sumaDivisores(n,y=1): #devuelve la suma de todos los divisores positivos de n.
    if y==n:
        return y
    elif n%y==0:
        return y+sumaDivisores(n,y+1)
    else:
        return sumaDivisores(n,y+1)
        
def divisiblePor3(n):
    if n<10:
        return (n==3 or n==6 or n==9)
    else:
        return divisiblePor3(sumaDigitos(n))

def divisiblePor17(n):
    if n<=0:
        return abs(n)%17==0
    if n==17:
        return True #hay otra manera de poner esto?
    elif n<17:
        return False
    else:
        return divisiblePor17((n//10)-5*(n%10))

#########################PARTE 2##########################################

def suma(a):
    if a==[]:
        return 0
    else:
        return a.pop(0)+suma(a)

def maximo(a):
    if len(a)==1:
        return a[0]
    elif a[0]>=a[1]:
        a.pop(1)
    else:
        a.pop(0)
    return maximo(a)

def maximo2(a):
    if len(a)==1:
        return a[0]
    elif a[0]>maximo2(a[1:]):
        return a[0]
    else:
        return maximo2(a[1:])

def promedio(a):
    b=len(a)
    return suma(a)/b

def listaDeAbs(a): 
    if a!=[]:
        return [abs(a.pop(0))]+listaDeAbs(a)
    else:
        return []

def maximoAbsoluto(a): #TENGO QUE USAR LA FUNCION MAXIMO Y LISTA DE ABS
    return maximo(listaDeAbs(a))

def cantidadApariciones(a, x):
    if len(a)==0:
        return 0
    elif a[0]==x:
        return 1+cantidadApariciones(a[1:],x)
    else:
        return cantidadApariciones(a[1:],x)
    
def eliminar(a,y):
    if a==[]:
        return a
    elif len(a)-1==y:
        a.pop(y)
        return a
    else:
        return eliminar((a[:len(a)-1]),y)+[a[len(a)-1]]

def buscarYeliminar(a, x): 
    if len(a)==0:
        return []
    elif a[0]==x:
        a.pop(0)
        return eliminar(a[0:],x)
    else:
        return [a[0]]+ eliminar(a[1:],x)
    
def todosPares(a):
    if a==[]:
        return True 
    elif a.pop(0)%2==0:
        return todosPares(a)
    else:
        return False

def ordenAscendente(a):
    if len(a)==2:
        if a.pop(0)<=a[0]:
            return True
    else:
        if a.pop(0)<=a[0]:
            return ordenAscendente(a)
        else: 
            return False

def ordenDescendente(a):
    if len(a)==1 or len(a)==0:
        return True
    elif a[0]>=a[1]:
        return ordenDescendente(a[1:])
    else:
        return False

def reverso(a):  
    if a !=[]:
        return [a.pop(len(a)-1)]+reverso(a)
    else:
        return []

def sumaPosImpares(a):
    if len(a)==1:
        return 0
    else:
        a.pop(0)
        return a.pop(0)+sumaPosImpares(a)

def triangular(a):
    if a==[]:
        return True
    elif a[len(a)-1]<=a[len(a)-2]:
        return triangular (a[:len(a)-1])
    else:
        return ordenAscendente (a[:len(a)-1])

#########PARTE 3###############3
def map(fn, a): 
    if a==[]:
        return []
    else:
        return [fn(a.pop(0))]+map(fn,a)
    
def filter(fn, a):
    if a==[]:
        return []
    else:
        n=a.pop(0)
        if fn(n):
            return [n]+filter(fn,a)
        return filter(fn,a)

def suma2(a,b):
    return a+b    

def reduce(fn, a):
    if len(a)==1:
        return a[0]
    else: 
        return fn(a[0], reduce(fn, a[1:]))

#(Opcional) Piense como implementara las funciones suma, maximo, cantidadApariciones,
#todosPares y ordenAscendente del ejercicio 2 utilizando alguna combinacion de los esquemas
#de recursion presentados en los tems anteriores.

##############PARTE 4###################
def signo(n):
    if n<0:
        return -1
    else:
        return 1
    
def problema_A(a,j):
    if j==0:
        return signo(a[j])
    else:
        return a.pop(j)**j+problema_A(a,j-1)

def esPrimo(x): #AUXILIAR PROBLEMA B
    suma_divisores=0
    for i in range (1,abs(x)+1):
        if x%i==0:
            suma_divisores+=i
    return suma_divisores==abs(x)+1

def problema_B(n1,n2): 
    if n1+1 <= n2 and esPrimo(n1+1):
        return n1+1
    else:
        return problema_B(n1+1,n2)
    
def problema_C(a,b):
    if a==[]:
        return []
    else:
        return problema_C(a[0:len(a)-1],b)+[a.pop()+b[len(a)%len(b)]]
    
def problema_D(X,V):
    if X==[]:
        return []
    b=X.pop(0)
    if b not in V:
        return [b]+problema_D(X,V)
    return problema_D(X,V)

#################PROBLEMA 5######

print(2%2)
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 13:57:38 2019

@author: Flor
"""
def esPrimo(x): #####es ineficiente para numeros grandes seria mejor que apenas encuentre un divisor (ademas de si
#mismo y 1), de FALSE en vez de recorrer todos los numeros, ademas inclui con el ABS tambien a los numeros negativos aunque la especificacion no 
#lo pida, me parece mas generico y esa funcion puede servir para casos mas abarcativos, para el caso de 0, 1 da False
    suma_divisores=0
    for i in range (1,abs(x)+1):
        if x%i==0:
            suma_divisores+=i
    if suma_divisores==abs(x)+1:
        return True
    else:
        return False
    
def queResacon(n): #creo una lista a que va a contener los numeros que cumplan ambas condiciones AUX hasta llegar 
# al len de n, y de la lista tomo el ultimo valor, es decir devuelve el enésimo numero natural que cumpla con ambos auxiliares
    a=[]
    i=1
    while len (a)<n:
        if esPrimo((2**i)-1)==True:
            a.append((2**i)-1)
            i+=1
        else:
            i+=1
    return a[n-1]



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
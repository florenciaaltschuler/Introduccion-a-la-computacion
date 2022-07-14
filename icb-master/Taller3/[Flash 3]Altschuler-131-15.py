#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from datetime import datetime
   
def Metodo_default(datos_temp, tam_ventana): #suma los elementos de la ventana
    datos_temp=elem_matriz_float(datos_temp)
    matriz_default=[[0 for col in range(len(datos_temp[0]))] for row in range(len(datos_temp)-tam_ventana+1)] #creo una matriz del temno adecuado con 0
    for j in range (len(datos_temp[0])):#columnas las fijo
        for i in range (len(datos_temp)-tam_ventana+1): #filas#SUPONGO QUE LA LONGITUD DE TODAS LAS LINEAS ES LA MISMA
            suma=0
            for n in range (tam_ventana):
                if type(datos_temp[i+n][j])==str:
                    matriz_default[i][j]= 'NA'
                else:
                    suma=suma+datos_temp[i+n][j]
                    if type(matriz_default[i][j])!=str:
                        matriz_default[i][j]=round(suma/tam_ventana,2) #relleno la matriz con los valores de la suma
    return matriz_default

def Metodo_promedio(datos_temp, tam_ventana): #suma los elementos de la ventana
    datos_temp=elem_matriz_float(datos_temp)
    matriz_promedio=[[0 for col in range(len(datos_temp[0]))] for row in range(len(datos_temp)-tam_ventana+1)] #creo una matriz del temno adecuado con 0
    for j in range (len(datos_temp[0])):#columnas las fijo
        for i in range (len(datos_temp)-tam_ventana+1): #filas#SUPONGO QUE LA LONGITUD DE TODAS LAS LINEAS ES LA MISMA
            suma=0
            contador_na=0
            for n in range (tam_ventana):
                if type(datos_temp[i+n][j])!=str:
                    suma=round(suma+datos_temp[i+n][j],4)
                else:
                    contador_na=contador_na+1
                matriz_promedio[i][j]=round(suma/(tam_ventana-contador_na),2) #relleno la matriz con los valores de la suma
    return  matriz_promedio

def Metodo_mediana(datos_temp, tam_ventana):
    datos_temp=elem_matriz_float(datos_temp)
    matriz_mediana=[[0 for col in range(len(datos_temp[0]))] for row in range(len(datos_temp)-tam_ventana+1)] #creo una matriz del temno adecuado con 0
    for j in range (len(datos_temp[0])):#columnas las fijo
        for i in range (len(datos_temp)-tam_ventana+1): #filas#SUPONGO QUE LA LONGITUD DE TODAS LAS LINEAS ES LA MISMA
            suma=0
            for n in range (tam_ventana):
                if type(datos_temp[i+n][j])!=str:
                    suma=round(suma+datos_temp[i+n][j],4)
                else:
                    suma=suma+mediana(datos_temp[0][0:j]+datos_temp[0][(j+1):len(datos_temp)])
            matriz_mediana[i][j]=round(suma/(tam_ventana),2) #relleno la matriz con los valores de la suma
    return  matriz_mediana

def mediana(a): #para medir la mediana en una lista
    a.sort()
    if len(a)%2==0:
        return (a[len(a)//2]+a[(len(a)//2)-1])/2
    else:
        return a[(len(a)//2)]
           
        ###########################PROCESAMIENTO TIEMPO#################
        #EN LA LISTA DELTA_TIEMPO APARECE LA DIFERENCIA DE LOS TIEMPOS ENTRE VENTANAS, EN SEGUNDOS
def delta_tiempo(datos_tiempo,tam_ventana):
    delta_tiempo=[]
    for i in range (0,len(datos_tiempo)-int(tam_ventana)+1):
        intervalo=datetime.strptime(datos_tiempo[i+int(tam_ventana)-1],'%Y-%m-%dT%H:%M:%S')-datetime.strptime(datos_tiempo[i],'%Y-%m-%dT%H:%M:%S')
        delta_tiempo.append(intervalo.seconds)
    return delta_tiempo
       
##ACA TRANSFORMO TODOS LOS ELEMENTOS DE DATOS_TEMP EN FLOAT
def elem_matriz_float(datos_temp):
    for i in range (len(datos_temp)):
        for j in range (len(datos_temp[i])):
            if datos_temp[i][j]!="NA": #para que no transforme los NA's
                datos_temp[i][j] = float(datos_temp[i][j])
    return datos_temp
       
def main(argumentos):
    arch_entrada = argumentos[0]
    arch_salida  = argumentos[1]
    tam_ventana  = int(argumentos[2])
     
    if len(argumentos)> 3:
        metodo = argumentos[3]
    else:
        metodo = "default"
   
    with open(arch_entrada, 'r') as entrada, open(arch_salida, 'w') as salida: # Abre los archivos de entrada (en modo R:Read) y el de salida (en modo W:Write)
        lineasDeEntrada = []                       # Aquí nos vamos a guardar toda la info del archivo de entrada
        datos_temp=[] # LISTA DE LISTAS (MATRIZ) DE MEDICIONES
        datos_tiempo=[]  ##LISTA DE LOS TIEMPOS  
        for linea in entrada:
            linea = linea.strip('\n')             # Elimina el salto de línea del final
            camposDeLinea = linea.split(',')     # Se parte la cadena de la línea entera y se genera una lista
            lineasDeEntrada.append(camposDeLinea) # Se agrega la lista de campos de la línea a la lista de líneas completa
            datos_temp.append(camposDeLinea[1:])
            datos_tiempo.append(camposDeLinea[0])
        #lineasaFloat=np.array(lineasDeEntrada)
        #lineasFloat=lineasaFloat.astype(np.float)  #pasar de string a floats
   
        ####PROCESAMIENTO DATOS SEGUN EL METODO####
        #def usar_metodo(datos_temp, metodo):
        matriz_unida=[]
        if metodo=="default":
            matriz_unida=Metodo_default(datos_temp,tam_ventana)
        if metodo=="promedio":
            matriz_unida=Metodo_promedio(datos_temp,tam_ventana)
        if metodo=="mediana":
            matriz_unida=Metodo_mediana(datos_temp,tam_ventana)
        matriz_tiempo=delta_tiempo(datos_tiempo, tam_ventana)
        #acoplo el tiempo con los resultados
        for i in range (0,len(matriz_unida)+len(matriz_tiempo),2):
            matriz_unida.insert(i,matriz_tiempo.pop(0))
        
        #print(matriz_unida, file=salida)   
        for lineaPorCampos in matriz_unida:
            print(lineaPorCampos, file=salida) # Guarda en un archivo los campos originales, sin la primera columna

# Sólo si el programa es ejecutado (esto es, no se usa con 'import') se ejecturará lo de abajo

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Se esperaban más argumentos:\n taller3.py arch_entrada arch_salida tam_ventana [metodo_na]")
        sys.exit(1)
   
    main(sys.argv[1:])






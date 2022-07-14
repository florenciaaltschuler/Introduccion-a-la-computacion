# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:58:46 2020

@author: sol
"""
import numpy as np
import time
import imageio
from numba import jit, njit, config, prange
import matplotlib.pyplot as plt

"""PUNTO 1"""
def grey_filter(img):
# para acceder al canal rojo, R = img[:, :, 0]
#img_grey es una numpy.array de dos dimensiones, img[2,2,1] accedo al valor del pixel img_grey[2,2]
    f=img.shape[0] #fila
    c=img.shape[1] #columna
    img_grey=np.zeros((f,c))
    for i in range (0,f-1):
        for j in range (0,c-1):
            img_grey[i,j] =(img[i, j, 0] * 0.3+ img[i, j, 1] * 0.6 + img[i, j, 2] * 0.11)
    return img_grey

"""PUNTO 2"""
def blur_filter(img):
    f=img.shape[0]
    c=img.shape[1]
    for i in range (1,f-1):
        for j in range (1, c-1):
            img[i,j]=(img[i+1,j]+img[i-1,j]+img[i,j+1]+img[i,j-1])*0.25
    #ponemos los bordes negros 
    img[0,:]=0
    img[f-1,:]=0
    img[:,0]=0
    img[:,c-1]=0
    return img

"""PUNTO 3, repito las funciones anteriores pero aplicando  las directivas de Numba para que se ejecuten just-in-timecompiling"""
@jit
def grey_filter_jit(img):
    f=img.shape[0] 
    c=img.shape[1] 
    img_grey=np.zeros((f,c))
    for i in range (0,f-1):
        for j in range (0,c-1):
            img_grey[i,j] =(img[i, j, 0] * 0.3+ img[i, j, 1] * 0.6 + img[i, j, 2] * 0.11)
    return img_grey

@jit
def blur_filter_jit(img):
    f=img.shape[0]
    c=img.shape[1]
    for i in range (1,f-1):
        for j in range (1, c-1):
            img[i,j]=(img[i+1,j]+img[i-1,j]+img[i,j+1]+img[i,j-1])*0.25
    img[0,:]=0
    img[f-1,:]=0
    img[:,0]=0
    img[:,c-1]=0
    return img

"""PUNTO 4, modifico las fx del punto 1 y 2 para que Numba utilice paralelismo"""
@njit (parallel=True)
def grey_filter_njit(img):
    f=img.shape[0] 
    c=img.shape[1] 
    img_grey=np.zeros((f,c))
    for i in prange (0,f-1):
        for j in prange (0,c-1):
            img_grey[i,j] =(img[i, j, 0] * 0.3+ img[i, j, 1] * 0.6 + img[i, j, 2] * 0.11)
    return img_grey

@njit (parallel=True)
def blur_filter_njit(img):
    f=img.shape[0]
    c=img.shape[1]
    for i in prange (1,f-1):
        for j in prange (1, c-1):
            img[i,j]=(img[i+1,j]+img[i-1,j]+img[i,j+1]+img[i,j-1])*0.25
    img[0,:]=0
    img[f-1,:]=0
    img[:,0]=0
    img[:,c-1]=0
    return img

"""PUNTO 5"""
def medirTiempos(fn,*args):
    inicio=time.time()
    fn(*args)
    return time.time()-inicio

def realizarExperimento():
#devuelve el tiempo de implementacion en python, en numba jit y con paralelizacion respectivamente del tiempo que tarda en transformar en gris y blurear la imagen
    Tiempos=[]
    tiempo_py=medirTiempos(blur_filter,grey_filter(img))
    tiempo_jit=medirTiempos(blur_filter_jit,grey_filter_jit(img))
    Tiempos.append(tiempo_py)
    Tiempos.append(tiempo_jit)
    for i in range (1,5): #realizamos la paralelizacion con 1,2,3 y 4 nucleos, seteamos los threading layers
        config.THREADING_LAYER = i
        tiempo=medirTiempos(blur_filter_njit,grey_filter_njit(img))
        Tiempos.append(tiempo)
    return Tiempos


   
"""PARA VER IMAGEN RESULTANTE DE APLICAR LOS FILTROS"""
img=imageio.imread('3.jpg') #leo la imagen base
blur_img=blur_filter(grey_filter(img)) #le aplico los filtros
blur_image = img.fromarray(blur_img.astype(np.uint8)) #paso a enteros los elementos de la matriz para que sea leida como imagen
blur_image.save('blur_image.png') #almaceno la imagen en disco

"""realizo el experimento"""
#definir img, realizo el experimento con 2 repeticiones y relalizo el experimento para 8 imagenes de tamaños crecientes

Matriz=[]
imagenes=[imageio.imread("1.png"), imageio.imread("2.jpg"), imageio.imread("3.jpg"), imageio.imread("4.jpg"),imageio.imread("5.jpg"), imageio.imread("6.jpg"), imageio.imread("7.jpg"), imageio.imread("8.jpg")]

for i in range (0,2): #2 repeticiones
    for i in range (len(imagenes)):
        img= imagenes[i]
        Matriz.append(realizarExperimento())
    
Matriz = np.array(Matriz) 
Matriz = Matriz.reshape(2, 8, 6) #(cantidad repeticiones, cantidad puntos, cantidad metodos)

"""GRAFICO"""

fig = plt.figure()
plt.title('Tiempo de ejecución')
plt.xscale('linear')
plt.yscale('log')
plt.grid(True)
Num_kbytes=[689,2694,3403,3971,4373,4642,4917,5463]
medias = np.mean(Matriz[:,:,:], axis=0)
stds   = np.std(Matriz[:,:,:], axis=0)
               
plt.errorbar(x=Num_kbytes, y=medias[:,0],yerr=stds[:,0], label='python')
plt.errorbar(x=Num_kbytes, y=medias[:,1],yerr=stds[:,1], label='jit')
plt.errorbar(x=Num_kbytes, y=medias[:,2],yerr=stds[:,2], label='njit_1')
plt.errorbar(x=Num_kbytes, y=medias[:,3],yerr=stds[:,3], label='njit_2')
plt.errorbar(x=Num_kbytes, y=medias[:,4],yerr=stds[:,4], label='njit_3')
plt.errorbar(x=Num_kbytes, y=medias[:,5],yerr=stds[:,5], label='njit_4')

plt.xlabel('tamaño imágen [kB]')
plt.ylabel('tiempo de ejecución [seg]')
plt.legend(loc='best')
plt.savefig('Numba_grafico.pdf')#Grabamos el archivo de salida





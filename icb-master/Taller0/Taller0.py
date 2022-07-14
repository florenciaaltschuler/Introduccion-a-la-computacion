import random

def generarMazo(n):
#creo una lista y le voy agregando los numeros del 1 al 13, despues multiplico la lista 
#por 4 para tener las cuatro figuras y por el numero de jugadores n, luego mezclo
    Mazo_individual=[]
    for i in range (1,14):
        Mazo_individual.append(i)
    Mazo_total=Mazo_individual*n*4
    random.shuffle(Mazo_total)
    return Mazo_total

def jugar(m):
#a la variable suma le voy sumando las cartas que saque el jugador, va a sacar cartas
#siempre que la longitud del mazo sea distinta a 0 y siempre y cuando el valor de la suma sea 
#menor o igual a 21
    i=0
    suma=0
    while suma <= 21:
        if len(m)!=0:
            suma=suma+m.pop(0)
        else:
            return suma
    return suma

def jugar_varios(m,j):
#creo la lista en la que aparece la suma de cada jugador, la funcion jugar varios tiene que
#llamar a la funcion jugar j veces, siendo j el numero de jugadores
    i=1
    jugadas=[]
    while i <=j:
        jugadas.append(jugar(m))
        i=i+1
    return jugadas

def jugarMiedo(m):
#ahora el jugador va a dejar de jugar cuando su suma sea mayor a 19 (siempre que el mazo
#no esté vacío)
    suma=0
    while suma <= 19:
        if len(m)!=0:
            suma=suma+m.pop(0)
        else:
            return suma
    return suma

def jugarBorracho(m):
#al principio saca una carta, mientras que la suma sea menor o igual a 21 implementa la 
#estrategia de pedir otra carta aleatoriamente, cuando no pide más o suma superó 21, 
#devuelve el valor suma
    i=0
    suma=m.pop(0)
    while suma <=21:
        if len(m)!=0:
            if random.random() > 0.5:
                suma=suma+m.pop(0)
            else:
                return suma
        else:
            return suma
    return suma
             
def jugarSmart(m):
#el jugador saca una carta, y dependiendo de la suma, toma distintas estrategias
#para decidir si tomar otra o no (siempre que la suma sea menor a 21)
    suma=m.pop(0)
    while suma<=21:
        if suma <= 5:
            if random.random() > 0.25:
                suma=suma+m.pop(0)
            else:
                return suma
        if 5<suma<=15:
            if random.random()>0.5:
                suma=suma+m.pop(0)
            else:
                return suma
        if 15<suma<21:
            if random.random()>0.75:
                suma=suma+m.pop(0)
            else:
                return suma
        else:
            return suma
    return suma             
         
def compararEstrategia(lista_jug):  
#como la longitud de lista de jugadores me dice la cantidad de jugadores, uso ese numero
#para crear un mazo m, y para cada jugador juega una estrategia distinta y crea una lista 
#"resultado"con la suma de cada jugador
    i=0
    resultado=[]
    m=generarMazo(len(lista_jug))
    while i<len(lista_jug):
        if lista_jug[i]==0:
            resultado.append(jugar(m))
        if lista_jug[i]==1:
            resultado.append(jugarMiedo(m))
        if lista_jug[i]==2:
            resultado.append(jugarBorracho(m))
        if lista_jug[i]==3:
            resultado.append(jugarSmart(m))
        i=i+1         
    return resultado         
 

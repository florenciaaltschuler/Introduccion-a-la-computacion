def hayBorde(a,n,h): #por ahora solo me dice si hay borde en los primeros dos numeros de la lista
    if a==[]:#si es una lista vacia, no hay borde
        return False
    x=0     #comienzo del numero 1
    y=x+1     #fin del numero 1
    while a[x]==a[y]:
        y+=1
    w=y     #comienzo del numero 2
    z=w+1    #fin del numero 2 
    while z<len(a) and a[w]==a[z] :
        z+=1
    if (y-x)>=n and (z-w)>=n and abs(a[x]-a[w])==h:
        return True
    elif z<len(a):
        for i in range (0,x+1):
            a.remove(a[i])
        return hayBorde(a,n,h)
    else:
        return False
    

def esTriang(a):
    if a==[]:
        return True
    i=0 #i es el contador para el momento creciente de la lista
    while i<(len(a)-1) and a[i]<=a[i+1]:
        i+=1
    j=i #j es el contador para el momento decreciente de la lista
    while j<(len(a)-1) and a[j]>=a[j+1]:
        j+=1
    return j+1==len(a) #cuando ya termine de leer toda la lista y si se cumplieron las dos condiciones
        

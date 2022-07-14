# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:17:17 2020

@author: sol
"""

# asumimos que las celdas son consistentes entre si. es decir si en la celda X hay pared a la derecha, la celda X+1 hay pared a la izquierda


class Laberinto(object):
  def __init__(self, parent=None):
    self.fil=5
    self.col=5
    self.parent = parent
    self.laberinto=[[[1,1,0,0],[0,1,0,1],[0,1,0,1],[0,1,0,1],[0,1,1,0]],[[1,1,0,0],[0,1,0,1],[0,1,1,0],[1,1,0,1],[0,1,0,0]],[[0,1,0,0],[0,1,0,1],[0,1,0,1],[0,1,1,1],[1,1,1,0]],[[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,1,1],[1,1,1,0]],[[0,0,0,0],[0,1,0,1],[0,1,0,1],[0,1,1,1],[1,0,1,0]]]
    self.posQueso=(1,0)
    self.posRata=(0,0)
    self.diccionario={}
    self._posAnteriorRata = ()
##### interfaz (metodos publicos)
  def cargar(self,fn):
    with open (fn, 'r') as entrada:
      matriz = [] 
      self.laberinto = []
      for linea in entrada:
        if linea[0]=='D':
            linea1 = linea
            linea1 = linea[4:(len(linea1)-2)]
            dimMatrices = linea1.split(',')
            for i in range(len(dimMatrices)):
                dimMatrices[i] = int(dimMatrices[i])
        else:
            linea = linea.strip('\n') #borre el espacio
            lineaPorCampos = linea.split('][')
            lineaPorCampos[0] = lineaPorCampos[0][1:]
            lineaPorCampos[len(lineaPorCampos)-1] = lineaPorCampos[len(lineaPorCampos)-1][:7]
            matriz.append(lineaPorCampos)
      self.fil=dimMatrices[0]#filas,
      self.col=dimMatrices[1]#columnas
      for fila in range(len(matriz)):
        lista = []
        N = []
        for columna in range(len(matriz[fila])):
            celda = []
            celda = matriz[fila][columna].split(',')
            lista.append([0,0])
            for pos in range(len(celda)):
              celda[pos] = int(celda[pos])
            N.append(celda)
        self.laberinto.append(N)
    self.posRata=(0,0) 
    self.posQueso=((self.fil-1),(self.col-1))
    self.resetear()
    return self.laberinto
       
  def tamano(self):
    return (self.fil,self.col)
  
  def resetear(self):
    for i in range (self.fil):
      for j in range (self.col):
        self.diccionario[(i,j)]={"visitada": False, "caminoactual": False} 
    return self.diccionario

  def getPosicionRata(self):
    return self.posRata
  
  def getPosicionQueso(self):
    return self.posQueso

  def setPosicionRata(self,i,j):
    self.posRata=(i,j)
    pass
  
  def setPosicionQueso(self,i,j):
    self.posQueso=(i,j)
    pass

  def esPosicionRata(self, i, j):
    return (i == self.posRata[0] and j == self.posRata[1])

  def esPosicionQueso(self, i, j):
    return (i == self.posQueso[0] and j == self.posQueso[1])

  def getInfoCelda(self, i, j):
  # devuelve lo que hay dentro de la clave (i,j) del diccionario
    if (i,j) in self.diccionario:
      return self.diccionario[(i,j)]

  def get(self, i, j):
      res=[] #le voy appendeando los booleanos
      for k in range (4):
        res.append(self.laberinto[i][j][k]==1)
      return res

  def resuelto(self):
    return self.posRata==self.posQueso

  def EsPared(self, offsetX, offsetY):
    infoCelda=self.get(self.posRata[0],self.posRata[1]) 
    offset=(offsetX,offsetY)
    # calcular con posicion actual
    # abajo, si offset es (1,0) => hay que fijarse tercera posicion del vector
    if offset ==(1,0):
      return bool(infoCelda[3]) #devuelve true si es 1 (pared)
    # arriba
    if offset ==(-1,0):
      return bool(infoCelda[1])
    # derecha
    if offset ==(0,1):
      return bool(infoCelda[2])
    # izq
    if offset ==(0,-1):
      return bool(infoCelda[0])

  def EstaVisitada(self, offsetX, offsetY):
    # calcular con posicion futura
    # accede al diccionario de la posicion futura y ver si esta visitada=true
    return self.getInfoCelda(self.posRata[0]+offsetX,self.posRata[1]+offsetY)['visitada']
    
  def EsCaminoActual(self, offsetX, offsetY):
    # calcular con posicion futura
    # accede al diccionario de la posicion futura y ver si esta caminoActual=true
    return self.getInfoCelda(self.posRata[0]+offsetX,self.posRata[1]+offsetY)['caminoactual']

  def EstaDentroLaberinto(self, offsetX,offsetY):
    return 0<=self.posRata[0]+offsetX<self.fil and 0<=self.posRata[1]+offsetY<self.col

  def puedeMover(self, offsetX, offsetY):
    # no es pared y no esta visitada y no es camino actual
    if not self.EstaDentroLaberinto(offsetX,offsetY):
        return False  
    return not (self.EsPared(offsetX, offsetY) or self.EstaVisitada(offsetX, offsetY) or self.EsCaminoActual(offsetX, offsetY))

  def moverRata(self, offsetX, offsetY):
    # setea la posicion nueva como camino actual 
    self.setPosicionRata(self.posRata[0]+offsetX,self.posRata[1]+offsetY)
    self._redibujar()  
    pass

  def marcarPosicionRataComoCaminoActual(self,boolean):
    self.diccionario[self.posRata]['caminoactual']=boolean
    pass
      
  def marcarPosicionRataComoVisitada(self):
    self.diccionario[self.posRata]['visitada']=True 
    pass

  def puedeVolver(self,offsetX,offsetY):
    if not self.EstaDentroLaberinto(offsetX,offsetY):
        return False  
    return not (self.EsPared(offsetX, offsetY) or self.EstaVisitada(offsetX, offsetY))

  def volverAtras(self):
    #se elige el orden inverso al que se movio alguna posicion es camino actual, mover a rata a camino actual y llamar a resolver, si todas son visitadas o pared, return false
    if self.puedeVolver(-1, 0):
      self.moverRata(-1, 0)
      return self.resolver()
    if self.puedeVolver(1, 0):
      self.moverRata(1, 0)
      return self.resolver()
    if self.puedeVolver(0, -1):
      self.moverRata(0, -1)
      return self.resolver()
    if self.puedeVolver(0, 1):
      self.moverRata(0, 1)
      return self.resolver()
    else: 
      return False

  def resolver(self):
    if self.resuelto(): 
      return True

    elif self.puedeMover(1, 0):
      self.marcarPosicionRataComoCaminoActual(True)
      self.moverRata(1, 0)
      self.resolver() # llamo a la recursión
    elif self.puedeMover(-1, 0):
      self.marcarPosicionRataComoCaminoActual(True)
      self.moverRata(-1, 0)
      self.resolver()
    elif self.puedeMover(0, 1):
      self.marcarPosicionRataComoCaminoActual(True)
      self.moverRata(0, 1)
      self.resolver()
    elif self.puedeMover(0, -1):
      self.marcarPosicionRataComoCaminoActual(True)
      self.moverRata(0, -1)
      self.resolver()
    else: #en este caso tiene que hacer backtracjing
      self.marcarPosicionRataComoVisitada() 
      self.marcarPosicionRataComoCaminoActual(False)
      self.volverAtras()
      
    return False
    # a lo mejor poner if: return true
    #else: return false, el false ponerlo abajo de un else y despues adentro los otroos ifs

  def _redibujar(self):
    if self.parent is not None:
        self.parent.update()
        









  
  

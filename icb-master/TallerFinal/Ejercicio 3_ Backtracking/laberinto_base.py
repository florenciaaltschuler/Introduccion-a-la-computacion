# -*- coding: utf-8 -*-

class Laberinto(object):
	def __init__(self, parent=None):
		self.parent = parent
   
	##### interfaz (metodos publicos)

	####
	#### COMPLETAR CON LOS METODOS PEDIDOS
	####

	##### auxiliares (metodos privados)

	def _redibujar(self):
	    if self.parent is not None:
	        self.parent.update()

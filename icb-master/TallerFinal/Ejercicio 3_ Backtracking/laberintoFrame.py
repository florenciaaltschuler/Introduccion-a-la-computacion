# -*- coding: utf-8 -*-
# Copyright (C) 2000-2013 Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import operator, traceback
import iconos

from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QBrush, QPainter, QFrame, QImage

from laberintoThread import LaberintoThread

def trace(f):
    def _f(*args, **kwargs):
        if args[0].traceCalls:
            print("{0}.{1} {2}".format(type(args[0]), f.__name__, args[1:]))
        return f(*args, **kwargs)
    return _f

class Direction(object):
    Left, Right, Up, Down = 0, 1, 2, 3
    def __init__(self, d):
        self.direction = d

class Position(object):
    def __init__(self, pos, cell, limits):
        self.pos = pos
        self.cell = cell
        self.limits = limits

    def move(self, direction):
        left, up, right, down = tuple(self.cell)
        r = self.pos
        if direction == Direction.Left and not left:
            r = tuple(map(operator.add, self.pos, (0, -1)))
        elif direction == Direction.Right and not right:
            r = tuple(map(operator.add, self.pos, (0, 1)))
        elif direction == Direction.Up and not up:
            r = tuple(map(operator.add, self.pos, (-1, 0)))
        elif direction == Direction.Down and not down:
            r = tuple(map(operator.add, self.pos, (1, 0)))
        assert self._validPos(r)
        return r

    def _validPos(self, pos):
        return 0 <= pos[0] < self.limits[0] and 0 <= pos[1] < self.limits[1]

class LaberintoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # prints con los llamados a métodos
        self.traceCalls = False

        self.mainwidget = parent.parent() # GP es la MainWindow, Parent es centralWidget
        self.laberinto = LaberintoThread(parent=self)
        self.cell_size = 60
        self.frame_size = (600, 600)
        self.mousepos = None

        self.cheese = QImage(':obj/img/cheese.png')
        self.scaled_cheese = None
        self.rat = QImage(':obj/img/rat.png')
        self.scaled_rat = None

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self._moveKeyboardFocusObject(Direction.Left)
        elif key == Qt.Key_Right:
            self._moveKeyboardFocusObject(Direction.Right)
        elif key == Qt.Key_Up:
            self._moveKeyboardFocusObject(Direction.Up)
        elif key == Qt.Key_Down:
            self._moveKeyboardFocusObject(Direction.Down)
        else:
            super().keyPressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        tv, th = self.laberinto.tamano()
        cell_x, cell_y = self.width() / th, self.height() / tv
        # calculo sobre qué celda estoy parado
        newmousepos = (pos.y() // cell_y, pos.x() // cell_x)
        # actualizo self.mousepos y redibujo solamente si cambió
        if newmousepos != self.mousepos:
            self.mousepos = newmousepos
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._moveMouseFocusObject()
            self.laberinto.resetear()
        else:
            super().mousePressEvent(event)

    def updateFrameSize(self):
        tv, th = self.laberinto.tamano()
        self.frame_size = (th*self.cell_size, tv*self.cell_size)
        if tv > 0 and th > 0:
            self.scaled_cheese = self.cheese.scaled(self.frame_size[0] / th, self.frame_size[1] / tv)
            self.scaled_rat = self.rat.scaled(self.frame_size[0] / th, self.frame_size[1] / tv)

    def minimumSizeHint(self):
        return QSize(*self.frame_size)

    def sizeHint(self):
        return QSize(*self.frame_size)

    def paintEvent(self, event):
        bg_color = Qt.black

        # configuración del painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # transformación window-viewport
        painter.setWindow(0, 0, *self.frame_size)

        # fondo del laberinto
        painter.fillRect(0, 0, self.frame_size[0], self.frame_size[1], QBrush(bg_color))

        # dibujar el laberinto
        self._paintLaberinto(painter)

    def load(self, fn):
        try:
            # cargo el archivo
            self.laberinto.cargar(fn)

            # guardo el valor que me setearon del queso y la rata para poder restaurarlos después
            quesov, quesoh = self.laberinto.getPosicionQueso()
            ratav, ratah = self.laberinto.getPosicionRata()

            # seteo los valores máximos de los spinboxes para que no nos podamos ir de los límites del laberinto
            tv, th = self.laberinto.tamano()
            self.mainwidget.setStartPosLimits(tv-1, th-1)
            self.mainwidget.setEndPosLimits(tv-1, th-1)

            # restauro
            self.laberinto.setPosicionRata(ratav, ratah)
            self.laberinto.setPosicionQueso(quesov, quesoh)

            # actualizo posiciones inicial y final
            self.mainwidget.refreshSpinBoxes()

            # actualizo tamaño del widget y de sus ancestros
            self.updateFrameSize()
            self.updateGeometry()
            self.parent().adjustSize()
            self.mainwidget.adjustSize()
        except Exception as e:
            # muestro en pantalla el traceback de la excepción que puede estar tirando cargar para que la vea el usuario
            traceback.print_exc()
            # vuelvo a tirar la excepcion para arriba para que sea manejada por la GUI
            raise e

    def reset(self):
        self.laberinto.resetear()
        self.update()

    def getPosicionRata(self):
        return self.laberinto.getPosicionRata()

    def getPosicionQueso(self):
        return self.laberinto.getPosicionQueso()

    @trace
    def setPosicionRata(self, i, j):
        if self.laberinto.setPosicionRata(i, j):
            self.mainwidget.updateUIStartPos(i, j)
            self.update()

    @trace
    def setPosicionQueso(self, i, j):
        if self.laberinto.setPosicionQueso(i, j):
            self.mainwidget.updateUIEndPos(i, j)
            self.update()

    def setKeyboardTracking(self, enabled):
        if enabled:
            self.grabKeyboard()
        else:
            self.releaseKeyboard()

    def setMouseTracking(self, enabled):
        self.mousepos = None
        self.update()
        super().setMouseTracking(enabled)

    def laberintoResuelto(self):
        self.mainwidget.showLaberintoResuelto()

    def laberintoIncompleto(self):
        self.mainwidget.showLaberintoIncompleto()

    #### métodos privados
    def _paintLaberinto(self, painter):
        # referencia local al laberinto
        l = self.laberinto
        tv, th = l.tamano()

        if tv > 0 and th > 0:
            # configuro color del painter
            fg_color = Qt.white
            painter.setBrush(fg_color)
            painter.setPen(fg_color)

            # tamaño de cada celda
            gap_i = self.frame_size[1] / tv
            gap_j = self.frame_size[0] / th

            # itero las celdas
            l.lock()
            for i in range(tv):
                for j in range(th):
                    self._paintCellMeta(painter, l.getInfoCelda(i, j), gap_j, gap_i)
                    cell = l.get(i, j)
                    if l.esPosicionRata(i, j):
                        painter.drawImage(0, 0, self.scaled_rat)
                    elif l.esPosicionQueso(i, j):
                        painter.drawImage(0, 0, self.scaled_cheese)
                    self._paintCell(painter, cell, gap_j, gap_i)
                    if self.mousepos is not None and self.mousepos == (i, j):
                        self._paintMouseUnder(painter, gap_j, gap_i)
                    painter.translate(gap_j, 0)
                painter.translate(-gap_j*th, gap_i)
            l.unlock()

    def _paintCell(self, painter, cell, csize_x, csize_y):
        left, up, right, down = tuple(cell)
        if left:
            painter.drawLine(0, 0, 0, csize_y-1)
        if up:
            painter.drawLine(0, 0, csize_x-1, 0)
        if right:
            painter.drawLine(csize_x-1, 0, csize_x-1, csize_y-1)
        if down:
            painter.drawLine(0, csize_y-1, csize_x-1, csize_y-1)

    def _paintCellMeta(self, painter, meta, csize_x, csize_y):
        cpath_color = Qt.darkGreen
        oldpath_color = Qt.gray
        if meta['caminoActual']:
            painter.fillRect(0, 0, csize_x-1, csize_y-1, QBrush(cpath_color))
        elif meta['visitada']:
            painter.fillRect(0, 0, csize_x-1, csize_y-1, QBrush(oldpath_color))

    def _paintMouseUnder(self, painter, csize_x, csize_y):
        painter.save()
        mouseUnder_color = Qt.blue
        painter.setOpacity(0.6)
        painter.fillRect(0, 0, csize_x-1, csize_y-1, QBrush(mouseUnder_color))
        painter.restore()

    def _moveMouseFocusObject(self):
        rataFocus = self.mainwidget.isModifyStartPosEnabled()
        quesoFocus = self.mainwidget.isModifyEndPosEnabled()
        if rataFocus:
            self.setPosicionRata(*self.mousepos)
        elif quesoFocus:
            self.setPosicionQueso(*self.mousepos)

    def _moveKeyboardFocusObject(self, direction):
        rataFocus = self.mainwidget.isModifyStartPosEnabled()
        quesoFocus = self.mainwidget.isModifyEndPosEnabled()
        if rataFocus:
            self._moveRata(direction)
        elif quesoFocus:
            self._moveQueso(direction)

    def _moveRata(self, direction):
        oldstart = self.laberinto.getPosicionRata()
        oldend = self.laberinto.getPosicionQueso()
        pos = Position(oldstart, self.laberinto.get(*oldstart), self.laberinto.tamano())
        newstart, newend = pos.move(direction), oldend
        self._relocate(newstart, newend)

    def _moveQueso(self, direction):
        oldstart = self.laberinto.getPosicionRata()
        oldend = self.laberinto.getPosicionQueso()
        pos = Position(oldend, self.laberinto.get(*oldend), self.laberinto.tamano())
        newstart, newend = oldstart, pos.move(direction)
        self._relocate(newstart, newend)

    def _relocate(self, posrata, posqueso):
        self.laberinto.resetear()
        self.setPosicionRata(*posrata)
        self.setPosicionQueso(*posqueso)

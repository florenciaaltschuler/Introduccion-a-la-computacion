#!/usr/bin/env python3
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

import sys
from PyQt4.QtCore import QDir
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt4 import uic

def trace(f):
    def _f(*args, **kwargs):
        if args[0].traceCalls:
            print("{0}.{1} {2}".format(type(args[0]).__name__, f.__name__, args[1:]))
        return f(*args, **kwargs)
    return _f

class LaberintoViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # prints con los llamados a métodos
        self.traceCalls = True
        
        # cargo UI externa
        self.ui = uic.loadUi('laberinto.ui', self)

        # desactivo botones y sliders mientras no se haya cargado nada
        self.disableButtons(True)
        self.modifyStartPosEnabled = False
        self.modifyEndPosEnabled = False

        # conecto los botones
        self.ui.cargarButton.clicked.connect(self.load)
        self.ui.salirButton.clicked.connect(self.close)
        self.ui.resolverButton.clicked.connect(self.solve)
        self.ui.resetearButton.clicked.connect(self.reset)
        self.ui.modificarInicialButton.toggled.connect(self.toggleModifyStartPos)
        self.ui.modificarFinalButton.toggled.connect(self.toggleModifyEndPos)

        # conecto eventos de los spinboxes
        self.ui.xInicialSpinBox.valueChanged.connect(self.changeValueX0)
        self.ui.xFinalSpinBox.valueChanged.connect(self.changeValueXf)
        self.ui.yInicialSpinBox.valueChanged.connect(self.changeValueY0)
        self.ui.yFinalSpinBox.valueChanged.connect(self.changeValueYf)

        # evento del slider
        self.setAnimationSpeed(self.ui.animationSpeedSlider.value()) # reseteo al valor de la UI
        self.ui.animationSpeedSlider.valueChanged.connect(self.setAnimationSpeed)

    def load(self):
        fn = QFileDialog.getOpenFileName(self, "Cargar laberinto",
                QDir.currentPath(), "Laberintos (*.lab);;*")
        
        # QFileDialog.getOpenFileName devuelve '' si el usuario cancelo
        if len(fn) > 0:
            try:
                self.ui.frame.load(fn)
                self.disableButtons(False)
                self.reset()
            except:
                self.showLoadError(fn)
    
    def solve(self):
        self.disableLoad(True)
        self.disableButtons(True)
        self.ui.frame.laberinto.resolver()

    def reset(self):
        t = self.ui.frame.laberinto.tamano()
        self.ui.xInicialSpinBox.setMaximum(t[0]-1)
        self.ui.yInicialSpinBox.setMaximum(t[1]-1)
        self.ui.frame.reset()
        self.refreshSpinBoxes()

    @trace
    def disableLoad(self, val):
        self.ui.cargarButton.setDisabled(val)

    @trace
    def disableButtons(self, val):
        self.disableSpinboxInicial(val)
        self.disableSpinboxFinal(val)
        self.modifyButtonsSetChecked(False)
 
        self.ui.resolverButton.setDisabled(val)
        self.ui.resetearButton.setDisabled(val)
        self.ui.modificarInicialButton.setDisabled(val)
        self.ui.modificarFinalButton.setDisabled(val)

        self.update()

    @trace
    def disableSpinboxInicial(self, val):
        self.ui.xInicialSpinBox.setReadOnly(val)
        self.ui.yInicialSpinBox.setReadOnly(val)

    @trace
    def disableSpinboxFinal(self, val):
        self.ui.xFinalSpinBox.setReadOnly(val)
        self.ui.yFinalSpinBox.setReadOnly(val)

    @trace
    def toggleModifyStartPos(self, val):
        # toggleo los spinboxes
        self.modifyStartPosEnabled = val
        self.ui.xInicialSpinBox.setReadOnly(not val)
        self.ui.yInicialSpinBox.setReadOnly(not val)

        # desactivo el otro spinbox si ya estaba activo
        if val and self.ui.modificarFinalButton.isChecked(): #self.isModifyEndPosEnabled():
            self.ui.modificarFinalButton.setChecked(False)
            self.toggleModifyEndPos(False)

        self.ui.frame.setKeyboardTracking(val)
        self.ui.frame.setMouseTracking(val)

    @trace
    def toggleModifyEndPos(self, val):
        # toggleo los spinboxes
        self.modifyEndPosEnabled = val
        self.ui.xFinalSpinBox.setReadOnly(not val)
        self.ui.yFinalSpinBox.setReadOnly(not val)

        # desactivo el otro spinbox si ya estaba activo
        if val and self.ui.modificarInicialButton.isChecked(): #self.isModifyStartPosEnabled():
            self.ui.modificarInicialButton.setChecked(False)
            self.toggleModifyStartPos(False)

        self.ui.frame.setKeyboardTracking(val)
        self.ui.frame.setMouseTracking(val)

    @trace
    def changeValueX0(self, event):
        self.ui.frame.setPosicionRata(self.ui.xInicialSpinBox.value(),
                self.ui.yInicialSpinBox.value())

    @trace
    def changeValueXf(self, event):
        self.ui.frame.setPosicionQueso(self.ui.xFinalSpinBox.value(),
                self.ui.yFinalSpinBox.value())

    @trace
    def changeValueY0(self, event):
        self.changeValueX0(event)

    @trace
    def changeValueYf(self, event):
        self.changeValueXf(event)

    @trace
    def updateUIStartPos(self, i, j):
        self.ui.xInicialSpinBox.setValue(i)
        self.ui.yInicialSpinBox.setValue(j)

    @trace
    def updateUIEndPos(self, i, j):
        self.ui.xFinalSpinBox.setValue(i)
        self.ui.yFinalSpinBox.setValue(j)

    @trace
    def refreshSpinBoxes(self):
        self.updateUIStartPos(*self.ui.frame.getPosicionRata())
        self.updateUIEndPos(*self.ui.frame.getPosicionQueso())

    @trace
    def setStartPosLimits(self, i, j):
        self.ui.xInicialSpinBox.setMaximum(i)
        self.ui.yInicialSpinBox.setMaximum(j)

    @trace
    def setEndPosLimits(self, i, j):
        self.ui.xFinalSpinBox.setMaximum(i)
        self.ui.yFinalSpinBox.setMaximum(j)

    @trace
    def isModifyStartPosEnabled(self):
        return self.modifyStartPosEnabled

    @trace
    def isModifyEndPosEnabled(self):
        return self.modifyEndPosEnabled

    @trace
    def modifyButtonsSetChecked(self, val):
        self.ui.modificarInicialButton.setChecked(val)
        self.ui.modificarFinalButton.setChecked(val)

    @trace
    def solveButtonsSetChecked(self, val):
        self.ui.resolverButton.setChecked(val)

    @trace
    def setAnimationSpeed(self, speed):
        slider = self.ui.animationSpeedSlider
        delay = (slider.maximum() - slider.value()) / 100.0
        self.ui.frame.laberinto.setAnimationDelay(delay)

    @trace
    def showLoadError(self, fn):
        QMessageBox.critical(self, "Error de carga",
            "No se pudo cargar: {0}".format(fn))

    @trace
    def showLaberintoIncompleto(self):
        self.solveButtonsSetChecked(False)
        self.disableLoad(False)
        self.disableButtons(False)
        QMessageBox.critical(self, "Laberinto incompleto",
            "No se pudo llegar al final del laberinto")

    @trace
    def showLaberintoResuelto(self):
        self.solveButtonsSetChecked(False)
        self.disableLoad(False)
        self.disableButtons(False)
        QMessageBox.information(self, "Laberinto resuelto!",
                "La rata se comió el queso")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    lv = LaberintoViewer()
    lv.show()

    sys.exit(app.exec_())

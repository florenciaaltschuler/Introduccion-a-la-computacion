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

from PyQt4.QtCore import QThread, QMutex, QWaitCondition, QTimer, pyqtSignal

from laberinto import Laberinto

class LaberintoThread(QThread):
    laberintoTerminado = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()

        self.laberinto = Laberinto(parent=self)
        self.mutex = QMutex()
        self.waitWorker = QWaitCondition()
        self.waitController = QWaitCondition()

        self.parent = parent
        self.running = True
        self.solving = False
        self.timer = QTimer()
        self.delay = 20

        self.timer.timeout.connect(self.continue_)
        self.laberintoTerminado.connect(self.handleLaberintoTerminado)

        self.start()

    def __del__(self):
        self.running = False
        self.waitWorker.wakeOne()
        self.wait()

    ##### interfaz que sobreescribo (métodos públicos)

    def tamano(self, *args):
        return self.laberinto.tamano(*args)

    def cargar(self, *args):
        self.laberinto.cargar(*args)

    def resolver(self):
        self.mutex.lock()
        if not self.solving:
            self.waitWorker.wakeOne()
        self.mutex.unlock()

    def resetear(self, *args):
        return self.laberinto.resetear(*args)

    def esPosicionRata(self, *args): 
        return self.laberinto.esPosicionRata(*args)

    def esPosicionQueso(self, *args):
        return self.laberinto.esPosicionQueso(*args)

    def get(self, *args):
        return self.laberinto.get(*args)

    def getInfoCelda(self, *args):
        return self.laberinto.getInfoCelda(*args)

    def getPosicionRata(self, *args):
        return self.laberinto.getPosicionRata(*args)

    def getPosicionQueso(self, *args):
        return self.laberinto.getPosicionQueso(*args)

    def setPosicionRata(self, *args):
        return self.laberinto.setPosicionRata(*args)

    def setPosicionQueso(self, *args):
        return self.laberinto.setPosicionQueso(*args)

    ##### intefaz nueva

    def update(self):
        self.mutex.unlock()
        self.parent.update()
        self.mutex.lock()
        self.timer.stop()
        self.timer.start(self.delay)
        self.waitController.wait(self.mutex)

    def continue_(self):
        self.mutex.lock()
        self.timer.stop()
        self.waitController.wakeOne()
        self.mutex.unlock()

    def setAnimationDelay(self, delay):
        self.mutex.lock()
        self.delay = delay
        self.mutex.unlock()

    def handleLaberintoTerminado(self, e):
        if e:
            self.parent.laberintoResuelto()
        else:
            self.parent.laberintoIncompleto()

    def lock(self):
        self.mutex.lock()

    def unlock(self):
        self.mutex.unlock()

    ##### main del thread

    def run(self):
        while self.running:
            self.mutex.lock()
            self.waitWorker.wait(self.mutex)
            if self.running:
                self.solving = True
                self.res = self.laberinto.resolver()
                self.laberintoTerminado.emit(self.res)
                self.solving = False
            self.mutex.unlock()

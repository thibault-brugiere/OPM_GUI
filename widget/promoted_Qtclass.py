# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:38:47 2026

@author: tbrugiere
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
        
class WheelLabel(QLabel):

    wheelScrolled = Signal(int, float, float)  # delta, x, y

    def wheelEvent(self, event):

        delta = event.angleDelta().y()
        pos = event.position()  # QPointF

        self.wheelScrolled.emit(delta, pos.x(), pos.y())
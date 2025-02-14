# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:44:08 2025

@author: tbrugiere
"""

import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap

import _test_Function_UI as test

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QImage Viewer")

        # Création du QLabel pour afficher l'image
        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        # Création et affichage d'une QImage (image aléatoire)
        self.display_random_image()

    def display_random_image(self):
        """Crée une image en niveaux de gris et l'affiche."""
        
        qt_image = test.test_create_preview()
        
        self.label.setPixmap(QPixmap.fromImage(qt_image))

# Lancer l'application
app = QApplication(sys.argv)
window = ImageViewer()
window.show()
sys.exit(app.exec())
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:30:13 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic D:/Projets_Python/OPM_GUI/widget/ui_autofocus_02_03.ui -o D:/Projets_Python/OPM_GUI/widget/ui_autofocus_02_03.py

"""
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtGui import QPixmap, QImage

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from widget.ui_autofocus_02_03 import Ui_Form
from hardware.functions_piezo import piezo_SAS

parameters = {"original_piezo_position" : 15.880000,
              "best_piezo_position" : 15.881000,
              "max_intensity" : 20000,
              "R2" : 1.0,
              "quality" : True}

class autofocus_O2_O3_Window(QWidget, Ui_Form):
    """
    Show the window to set default channels
    """
    def __init__(self, piezo = None, graph = None, parameters = parameters):
        """
        preset_size : Array of preset sizes 
        """
        super().__init__()
        self.setupUi(self)
        self.piezo = piezo
        self.graph = graph
        self.parameters = parameters
        self.on_init()
        
    def on_init(self):
        
        self.setWindowTitle('Result autofocus O2 - O3')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        if __name__ == '__main__' :
            self.red_icon = QPixmap(os.path.join(parent_dir,  'Icons/Red_Light_Icon_On.png'))
            self.green_icon = QPixmap(os.path.join(parent_dir,  'Icons/Green_Light_Icon_On.png'))
        else :
            self.red_icon = QPixmap('Icons/Red_Light_Icon_On.png')
            self.green_icon = QPixmap('Icons/Green_Light_Icon_On.png')
        
        if self.parameters["quality"]:    
            self.label_autofocus_quality_icon.setPixmap(self.green_icon)
        else :
            self.label_autofocus_quality_icon.setPixmap(self.red_icon)
        
        if self.piezo is None :
            self.piezo = piezo_SAS()
        
        self.label_parameters.setText(
f""" Original position = {self.parameters["original_piezo_position"]:6f}
      Best position = {self.parameters["best_piezo_position"]:6f}
 Max intensity = {self.parameters["max_intensity"]:.1f}
 R² = {self.parameters["R2"]:.4f}""")

        
        self.create_graph_image()
        
        #
        # Connexion entre les boutons et les fonctions
        #
        self.pb_yes.clicked.connect(self.pb_yes_clicked)
        self.pb_no.clicked.connect(self.pb_no_clicked)
        
        self.accepted = False

    #
    # Functionsappelées par les boutons
    #
    def pb_yes_clicked(self):
        self.piezo.move_to(self.parameters["best_piezo_position"])
        self.accepted = True
    
    def pb_no_clicked(self):
        self.piezo.move_to(self.parameters["original_piezo_position"])
        self.accepted = True
    
    def create_graph_image(self):
        if self.graph is None :
            return
        graph = self.graph
        width = self.label_graph.width()
        height = self.label_graph.height()
        # dpi = graph.get_dpi()
        graph_width = 5
        graph_height = graph_width * height / width
        
        graph.set_size_inches(graph_width, graph_height)
        
        graph.tight_layout()
        graph.canvas.draw()
        rgba = graph.canvas.buffer_rgba()
        
        image = QImage(
            rgba,
            rgba.shape[1],
            rgba.shape[0],
            QImage.Format_RGBA8888
            )
        
        pixmap = QPixmap.fromImage(image)
        
        self.label_graph.setPixmap(
            pixmap.scaled(
                self.label_graph.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
                ))
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            if not self.accepted :
                self.pb_no_clicked()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.ignore()
        
if __name__ == '__main__':
    "To test the window"
    
    app = QApplication(sys.argv)
    
    editor = autofocus_O2_O3_Window()
    editor.show()
    sys.exit(app.exec())
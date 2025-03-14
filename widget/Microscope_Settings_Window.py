# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:41:33 2025

@author: tbrugiere
"""
"""
Convert file.ui to file.py

pyside6-uic widget/ui_microscope_settings.ui -o widget/ui_microscope_settings.py

"""
import os
import sys

from PySide6.QtCore import Qt,  QSize
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtGui import QIcon

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from widget.ui_microscope_settings import Ui_Form

class microscope_settings_window(QWidget, Ui_Form):
    """
    Show the window to microscope parameters
    """
    
    def __init__(self, microscope, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.microscope = microscope
        self.setupUi(self)
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('microscope parameters')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        #
        # Dictionnary creation
        #
       
        self.lineEdits = {'tilt_angle' : self.lineEdit_tilt_angle,
                     'mag_total' : self.lineEdit_mag_total,
                     'volts_per_um' : self.lineEdit_volts_per_um,
                     'galvo_response_time' : self.lineEdit_galvo_response_time,
                     'galvo_flyback_time' : self.lineEdit_galvo_flyback_time,
                     'laser_response_time' : self.lineEdit_laser_response_time,    
                     }
        
        self.microscope_params = {'tilt_angle' : self.microscope.tilt_angle,
                             'mag_total' : self.microscope.mag_total,
                             'volts_per_um' : self.microscope.volts_per_um,
                             'galvo_response_time' : self.microscope.galvo_response_time,
                             'galvo_flyback_time' : self.microscope.galvo_flyback_time,
                             'laser_response_time' : self.microscope.laser_response_time,    
                             }
        
        #
        # Initialisation of the lineEdits
        #
        
        for key in self.lineEdits.keys():
            self.lineEdits[key].editingFinished.connect(self.test_lineEdit)
        
        self.init_lineEdit()
        
    ####################################
    ## Functions called by line edits ##
    ####################################
    
    def init_lineEdit(self):
        for key in self.lineEdits.keys():
            self.lineEdits[key].blockSignals(True)
            self.lineEdits[key].setText(str(self.microscope_params[key]))
            self.lineEdits[key].blockSignals(False)
        
    def test_lineEdit(self):
        for key in self.lineEdits.keys():
            if self.lineEdits[key].text() == str(self.microscope_params[key]):
                pass
            else:
                try:
                    value = float(self.lineEdits[key].text())
                    self.microscope_params[key] = value
                except:
                    self.lineEdits[key].blockSignals(True)
                    self.lineEdits[key].setText(str(self.microscope_params[key]))
                    self.lineEdits[key].blockSignals(False)
                    
    def set_values(self):
        self.microscope.tilt_angle = self.microscope_params['tilt_angle']
        self.microscope.mag_total = self.microscope_params['mag_total']
        self.microscope.volts_per_um = self.microscope_params['volts_per_um']
        self.microscope.galvo_response_time = self.microscope_params['galvo_response_time']
        self.microscope.galvo_flyback_time = self.microscope_params['galvo_flyback_time']
        self.microscope.laser_response_time = self.microscope_params['laser_response_time']
                    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.set_values()
            self.parent().microscope = self.microscope
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
        
        
        #################################################################
        
if __name__ == '__main__':
    "To test the window"
    
    from configs.config import microscope
    
    app = QApplication(sys.argv)
    
    editor = microscope_settings_window(microscope())
    editor.show()
    sys.exit(app.exec())
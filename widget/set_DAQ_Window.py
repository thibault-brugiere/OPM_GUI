# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:40:34 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_set_DAQ.ui -o widget/ui_set_DAQ.py

TODO :

"""

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from widget.ui_set_DAQ import Ui_Form

class setDAQWindow(QWidget, Ui_Form):
    """
    Show the window to set channels
    """
    def __init__(self, daq_channels, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.daq_channels = daq_channels
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('set DAQ channels')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        self.lineEdit = {"galvo": self.lineEdit_galvo,
                        "camera_0": self.lineEdit_camera1,
                        "camera_1": self.lineEdit_camera2,
                        "405" : self.lineEdit_laser_405,
                        "488" : self.lineEdit_laser_488,
                        "561" : self.lineEdit_laser_561,
                        "640" : self.lineEdit_laser_640,
                        "laser_blanking" : self.lineEdit_laser_blanking
                        }
        
        for key in self.lineEdit.keys():
            self.lineEdit[key].setText(self.daq_channels[key])
            if self.daq_channels[key] is None:
                self.lineEdit[key].setText('None')
        
    
    def set_daq_channels(self):
        for key in self.lineEdit.keys():
            if self.lineEdit[key].text() == 'None':
                self.daq_channels[key] = None
            else:
                self.daq_channels[key] = self.lineEdit[key].text()
                
        # for key,value in self.daq_channels.items():
        #     if value is not None:
        #         print(key+value)
        #     else:
        #         print(key + "/None")
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            """Are you sure you want to apply the changes?
            If ou press Yes, settings in the main window will be erased""",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.set_daq_channels()
            self.parent().microscope.daq_channels = self.daq_channels
            self.parent().sync_laser_interface()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
    
if __name__ == '__main__':
    "To test the window"
    app = QApplication(sys.argv)
    daq_channels = {"galvo": "Dev1/ao0",
                    "camera_1": "Dev1/port0/line0",
                    "camera_2": None,
                    "405" : "Dev1/ao1",
                    "488" : None,
                    "561" : "Dev1/ao2",
                    "640" : "Dev1/ao3",
                    "laser_blanking" : "Dev1/port0/line3"
                    }
    
    editor = setDAQWindow(daq_channels)
    editor.show()
    sys.exit(app.exec())
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
    def __init__(self, daq_channels, daq_channels_laser_analog_out, daq_channels_laser_digital_out, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.daq_channels = daq_channels
        self.daq_channels_laser_analog_out = daq_channels_laser_analog_out
        self.daq_channels_laser_digital_out = daq_channels_laser_digital_out
        
        self.daq_channels_Dict = {
            "lineEdit" : self.daq_channels,
            "lineEdit_laser_analog_out" : self.daq_channels_laser_analog_out,
            "lineEdit_laser_digital_out" : self.daq_channels_laser_digital_out
            }
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('set DAQ channels')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        self.lineEdit = {"co_channel" : self.lineEdit_vol_trig,
                        "co_terminal" : self.lineEdit_vol_trig_outputt,
                        "galvo": self.lineEdit_galvo,
                        "camera_0": self.lineEdit_camera1,
                        "camera_1": self.lineEdit_camera2,
                        "filter_wheel_1" : self.lineEdit_filter_wheel_1,
                        "filter_wheel_2" : self.lineEdit_filter_wheel_2,
                        "channel_finished": self.lineEdit_ChannelFinished,
                        "laser_blanking" : self.lineEdit_laser_blanking,
                        }
        
        self.lineEdit_laser_analog_out = {
                        "405" : self.lineEdit_laser_ao_405,
                        "488" : self.lineEdit_laser_ao_488,
                        "561" : self.lineEdit_laser_ao_561,
                        "640" : self.lineEdit_laser_ao_640,
                        }
        
        self.lineEdit_laser_digital_out = {
                        "405" : self.lineEdit_laser_do_405,
                        "488" : self.lineEdit_laser_do_488,
                        "561" : self.lineEdit_laser_do_561,
                        "640" : self.lineEdit_laser_do_640,
                        }
        
        self.lineEditDict = {
            "lineEdit" : self.lineEdit,
            "lineEdit_laser_analog_out" : self.lineEdit_laser_analog_out,
            "lineEdit_laser_digital_out" : self.lineEdit_laser_digital_out
            }
        
        for lineEditkey in self.lineEditDict.keys():
            for key in self.lineEditDict[lineEditkey].keys():
                self.lineEditDict[lineEditkey][key].setText(self.daq_channels_Dict[lineEditkey][key])
                if self.daq_channels_Dict[lineEditkey][key] is None:
                    self.lineEditDict[lineEditkey][key].setText('None')
                
                
        
        # for key in self.lineEdit.keys():
        #     self.lineEdit[key].setText(self.daq_channels[key])
        #     if self.daq_channels[key] is None:
        #         self.lineEdit[key].setText('None')
                
        
    def set_daq_channels(self):
        # for key in self.lineEdit.keys():
        #     if self.lineEdit[key].text() == 'None':
        #         self.daq_channels[key] = None
        #     else:
        #         self.daq_channels[key] = self.lineEdit[key].text()
        
        for lineEditkey in self.lineEditDict.keys():
            for key in self.lineEditDict[lineEditkey].keys():
                if self.lineEditDict[lineEditkey][key].text() == 'None':
                    self.daq_channels_Dict[lineEditkey][key] = None
                else:
                    self.daq_channels_Dict[lineEditkey][key] = self.lineEditDict[lineEditkey][key].text()
        
    
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
            self.parent().microscope.daq_channels_laser_analog_out = self.daq_channels_laser_analog_out
            self.parent().microscope.daq_channels_laser_digital_out = self.daq_channels_laser_digital_out
            self.parent().sync_laser_interface()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
    
if __name__ == '__main__':
    "To test the window"
    app = QApplication(sys.argv)
    daq_channels = {"co_channel": "Dev1/ctr0", # ADD: trigger start of each volume
                    "co_terminal": "/Dev1/PFI0", # ADD: trigger start of each volume
                    "galvo": "Dev1/ao0", # Fait bouger le galvo pour le scanning
                    "camera_0": "Dev1/port0/line0", # Trigger l'exposition de la camera
                    "camera_1": "Dev1/port0/line1", # Trigger l'exposition de la deuxieme camera (si presente)
                    "filter_wheel_1": "Dev1/port0/line2", # Trigger de la roue de filtres
                    "filter_wheel_2": "Dev1/port0/line3", # Trigger de la roue de filtres
                    "channel_finished": "/Dev1/PFI1",
                    "laser_blanking" : "Dev1/port0/line4", # Trigger le blanking de l'AOTF du banc laser
                    }
    
    daq_channels_laser_analog_out = {"405" : "Dev1/ao1", # Régle la puissance du laser 405
                                     "488" : "Dev1/ao2",      # Régle la puissance du laser 488
                                     "561" : None, # Régle la puissance du laser 561
                                     "640" : "Dev1/ao3", # Régle la puissance du laser 640
                                     }
    
    daq_channels_laser_digital_out = {"405" : "Dev1/port0/Line8", # Régle digital modulation (dm) du laser 405
                                      "488" : "Dev1/port0/Line9", # Régle digital modulation (dm) du laser 488
                                      "561" : "Dev1/port0/Line10", # Régle digital modulation (dm) du laser 561
                                      "640" : "Dev1/port0/Line11", # Régle digital modulation (dm) du laser 640
                                      }
    
    editor = setDAQWindow(daq_channels, daq_channels_laser_analog_out, daq_channels_laser_digital_out)
    editor.show()
    sys.exit(app.exec())
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
        
        self.message_filters = ''
        
        #
        # Dictionnary creation
        #
        
        self.lineEdit_filters = [self.lineEdit_Filter1, self.lineEdit_Filter2, self.lineEdit_Filter3,
                                 self.lineEdit_Filter4, self.label_Filter5, self.lineEdit_Filter6]
       
        self.lineEdits = {'tilt_angle' : self.lineEdit_tilt_angle,
                     'mag_total' : self.lineEdit_mag_total,
                     'stage_port' : self.lineEdit_stage_port,
                     'trans_mirror_ser_num' : self.lineEdit_trans_mirror_ser_num,
                     'volts_per_um' : self.lineEdit_volts_per_um,
                     'galvo_response_time' : self.lineEdit_galvo_response_time,
                     'galvo_flyback_time' : self.lineEdit_galvo_flyback_time,
                     'laser_response_time' : self.lineEdit_laser_response_time,   
                     'Oxius_port' : self.lineEdit_OxxiusCombiner_port,
                     'filter_port' : self.lineEdit_Filter_port,
                     'filter_changing_time' : self.lineEdit_filter_changing_time,
                     'filter1' : self.lineEdit_Filter1,
                     'filter2' : self.lineEdit_Filter2,
                     'filter3' : self.lineEdit_Filter3,
                     'filter4' : self.lineEdit_Filter4,
                     'filter5' : self.lineEdit_Filter5,
                     'filter6' : self.lineEdit_Filter6
                     }
        
        self.microscope_params = {'tilt_angle' : self.microscope.tilt_angle,
                             'mag_total' : self.microscope.mag_total,
                             'stage_port' : self.microscope.stage_port,
                             'trans_mirror_ser_num' : self.microscope.trans_mirror_ser_num,
                             'volts_per_um' : self.microscope.volts_per_um,
                             'galvo_response_time' : self.microscope.galvo_response_time,
                             'galvo_flyback_time' : self.microscope.galvo_flyback_time,
                             'laser_response_time' : self.microscope.laser_response_time,
                             'Oxius_port' : self.microscope.OxxiusCombiner_port,
                             'filter_port' : self.microscope.filter_port,
                             'filter_changing_time' : self.microscope.filter_changing_time,
                             'filter1' : self.microscope.filters[0],
                             'filter2' : self.microscope.filters[1],
                             'filter3' : self.microscope.filters[2],
                             'filter4' : self.microscope.filters[3],
                             'filter5' : self.microscope.filters[4],
                             'filter6' : self.microscope.filters[5],
                             }
        
        self.param_type = {'tilt_angle' : 'float',
                           'mag_total' : 'float',
                           'stage_port' : 'str',
                           'trans_mirror_ser_num' : 'int',
                           'volts_per_um' : 'float',
                           'galvo_response_time' : 'float',
                           'galvo_flyback_time' : 'float',
                           'laser_response_time' : 'float',
                           'Oxius_port' : 'str',
                           'filter_port' : 'str',
                           'filter_changing_time' : 'float',
                           'filter1' : 'str',
                           'filter2' : 'str',
                           'filter3' : 'str',
                           'filter4' : 'str',
                           'filter5' : 'str',
                           'filter6' : 'str',
                           }
        
        self.param_filters = ['filter1','filter2','filter3','filter4','filter5','filter6']
        
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
            elif self.param_type[key] == 'float':
                try:
                    value = float(self.lineEdits[key].text())
                    self.microscope_params[key] = value
                except:
                    self.lineEdits[key].blockSignals(True)
                    self.lineEdits[key].setText(str(self.microscope_params[key]))
                    self.lineEdits[key].blockSignals(False)
            else:
                self.microscope_params[key] = self.lineEdits[key].text()
                if key in self.param_filters :
                    self.message_filters = """\n[WARNING]Changes has been made in filters,
you have to set changes in channels too"""
                    
    def set_values(self):
        self.microscope.tilt_angle = self.microscope_params['tilt_angle']
        self.microscope.mag_total = self.microscope_params['mag_total']
        self.microscope.stage_port = self.microscope_params['stage_port']
        self.microscope.trans_mirror_ser_num = self.microscope_params['trans_mirror_ser_num']
        self.microscope.volts_per_um = self.microscope_params['volts_per_um']
        self.microscope.galvo_response_time = self.microscope_params['galvo_response_time']
        self.microscope.galvo_flyback_time = self.microscope_params['galvo_flyback_time']
        self.microscope.laser_response_time = self.microscope_params['laser_response_time']
        self.microscope.OxxiusCombiner_port = self.microscope_params['Oxius_port']
        self.microscope.filter_port = self.microscope_params['filter_port']
        self.microscope.filter_changing_time = self.microscope_params['filter_changing_time']
        self.microscope.filters = [self.microscope_params['filter1'],
                                   self.microscope_params['filter2'],
                                   self.microscope_params['filter3'],
                                   self.microscope_params['filter4'],
                                   self.microscope_params['filter5'],
                                   self.microscope_params['filter6'],
                                   ]
                    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            f""""Are you sure you want to quit?\n{self.message_filters}""",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.set_values()
            try:
                self.parent().microscope = self.microscope
                self.parent().sync_filter_interface()
            except:
                pass
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
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:16:34 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_preset_ROI.ui -o widget/ui_preset_ROI.py

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

from Functions_UI import functions_ui

from widget.ui_preset_ROI import Ui_Form

class PresetROIWindow(QWidget, Ui_Form):
    """
    Show the window to set default channels
    """
    def __init__(self, preset_size, chipsize, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.preset_size = preset_size
        self.chipsize = chipsize
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Channels editor')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        self.combo_Box_update_options()
        self.spinBox_hsize.setMaximum(self.chipsize[0])
        self.spinBox_vsize.setMaximum(self.chipsize[1])
        
        #########################################
        ## Fonctions appelées pour les boutons ##
        #########################################
        
        self.spinBox_hsize.editingFinished.connect(self.spinBox_hsize_value_changed)
        self.spinBox_hpos.editingFinished.connect(self.spinBox_hpos_value_changed)
        self.spinBox_vsize.editingFinished.connect(self.spinBox_vsize_value_changed)
        self.spinBox_vpos.editingFinished.connect(self.spinBox_vpos_value_changed)
        self.pb_center_FOV.clicked.connect(self.pb_center_FOV_clicked)
        self.comboBox_size_preset.currentIndexChanged.connect(self.comboBox_size_preset_value_changed)
        
        self.pb_add_ROI.clicked.connect(self.pb_add_ROI_clicked)
        self.pb_remove_ROI.clicked.connect(self.pb_remove_ROI_clicked)

        """
    These functions update the selected camera's region of interest (ROI) parameters 
    based on user input from spin boxes.
    
    Each function retrieves the currently selected camera from `comboBox_camera` and updates 
    one of its four parameters accordingly:
    - `hsize`: Horizontal size of the ROI (`spinBox_hsize`).
    - `hpos`: Horizontal position of the ROI (`spinBox_hpos`).
    - `vsize`: Vertical size of the ROI (`spinBox_vsize`).
    - `vpos`: Vertical position of the ROI (`spinBox_vpos`).
    
    The updated values are stored in the `camera` dictionary, indexed by the camera's 
    current selection in `comboBox_camera`.
    """
    
    def spinBox_hsize_value_changed(self):
        'Horizontal size of the ROI'

        size = functions_ui.set_size(self.spinBox_hsize.value(),
                                     self.chipsize[0])
        
        self.spinBox_hsize.setValue(size)
        self.spinBox_hpos_value_changed()
        
    def spinBox_hpos_value_changed(self):
        'Horizontal position of the ROI'
        
        pos = self.spinBox_hpos.value()
        pos = functions_ui.set_pos(pos, self.spinBox_hsize.value(), self.chipsize[0])
    
        self.spinBox_hpos.setValue(pos)
        
    def spinBox_vsize_value_changed(self):
        'Vertical size of the ROI'
        size = functions_ui.set_size(self.spinBox_vsize.value(),
                                     self.chipsize[1])
        
        self.spinBox_vsize.setValue(size)
        self.spinBox_vpos_value_changed()
        
    def spinBox_vpos_value_changed(self):
        'Vertical position of the ROI'
        
        pos = self.spinBox_vpos.value()
        pos = functions_ui.set_pos(pos, self.spinBox_vsize.value(), self.chipsize[1])
    
        self.spinBox_vpos.setValue(pos)

        
    def pb_center_FOV_clicked(self):
        'Center the position of the ROI on the camera chip'
        
        self.spinBox_hpos.setValue(
            (self.chipsize[0] - self.spinBox_hsize.value())/2)
        
        self.spinBox_vpos.setValue(
            (self.chipsize[1] - self.spinBox_vsize.value())/2)
    
    def combo_Box_update_options(self):
        self.comboBox_size_preset.clear()
        self.comboBox_size_preset.addItems(self.preset_size)
    
    def comboBox_size_preset_value_changed(self):
        'set hpos and vpos to preset values'
        try:
            size = self.comboBox_size_preset.currentText()
            hsize, _ ,hpos, _ , vsize, _ ,vpos = size.split()
            
            self.spinBox_hsize.setValue(int(hsize))
            self.spinBox_hpos.setValue(int(hpos))
            self.spinBox_vsize.setValue(int(vsize))
            self.spinBox_vpos.setValue(int(vpos))
            
            self.spinBox_hsize_value_changed()
            self.spinBox_hpos_value_changed()
            self.spinBox_vsize_value_changed()
            self.spinBox_vpos_value_changed()
        except:
            pass
        
    def pb_add_ROI_clicked(self):
        new_size = str(self.spinBox_hsize.value()) + ' - ' + str(self.spinBox_hpos.value()) + ' - ' + str(self.spinBox_vsize.value()) + ' - ' + str(self.spinBox_vpos.value())
        self.preset_size.append(new_size)
        self.combo_Box_update_options()
        self.comboBox_size_preset.setCurrentText(new_size)
   
    def pb_remove_ROI_clicked(self):
        index  = self.comboBox_size_preset.currentIndex()
        self.preset_size.pop(index)
        self.combo_Box_update_options()
    
        ## Scanner
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            "Are you sure you want to apply the changes?\nIf ou press Yes, settings in the main window will be erased",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.parent().preset_size = self.preset_size
            self.parent().comboBox_size_preset_set_indexes()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
        
    # Ce bloc permet de tester la fenêtre ChannelEditorWindow indépendamment
if __name__ == '__main__':
    app = QApplication(sys.argv)
    chipsize = [4432 , 2368]
    preset_size = ['2048 - 0 x 1024 - 0', '2048 - 0 x 2048 - 0']
    
    editor = PresetROIWindow(preset_size, chipsize)
    editor.show()
    sys.exit(app.exec())
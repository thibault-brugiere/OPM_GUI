# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:30:13 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic D:/Projets_Python/OPM_GUI/widget/ui_alignement_O2_O3.ui -o D:/Projets_Python/OPM_GUI/widget/ui_alignement_O2_O3.py

"""
import os
import sys

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtGui import QIcon, QPixmap

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from hardware.functions_piezo import piezo_SAS
from hardware.functions_piezo import PiezoState
from widget.ui_alignement_O2_O3 import Ui_Form

class PiezoError(RuntimeError):
    "Error while using the Piezo"

class alignement_O2_O3_Window(QWidget, Ui_Form):
    """
    Show the window to set default channels
    """
    def __init__(self, parent=None, piezo = None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        self.piezo = piezo
        self.on_init()
        
    def on_init(self):
        
        self.setWindowTitle('alignement O2 - O3')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        #
        # Ajout des icones
        #
        
        self.pb_move = {'fw1' : self.pb_move_fw1, # Liste des push buttons
                   'fw10' : self.pb_move_fw10,
                   'bw1' : self.pb_move_bw1,
                   'bw10' : self.pb_move_bw10,
                   }
        
        icons = {'fw1' : 'Icons/Arrows_03.png', # Liste des icones
                 'fw10' : 'Icons/Arrows_04.png',
                 'bw1' : 'Icons/Arrows_02.png',
                 'bw10' : 'Icons/Arrows_01.png',
                 }

        for key in self.pb_move.keys():
            pb = self.pb_move[key]
            if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
                icon_path = os.path.join(parent_dir, icons[key])
            else:
                icon_path = icons[key]
                
            icon = QIcon(icon_path)
            
            pb.setText('')
            pb.setIcon(icon)
            pb.setIconSize(QSize(32,32))
        
        GLI_Icon = {'ON' : 'Icons/Green_Light_Icon_On.png',
               'OFF' : 'Icons/Green_Light_Icon_Off.png' }
        
        self.GLI_Pixmap = {'ON'  : None,
                    'OFF' : None}
        
        for key in GLI_Icon.keys() :
            if __name__ == "__main__":
                icon_path = os.path.join(parent_dir,  GLI_Icon[key])
            else :
                icon_path = GLI_Icon[key]
                
            self.GLI_Pixmap[key] = QPixmap(icon_path)
                
            
        self.label_piezo_referenced_icon.setPixmap(self.GLI_Pixmap["OFF"])
        
        if self.piezo is None :
            self.piezo = piezo_SAS()
            
        self.connected = self.piezo.connected
            
        self.piezo_position_timer = QTimer(self)
        self.piezo_position_timer.setInterval(500)  # ms
        self.piezo_position_timer.timeout.connect(self.get_position)
        
        self.devices = self.piezo.list_serial_ports() # Récupére la liste des devices disponibles
        self.set_comboBox_devices()
        self.comboBox_devices_indexChanged()
        self.step_size = 0.1
        
        
        #
        # Connexion entre les boutons et les fonctions
        #
        
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.spinBox_step_size.valueChanged.connect(self.spinBox_step_size_value_changed)
        self.slider_step_size.valueChanged.connect(self.slider_step_size_value_changed)
        
        # push buttons
        
        self.pb_piezo_reference.clicked.connect(self.pb_piezo_reference_clicked)
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_fw10.clicked.connect(self.pb_move_fw10_clicked)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        self.pb_move_bw10.clicked.connect(self.pb_move_bw10_clicked)

    #
    # Functionsappelées par les boutons
    #
    
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
        
    def comboBox_devices_indexChanged(self):
        """"set the self.port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.piezo.close()
        self.port = self.comboBox_devices.currentText()
        if self.port != 'None':
            try :
                self.piezo.change_port(self.port)
                self.piezo.connect()
            except :
                self.connected = False
                self.GLI_Pixmap["OFF"]
            
            self.connected = True
            state = self.piezo.get_status()
            if state == PiezoState.READY_OL:
                self.piezo.close_loop()
            elif state == PiezoState.READY_CL:
                pass
            else :
                raise PiezoError("Piezo is not in READY_CL or READY_OL state : {state}")
                
            if self.piezo.is_referenced():
                self.label_piezo_referenced_icon.setPixmap(self.GLI_Pixmap["ON"])
                self.label_piezo_referenced.setText("Referenced")
            
        self.tools_desactivation()
        self.set_label_connection()
        
    
    def spinBox_step_size_value_changed(self):
        """"set the step size in negative and positive direction in µm
        """
        self.step_size = self.spinBox_step_size.value()
        self.slider_step_size.blockSignals(True)
        self.slider_step_size.setValue(int(self.step_size * 1000))
        self.slider_step_size.blockSignals(False)
        
        
    def slider_step_size_value_changed(self):
        self.step_size = self.slider_step_size.value()/1000
        self.spinBox_step_size.blockSignals(True)
        self.spinBox_step_size.setValue(self.step_size)
        self.spinBox_step_size.blockSignals(True)
    
    # push buttons for movement
    
    def pb_piezo_reference_clicked(self):
        self.piezo.reference()
        self.get_position()
        if self.piezo.is_referenced():
            self.label_piezo_referenced_icon.setPixmap(self.GLI_Pixmap["OFF"])
            self.label_piezo_referenced.setText("Referenced")
    
    def pb_move_fw1_clicked(self):
        "Move forward of 1 step"
        self.piezo.move_by(self.step_size/1000)
        self.get_position()
        
    def pb_move_fw10_clicked(self):
        "Move forward of 5 steps"
        self.piezo.move_by(self.step_size * 5 / 1000)
        self.get_position()
        
    def pb_move_bw1_clicked(self):
        "Move backward of 1 step"
        self.piezo.move_by(- self.step_size / 1000)
        self.get_position()
        
    def pb_move_bw10_clicked(self):
        "Move backward 5 steps"
        self.piezo.move_by(- self.step_size * 5 / 1000)
        self.get_position()
        
        
    #
    # Autres fonctions
    #

    def get_position(self):
        "Get the current position of the device and display it"
        if self.connected :
            position = self.piezo.try_get_position()
            if position is not None :
                self.position = position
                self.lcdNumber_Position.display(self.position)

        
    def tools_desactivation(self):
        """activate and desactivate tools if depending on device connection"""
        if self.connected :
            inactive = False
            self.piezo_position_timer.start()
        else:
            inactive = True
            self.piezo_position_timer.stop()
        
        self.slider_step_size.setDisabled(inactive)
        self.spinBox_step_size.setDisabled(inactive)
        self.pb_piezo_reference.setDisabled(inactive)
        
        for pb in self.pb_move.values():
            pb.setDisabled(inactive)
            
        
    def set_label_connection(self):
        "set self.label_connection depending in the device connection"
        if self.connected :
            self.label_connection.setText('Connected')
            text_color = 'green'
        else:
            self.label_connection.setText('Not Connected')
            text_color = 'red'
            
        self.label_connection.setStyleSheet(f'color: {text_color}')
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.piezo.close()
            # self.position_timer.stop()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
        
if __name__ == '__main__':
    "To test the window"
    
    app = QApplication(sys.argv)
    
    editor = alignement_O2_O3_Window()
    editor.show()
    sys.exit(app.exec())
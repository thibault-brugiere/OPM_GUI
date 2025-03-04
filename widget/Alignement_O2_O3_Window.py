# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:30:13 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_alignement_O2_O3.ui -o widget/ui_alignement_O2_O3.py

TODO : Ajouter le réglage du step size

"""
import os
import sys
import time as t

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from Functions_Hardware import functions_super_agilis as piezzo
from widget.ui_alignement_O2_O3 import Ui_Form

class alignement_O2_O3_Window(QWidget, Ui_Form):
    """
    Show the window to set default channels
    """
    def __init__(self, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        self.on_init()
        
    def on_init(self):
        
        self.setWindowTitle('alignement O2 - O3')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        self.devices = piezzo.list_serial_ports() # Récupére la liste des devices disponibles
        self.set_comboBox_devices()
        self.comboBox_devices_indexChanged()
        
        #
        # Connexion entre les boutons et les fonctions
        #
        
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.spinBox_step_size.editingFinished.connect(self.spinBox_step_size_value_changed)
        self.slider_step_size.sliderReleased.connect(self.spinBox_step_size_value_changed)
        
        # push buttons
        
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_fw10.clicked.connect(self.pb_move_fw10_clicked)
        self.pb_move_fwj1.pressed.connect(self.pb_move_fwj1_pressed)
        self.pb_move_fwj1.released.connect(self.pb_move_jog_released)
        self.pb_move_fwj2.pressed.connect(self.pb_move_fwj2_pressed)
        self.pb_move_fwj2.released.connect(self.pb_move_jog_released)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        self.pb_move_bw10.clicked.connect(self.pb_move_bw10_clicked)
        self.pb_move_bwj1.pressed.connect(self.pb_move_bwj1_pressed)
        self.pb_move_bwj1.released.connect(self.pb_move_jog_released)
        self.pb_move_bwj2.pressed.connect(self.pb_move_bwj2_pressed)
        self.pb_move_bwj2.released.connect(self.pb_move_jog_released)
        
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
        self.port = self.comboBox_devices.currentText() 
        if self.port != 'None':
            port_ok = self.test_port()
            if port_ok:
                self.connected = True
                self.initialize()
            else:
                self.connected = False
        else :
            self.connected = False
            
        self.tools_desactivation()
        self.set_label_connection()
        
    
    def spinBox_step_size_value_changed(self):
        """"set the step size in negative and positive direction
        21% seems to be the minimum"""
        step_size = self.spinBox_step_size.value()
        command = 'XU-' + str(step_size) + ', ' + str(step_size)
        piezzo.send_command(command, self.port)
        t.sleep(0.01)
    
    # push buttons for movement
    
    def pb_move_fw1_clicked(self):
        "Move forward of 1 step"
        piezzo.send_command('XR1', self.port)
        t.sleep(0.01)
        self.get_position()
        
    def pb_move_fw10_clicked(self):
        "Move forward of 10 steps"
        piezzo.send_command('XR10', self.port)
        t.sleep(0.01)
        self.get_position()
        
    def pb_move_fwj1_pressed(self):
        "Move forward jogging at 50 steps/s"
        piezzo.send_command('JA1', self.port)
        
    def pb_move_fwj2_pressed(self):
        "Move forward jogging at 1000 steps/s"
        piezzo.send_command('JA2', self.port)
        
    def pb_move_bw1_clicked(self):
        "Move backward of 1 step"
        piezzo.send_command('XR-1', self.port)
        t.sleep(0.01)
        self.get_position()
        
    def pb_move_bw10_clicked(self):
        "Move backward of 10 steps"
        piezzo.send_command('XR-10', self.port)
        t.sleep(0.01)
        self.get_position()
        
    def pb_move_bwj1_pressed(self):
        "Move backward jogging at 50 steps/s"
        piezzo.send_command('JA-1', self.port)
        
    def pb_move_bwj2_pressed(self):
        "Move backward jogging at 1000 steps/s"
        piezzo.send_command('JA-2', self.port)
        
    def pb_move_jog_released(self):
        "Stop move jogging"
        piezzo.send_command('ST', self.port)
        t.sleep(0.01)
        self.get_position() 
        
    #
    # Autres fonctions
    #

    def get_position(self):
        "Get the current position of the device and display it"
        position = piezzo.send_command_response('TP', self.port)
        position = float(position[2:])
        self.position = position
        self.lcdNumber_Position.display(self.position)
        
    def test_port(self):
        "Test if the current port is the right device"
        ID = piezzo.send_command_response('ID?', self.port)
        t.sleep(0.01)
        if ID == 'IDCONEX-SAG-LS16P':
            port_ok = True
        else:
            port_ok = False
        
        return port_ok
        
    def tools_desactivation(self):
        """activate and desactivate tools if depending on device connection"""
        if self.connected :
            inactive = False
        else:
            inactive = True
        
        self.slider_step_size.setDisabled(inactive)
        self.spinBox_step_size.setDisabled(inactive)
        
        self.pb_move_fw1.setDisabled(inactive)
        self.pb_move_fw10.setDisabled(inactive)
        self.pb_move_fwj1.setDisabled(inactive)
        self.pb_move_fwj2.setDisabled(inactive)
        self.pb_move_bw1.setDisabled(inactive)
        self.pb_move_bw10.setDisabled(inactive)
        self.pb_move_bwj1.setDisabled(inactive)
        self.pb_move_bwj2.setDisabled(inactive)
        
    def initialize(self):
        self.spinBox_step_size_value_changed() # Set step size
        piezzo.send_command('XF1000', self.port) # set step frequancy to 1000 Hz, to set step size < 100%
        t.sleep(0.01)
        self.get_position()
        
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
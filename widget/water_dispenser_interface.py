# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:10:05 2026

@author: tbrugiere

pyside6-uic D:/Projets_Python/OPM_GUI/widget/ui_water_dispenser.ui -o D:/Projets_Python/OPM_GUI/widget/ui_water_dispenser.py

"""
import os
import sys
import time as t

from PySide6.QtCore import QThread, Signal, Qt, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap

# if __name__ == "__main__" and (__package__ is None or __package__ == ""):
#     # Lancement en script : on relance en module pour activer les imports relatifs
#     import sys
#     from pathlib import Path

#     pkg_root = Path(__file__).resolve().parent  # dossier qui contient multidimensional_acquisition/
#     sys.path.insert(0, str(pkg_root))
    
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from widget.ui_water_dispenser import Ui_Form
from hardware.WaterDispenser import WaterDispenser


class PositionMonitor(QThread):
    """
    Periodically read the motor position.

    Signals
    -------
    position_received : Signal(int)
        Emitted when a new motor position is received.
    communication_error : Signal(str)
        Emitted when communication with the Arduino fails.
    """

    position_received = Signal(int)
    motion_recieved = Signal(str)
    communication_error = Signal(str)

    def __init__(
        self,
        controller,
        interval_ms: int = 100,
        parent=None,
    ):
        super().__init__(parent)

        self.controller = controller
        self.interval_ms = interval_ms

    def run(self) -> None:
        """Periodically query the motor position."""
        while not self.isInterruptionRequested():
            if self.controller.connected :
                try:
                    position = self.controller.get_pos()
                    self.position_received.emit(position)
                    
                    motion = self.controller.get_motion()[0]
                    self.motion_recieved.emit(motion)
    
                except Exception as exc:
                    self.communication_error.emit(str(exc))

            self.msleep(self.interval_ms)

class Water_Dispenser_window(QWidget, Ui_Form):
    """
    """
    
    def __init__(self,
                 wd = None, #Water dispenser
                 port = "COM8",
                 parent = None):
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.port = port
        
        if wd is not None :
            self.wd = wd
        else :
            self.wd = WaterDispenser()
            
        self.position = 0
        self.wd_connected = False
        
        #
        # Position monitor
        #
        
        self.position_monitor = PositionMonitor(controller = self.wd,
                                                interval_ms = 100)
        
        self.position_monitor.position_received.connect(self.update_position)
        self.position_monitor.motion_recieved.connect(self.update_motion)
        self.position_monitor.communication_error.connect(self.handle_communication_error)
    
        self.position_monitor.start()
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Water Dispenser')
        
        #
        # Ajout des icones
        #
        
        if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
            self.fw1_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_03.png'))
            self.fw10_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_04.png'))
            self.bw1_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_02.png'))
            self.bw10_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_01.png'))
            self.Red_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_On.png'))
            self.Red_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_Off.png'))
            self.Green_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_On.png'))
            self.Green_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_Off.png'))
        else:
            self.fw1_icon = QPixmap('Icons/Arrows_03.png')
            self.fw10_icon = QPixmap('Icons/Arrows_04.png')
            self.bw1_icon = QPixmap('Icons/Arrows_02.png')
            self.bw10_icon = QPixmap('Icons/Arrows_01.png')
            self.Red_Light_Icon_On = QPixmap('Icons/Red_Light_Icon_On.png')
            self.Red_Light_Icon_Off = QPixmap('Icons/Red_Light_Icon_Off.png')
            self.Green_Light_Icon_On = QPixmap('Icons/Green_Light_Icon_On.png')
            self.Green_Light_Icon_Off = QPixmap('Icons/Green_Light_Icon_Off.png')
        
        #
        # Parameters
        #
        
        self.step_size_um = 0.100 # Step size in µm
        
        #
        # Detect material
        #
        
        self.devices = self.wd.list_serial_ports() # Récupére la liste des devices disponibles
        
        self.set_comboBox_devices()
            
        self.pb_move_fw1.setText('')
        self.pb_move_fw1.setIcon(self.fw1_icon)
        self.pb_move_fw10.setText('')
        self.pb_move_fw10.setIcon(self.fw10_icon)
        self.pb_move_bw1.setText('')
        self.pb_move_bw1.setIcon(self.bw1_icon)
        self.pb_move_bw10.setText('')
        self.pb_move_bw10.setIcon(self.bw10_icon)
        self.label_moving.setPixmap(self.Red_Light_Icon_Off)
        
        self.tools_desactivation() # TODO réécrire cette fonction
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_fw10.pressed.connect(self.pb_move_fw10_pressed)
        self.pb_move_fw10.released.connect(self.stop_motion)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        self.pb_move_bw10.pressed.connect(self.pb_move_bw10_pressed)
        self.pb_move_bw10.released.connect(self.stop_motion)
        self.spinBox_speed.editingFinished.connect(self.crawl)
        self.pb_start_stop.clicked.connect(self.crawl)
        self.pb_Reload.clicked.connect(self.pb_reload_clicked)
        
    #
    # Functions called by buttons
    #
    
    
    def try_wd(self):
        "Try to connect the piezo witout the setting the port"
        if not self.wd.connected :
            try :
                self.wd.connect()
                self.wd_connected = True
            except :
                pass
            
        if self.wd.connected :
            self.comboBox_devices.setCurrentText(self.wd.port)
            self.comboBox_devices.setEnabled(False)
            
        self.tools_desactivation()
        self.set_label_connection()
            
    def comboBox_devices_indexChanged(self):
        """"set the self.piezo_port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.wd.close()
        port = self.comboBox_devices.currentText() 
        if port != 'None':
            try :
                self.wd.change_port(port)
                self.wd.connect()
                self.wd_connected = True
                self.comboBox_devices.setDisabled(True)
            except :
                self.wd_connected = False
                return
        
        self.tools_desactivation()
        self.set_label_connection()
    
    def tools_desactivation(self):
        desactivation = not self.wd_connected
            
        # self.pb_move_bw1.setDisabled(desactivation)
        # self.pb_move_bw10.setDisabled(desactivation)
        # self.pb_move_fw1.setDisabled(desactivation)
        # self.pb_move_fw10.setDisabled(desactivation)
        # self.pb_start_stop.setDisabled(desactivation)
        
    def pb_move_fw1_clicked(self):
        "Move forward of 1 step"
        self.move_step(1)
        
    def pb_move_fw10_pressed(self):
        self.move_jog(1)
    
    def pb_move_bw1_clicked(self):
        "Move forward of 1 step"
        self.move_step(0)
    
    def pb_move_bw10_pressed(self):
        self.move_jog(0)
        
    def move_step(self, direction):
        if self.wd_connected :
            amount = self.spinBox_step_size.value()
            step = amount / self.wd.ul_per_step
            self.wd.move(step, 500, direction)
    
    def move_jog(self, direction):
        if self.wd_connected :
            amount = self.spinBox_step_size.value()
            step = amount / self.wd.ul_per_step / 10
            self.wd.run(step, direction)
        
        
    def stop_motion(self):
        if self.wd_connected :
            self.wd.stop()
        
    def crawl(self):
        if self.wd_connected :
            if self.pb_start_stop.isChecked():
                flow = self.spinBox_speed.value() / 60 # µl/s
                interval_ms = self.wd.ul_per_step / flow * 1000
                
                self.wd.crawl(interval_ms, 1)
            else :
                self.wd.stop()
            
    def pb_reload_clicked(self):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Do you want to reload water dispenser?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes)
        if reply == QMessageBox.Yes :
            self.wd.run(40000,0)
            
        
    def set_label_connection(self):
        "set self.label_connection depending in the device connection"
        if self.wd_connected :
            self.label_connection.setText('Connected')
            text_color = 'green'
        else:
            self.label_connection.setText('Not Connected')
            text_color = 'red'
            
        self.label_connection.setStyleSheet(f'color: {text_color}')
    
    #
    # Stabilization and display
    #
    
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
    
    def update_position(self, position):
        self.lcdNumber_Position.display(position)
    
    def update_motion(self, motion):
        if motion == "STOP" :
            self.label_moving.setPixmap(self.Green_Light_Icon_Off)
            self.pb_start_stop.setChecked(False)
            
        if motion == "MOVE" :
            self.label_moving.setPixmap(self.Red_Light_Icon_On)
            self.pb_start_stop.setChecked(False)
            
        if motion == "RUN" :
            self.label_moving.setPixmap(self.Green_Light_Icon_On)
            self.pb_start_stop.setChecked(False)
            
        if motion == "CRAWL" :
            self.label_moving.setPixmap(self.Green_Light_Icon_On)
            self.pb_start_stop.setChecked(True)
            
    def handle_communication_error(self, signal):
        # print(f'communication error {signal}')
        return
            
    def closeEvent(self, event):
        """Stop worker threads before closing the window."""
    
        try:
            self.wd.stop()
            self.wd.close()
    
        finally:
            event.accept()
    
    def _on_close(self):
        pass
    
##############################################################################
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    editor = Water_Dispenser_window()
    editor.show()
    sys.exit(app.exec())
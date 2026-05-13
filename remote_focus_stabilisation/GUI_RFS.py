# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:57:20 2026

@author: tbrugiere
"""
"""
Convert file.ui to file.py

pyside6-uic widget/ui_channel_editor.ui -o widget/ui_channel_editor.py

pyside6-uic D:/Projets_Python/OPM_GUI/remote_focus_stabilisation/ui_RFS.ui -o D:/Projets_Python/OPM_GUI/remote_focus_stabilisation/ui_RFS.py

"""

import atexit
import numpy as np
import os
from pylablib.devices import Thorlabs
import sys
import time as t

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, QImage

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from remote_focus_stabilisation.ui_RFS import Ui_Form
from remote_focus_stabilisation.main_stabilisation import remote_focus_stabilisation
from hardware.functions_super_agilis import functions_super_agilis as piezzo

from Functions_UI import functions_ui

class RFS_window(QWidget, Ui_Form):
    """
    """
    
    start_calibration = Signal()
    
    def __init__(self, camera_sn = '36805', NIDAQ_out = "Dev1/port0/Line13", piezzo_step = [4,47], parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        
        self.camera_sn = camera_sn
        self.NIDAQ_out = NIDAQ_out
        self.piezzo_step = piezzo_step # Values for the same and minimum piezzo step (~200nm)
        
        #
        # Stabilization worker
        #
        
        self.stabilisation = remote_focus_stabilisation(camera_sn = camera_sn,
                                                        NIDAQ_out = NIDAQ_out)
        self.stabilisationThread = QThread()
        self.stabilisation.moveToThread(self.stabilisationThread)
        self.stabilisation.new_data.connect(self.store_frame) # Channel received   
        self.stabilisationThread.started.connect(self.stabilisation.on_init)
        
        self.start_calibration.connect(self.stabilisation.calibration)
        
        self.stabilisationThread.start()
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Active Remote Focus Stabilization')
        
        #
        # Parameters
        #
        
        self.step_size = 100
        
        self.preview_frame = None # frame actually displayed

        self.is_preview = True
        self.is_preview_paused = False
        self.look_up_table = 'grayscale'
        self.min_grayscale = 0
        self.max_grayscale = 1023
        self.preview_zoom = 0.5
        
        self.piezzo_port = None
        self.piezzo_connected = False # Connexion of the piezzo
        self.piezzo_position = 0.0 # Position of the piezzo in µm
        
        #
        # Detect material
        #
        
        self.devices = piezzo.list_serial_ports() # Récupére la liste des devices disponibles
        self.set_comboBox_devices()
        self.comboBox_devices_indexChanged()

        #
        # Ajout des icones
        #
        
        if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
            self.fw1_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_03.png'))
            self.bw1_icon = QPixmap(os.path.join(parent_dir, 'Icons/Arrows_02.png'))
            self.Red_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_On.png'))
            self.Red_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_Off.png'))
            self.Green_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_On.png'))
            self.Green_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_Off.png'))
        else:
            self.fw1_icon = QPixmap('Icons/Arrows_03.png')
            self.bw1_icon = QPixmap('Icons/Arrows_02.png')
            self.Red_Light_Icon_On = QPixmap('Icons/Red_Light_Icon_On.png')
            self.Red_Light_Icon_Off = QPixmap('Icons/Red_Light_Icon_Off.png')
            self.Green_Light_Icon_On = QPixmap('Icons/Green_Light_Icon_On.png')
            self.Green_Light_Icon_Off = QPixmap('Icons/Green_Light_Icon_Off.png')
            
        self.pb_move_fw1.setText('')
        self.pb_move_fw1.setIcon(self.fw1_icon)
        self.pb_move_bw1.setText('')
        self.pb_move_bw1.setIcon(self.bw1_icon)
        self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
        self.label_stabilize_icon.setPixmap(self.Green_Light_Icon_Off)
        
        self.tools_desactivation()
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
        self.pb_laser_on.clicked.connect(self.pb_laser_on_clicked)
        self.pb_stabilize.clicked.connect(self.pb_stabilize_clicked)
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.pb_calibrate.clicked.connect(self.pb_calibrate_clicked)
        self.sb_step_size.valueChanged.connect(self.sb_step_size_value_changed)
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        # Combo box grayscale
        self.cb_preview_zoom.currentIndexChanged.connect(self.cb_preview_zoom_index_changed)
        self.sb_min_grayscale.valueChanged.connect(self.sb_grayscale_value_changed)
        self.sb_max_grayscale.valueChanged.connect(self.sb_grayscale_value_changed)
        self.pb_minmax_grayscale.clicked.connect(self.pb_minmax_grayscale_clicked)
        self.pb_auto_grayscale.clicked.connect(self.pb_auto_grayscale_clicked)
        self.pb_reset_grayscale.clicked.connect(self.pb_resset_grayscale_clicked)
        
    #
    # Functions called by buttons
    #
    
    def pb_laser_on_clicked(self):
        if self.pb_laser_on.isChecked():
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_On)
            self.label_laser.setText('ON ')
        else :
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
            self.label_laser.setText('OFF')
    
    def pb_stabilize_clicked(self):
        if self.pb_stabilize.isChecked():
            self.label_stabilize_icon.setPixmap(self.Green_Light_Icon_On)
            self.label_stabilize.setText('ON ')
        else :
            self.label_stabilize_icon.setPixmap(self.Green_Light_Icon_Off)
            self.label_stabilize.setText('OFF')
            
    def comboBox_devices_indexChanged(self):
        """"set the self.piezzo_port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.piezzo_port = self.comboBox_devices.currentText() 
        if self.piezzo_port != 'None':
            port_ok = self.test_port()
            if port_ok:
                self.piezzo_connected = True
                t.sleep(0.01)
                self.get_position()
                self.stabilisation.set_piezzo_port(self.piezzo_port)
                
            else:
                self.piezzo_connected = False
                print("not connected")
        else :
            self.piezzo_connected = False
        
        self.tools_desactivation()
        self.set_label_connection()
        self.set_step_size()
    
    def pb_calibrate_clicked(self):
        self.start_calibration.emit()
            
    def sb_step_size_value_changed(self):
        """"set the step size in negative and positive direction
        21% seems to be the minimum for forward
        """
        self.step_size = self.sb_step_size.value()
        
    def pb_move_fw1_clicked(self):
        "Move forward of 1 step"
        piezzo.send_command('XR1', self.piezzo_port)
        t.sleep(0.01)
        self.get_position()
    
    def pb_move_bw1_clicked(self):
        "Move backward of 1 step"
        piezzo.send_command('XR-1', self.piezzo_port)
        t.sleep(0.01)
        self.get_position()
    
    def cb_preview_zoom_index_changed(self):
        zoom_list = [0.5,0.5,1,2,3,4]
        self.preview_zoom = zoom_list[self.cb_preview_zoom.currentIndex()]
        
        self.update_preview()
    
    def sb_grayscale_value_changed(self):
        """Update grayscale min/max values ensuring min < max."""
        
        # Retrieve the current values from the spin boxes
        self.min_grayscale = self.sb_min_grayscale.value()
        self.max_grayscale = self.sb_max_grayscale.value()
        
        # Ensure that min_grayscale is always strictly less than max_grayscale
        if self.min_grayscale >= self.max_grayscale:
            self.min_grayscale = self.max_grayscale - 1 # Adjust min_grayscale
            
            # Update the spin box value while blocking signals to avoid infinite loops
            self.sb_min_grayscale.blockSignals(True)
            self.sb_min_grayscale.setValue(self.min_grayscale)
            self.sb_min_grayscale.blockSignals(False)
            
            # Update the slider value similarly
            self.slider_min_grayscale.blockSignals(True)
            self.slider_min_grayscale.setValue(self.min_grayscale)
            self.slider_min_grayscale.blockSignals(False)
            
            self.update_preview()
    
    def pb_minmax_grayscale_clicked(self):
        if self.preview_frame is not None:
            frame = self.preview_frame
            self.sb_min_grayscale.setValue(np.min(frame))
            self.sb_max_grayscale.setValue(np.max(frame))
        else:
            pass
        
    def pb_auto_grayscale_clicked(self):
        """Automatically adjust grayscale values using auto contrast."""
        if self.preview_frame is not None :
            frame = self.preview_frame
            min_gray, max_gray = functions_ui.auto_contrast(frame)
            
            self.sb_min_grayscale.setValue(min_gray)
            self.sb_max_grayscale.setValue(max_gray)
            
    def pb_resset_grayscale_clicked(self):
        """Reset grayscale values to full dynamic range (0–4095)."""
        self.sb_min_grayscale.setValue(0)
        self.sb_max_grayscale.setValue(1023)
        
    #
    # Others functions
    #
    
    def get_position(self):
        "Get the current position of the device and display it"
        position = piezzo.send_command_response('TP', self.piezzo_port)
        position = float(position[2:])
        position = 1000 * position
        self.piezzo_position = position
        self.lcdNumber_Position.display(self.piezzo_position)
        
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
        
    def test_port(self):
        "Test if the current port is the right device"
        ID = piezzo.send_command_response('ID?', self.piezzo_port)
        t.sleep(0.01)
        if ID == 'IDCONEX-SAG-LS16P':
            port_ok = True
        else:
            port_ok = False
        
        return port_ok
        
    def tools_desactivation(self):
        if self.piezzo_connected :
            inactive = False
        else:
            inactive = True
        
        self.slider_step_size.setDisabled(inactive)
        self.pb_move_bw1.setDisabled(inactive)
        self.pb_move_fw1.setDisabled(inactive)
        
    def set_label_connection(self):
        "set self.label_connection depending in the device connection"
        if self.piezzo_connected :
            self.label_connection.setText('Connected')
            text_color = 'green'
        else:
            self.label_connection.setText('Not Connected')
            text_color = 'red'
            
        self.label_connection.setStyleSheet(f'color: {text_color}')
        
    def set_step_size(self):
        """
        Steps size sets to get the same and minimum moovement in 

        Parameters
        ----------
        backward : TYPE, optional
            DESCRIPTION. The default is 4.
        forward : TYPE, optional
            DESCRIPTION. The default is 43.

        Returns
        -------
        None.

        """
        backward = self.piezzo_step[0] # Values for the same and minimum step (~200nm)
        forward = self.piezzo_step[1]
        
        piezzo.send_command('OL')
        t.sleep(0.01)
        piezzo.send_command('XF1000', self.piezzo_port) # set step frequancy to 1000 Hz, to set step size < 100%
        t.sleep(0.01)
        command = 'XU-' + str(backward) + ',' + str(forward)
        piezzo.send_command(command, self.piezzo_port)
        t.sleep(0.01)
    
    #
    # Stabilization and display
    #
    
    def store_frame(self, frame, data):
        """Receive a frame from the camera thread and store it (unless paused)."""
        if not self.is_preview_paused :
            self.preview_frame = frame
            self.preview_data = data
            self.update_preview()
    
    def update_preview(self):
        """Display the most recent frame in the GUI."""
        if self.is_preview and self.preview_frame is not None :
            qt_image = functions_ui.create_preview(self.preview_frame,
                                                   self.look_up_table,
                                                   self.min_grayscale,
                                                   self.max_grayscale,
                                                   self.preview_zoom)
            
            label_w = self.label_image_preview.width()
            label_h = self.label_image_preview.height()

            img_w = qt_image.width()
            img_h = qt_image.height()
            
            x0 = max((img_w - label_w) // 2, 0)
            y0 = max((img_h - label_h) // 2, 0)
            
            cropped = qt_image.copy(x0, y0, label_w, label_h)
            
            self.label_image_preview.setPixmap(QPixmap.fromImage(cropped))
            self.label_message.setText(f'camera connected : {self.preview_data["camera_connected"]}')
            self.label_message.adjustSize()
            
        elif self.preview_frame is None :
            self.label_image_preview.setText("No image!")
            self.label_message.setText(f'camera connected : {self.preview_data["camera_connected"]}')
            self.label_message.adjustSize()
            
    def closeEvent(self, event):
        """Stop worker threads before closing the window."""
    
        try:
    
            if hasattr(self, "stabilisationThread"):
                self.stabilisationThread.quit()
                self.stabilisationThread.wait()
    
        finally:
            event.accept()
    
    def _on_close(self):
        pass
    
##############################################################################
if __name__ == '__main__':
    
    
    
    app = QApplication(sys.argv)

    editor = RFS_window()
    editor.show()
    sys.exit(app.exec())
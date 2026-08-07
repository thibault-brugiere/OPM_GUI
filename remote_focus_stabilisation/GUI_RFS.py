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
import sys
import time as t

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

from PySide6.QtCore import QTimer, QThread, Signal, Qt, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from remote_focus_stabilisation.ui_RFS import Ui_Form
from remote_focus_stabilisation.Tools.plots import create_stabilisation_plot
from remote_focus_stabilisation.main_stabilisation import remote_focus_stabilisation
from hardware.functions_piezo import piezo_SAS as piezo
from hardware.functions_piezo import PiezoState
from hardware.functions_DAQ import functions_daq

from Functions_UI import functions_ui

class PiezoError(RuntimeError):
    "Error while using the Piezo"

class RFS_window(QWidget, Ui_Form):
    """
    """
    
    start_calibration = Signal()
    start_timelaps = Signal()
    stop_timelaps = Signal()
    start_stabilisation = Signal()
    stop_stabilisation = Signal()
    
    def __init__(self, camera_sn = '36805',
                 piezo_port = None,
                 NIDAQ_out = "Dev1/port0/Line13",
                 folder_path = None,
                 message = True,
                 parent = None):
        
        super().__init__(parent)
        self.setupUi(self)
        
        
        self.camera_sn = camera_sn
        self.piezo_port = piezo_port
        self.NIDAQ_out = NIDAQ_out
        self.folder_path = folder_path
        
        self.piezo = piezo()
        
        #
        # Check the DAQ connection
        #
        
        self.connected_daq = functions_daq.get_connected_daq_devices()

        if len(self.connected_daq) == 0 :
            print('WARNING: No ni-DAQ detected ! laser might be off')
        
        functions_daq.digital_out(False, self.NIDAQ_out) # Force the transmission light OFF
        
        #
        # Stabilization worker
        #
        
        if self.folder_path is None :
            self.stabilisation = remote_focus_stabilisation(camera_sn = camera_sn,
                                                        NIDAQ_out = NIDAQ_out,
                                                        message = message,
                                                        piezo = self.piezo)
        else :
            self.stabilisation = remote_focus_stabilisation(camera_sn = camera_sn,
                                                        NIDAQ_out = NIDAQ_out,
                                                        folder_path=self.folder_path,
                                                        message = message,
                                                        piezo = self.piezo)
            
        self.stabilisationThread = QThread()
        self.stabilisationThread.setObjectName("stabilisationThread")
        self.stabilisation.moveToThread(self.stabilisationThread)
        self.stabilisationThread.started.connect(self.stabilisation.on_init)
        
        self.stabilisation.new_data.connect(self.store_frame) # Channel received
        self.stabilisation.new_stabilisation.connect(self.update_graph)
        
        self.start_calibration.connect(self.stabilisation.start_calibration)
        self.start_timelaps.connect(self.stabilisation.timelaps)
        self.stop_timelaps.connect(self.stabilisation.stop_timelaps,
                                   Qt.DirectConnection)
        self.start_stabilisation.connect(self.stabilisation.stabilisation)
        self.stop_stabilisation.connect(self.stabilisation.stop_stabilisation,
                                        Qt.DirectConnection)
        
        self.stabilisationThread.start()
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Active Remote Focus Stabilization')
        
        #
        # Parameters
        #
        
        self.step_size_um = 0.100 # Step size in µm
        
        self.preview_frame = None # frame actually displayed

        self.look_up_table = 'grayscale'
        self.min_grayscale = 0
        self.max_grayscale = 1023
        self.preview_zoom = 0.5
        
        self.piezo_connected = False # Connexion of the piezo
        
        self.laser_on = False
        self.calibrated = False
        
        # Data for the graph
        self.timer_graph = QElapsedTimer()
        self.timer_graph.start()
        self.displacements = []
        self.piezo_displacements = []
        
        #
        # Detect material
        #
        
        self.devices = piezo.list_serial_ports() # Récupére la liste des devices disponibles
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
        self.label_timelaps_icon.setPixmap(self.Green_Light_Icon_Off)
        self.label_piezo_referenced_icon.setPixmap(self.Green_Light_Icon_Off)
        
        
        self.tools_desactivation()
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        self.pb_saving.clicked.connect(self.pb_saving_clicked)
        self.pb_laser_on.clicked.connect(self.pb_laser_on_clicked)
        self.pb_stabilize.clicked.connect(self.pb_stabilize_clicked)
        self.pb_timelaps.clicked.connect(self.pb_timelaps_clicked)
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.pb_piezo_reference.clicked.connect(self.pb_piezo_reference_clicked)
        self.slider_step_size.valueChanged.connect(self.slider_step_size_value_changed)
        self.sb_step_size.valueChanged.connect(self.sb_step_size_value_changed)
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        self.pb_calibrate.clicked.connect(self.pb_calibrate_clicked)
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
    def pb_saving_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        if folder is not None :
            self.stabilisation.folder = folder

            self.label_saving.setText(folder)
    
    def pb_laser_on_clicked(self):
        if self.pb_laser_on.isChecked():
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_On)
            self.label_laser.setText('ON ')
            functions_daq.digital_out(True, self.NIDAQ_out) # Force the transmission light OFF
            self.laser_on = True
            self.stabilisation.laser_on = True
        else :
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
            self.label_laser.setText('OFF')
            functions_daq.digital_out(False, self.NIDAQ_out) # Force the transmission light OFF
            self.laser_on = False
            self.stabilisation.laser_on = False
    
    def pb_stabilize_clicked(self):
        if self.pb_stabilize.isChecked():
            if self.laser_on and self.piezo_connected and self.calibrated :
                self.label_stabilize_icon.setPixmap(self.Green_Light_Icon_On)
                self.label_stabilize.setText('ON ')
                self.stabilisation.stabilisation_period_s = self.sb_stabilise_time.value()
                self.start_stabilisation.emit()
                self.pb_laser_on.setDisabled(True)
                self.pb_timelaps.setDisabled(True)
                self.sb_stabilise_time.setDisabled(True)
                self.pb_timelaps.setDisabled(True)
            else :
                self.pb_stabilize.setChecked(False)
        else :
            self.label_stabilize_icon.setPixmap(self.Green_Light_Icon_Off)
            self.label_stabilize.setText('OFF')
            self.stop_stabilisation.emit()
            self.pb_laser_on.setEnabled(True)
            self.pb_timelaps.setEnabled(True)
            self.sb_stabilise_time.setEnabled(True)
            self.pb_timelaps.setEnabled(True)
            
    def pb_timelaps_clicked(self) :
        if self.pb_timelaps.isChecked():
            self.label_timelaps_icon.setPixmap(self.Green_Light_Icon_On)
            self.label_timelaps.setText('ON ')
            self.stabilisation.timelaps_period_s = self.sb_timelaps_time.value()
            self.start_timelaps.emit()
            self.pb_stabilize.setDisabled(True)
        else :
            self.label_timelaps_icon.setPixmap(self.Green_Light_Icon_Off)
            self.label_timelaps.setText('OFF')
            self.stop_timelaps.emit()
            self.pb_stabilize.setEnabled(True)
            
    def comboBox_devices_indexChanged(self):
        """"set the self.piezo_port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.piezo_port = self.comboBox_devices.currentText() 
        if self.piezo_port != 'None':
            self.piezo.change_port(self.piezo_port)
            if self.piezo.test_port() :
                self.piezo_connected = True
                self.get_position()
                state = self.piezo.get_status()
                if state == PiezoState.READY_OL:
                    self.piezo.close_loop()
                elif state == PiezoState.READY_CL:
                    pass
                else :
                    raise PiezoError("Piezo is not in READY_CL or READY_OL state : {state}")
                    
                if self.piezo.is_referenced():
                    self.label_piezo_referenced_icon.setPixmap(self.Green_Light_Icon_On)
                    self.label_piezo_referenced.setText("Referened")
                
                self.stabilisation.set_piezo_port(self.piezo_port)
                
            else:
                self.piezo_connected = False
                print("[RFS] piezo not connected")
        else :
            self.piezo_connected = False
        
        self.tools_desactivation()
        self.set_label_connection()
    
    def pb_piezo_reference_clicked(self):
        self.piezo.reference()
        self.get_position()
        if self.piezo.is_referenced():
            self.label_piezo_referenced_icon.setPixmap(self.Green_Light_Icon_On)
            self.label_piezo_referenced.setText("Referened")
        
    def slider_step_size_value_changed(self):
        self.step_size_um = float(self.slider_step_size.value())/100
        self.sb_step_size.blockSignals(True)
        self.sb_step_size.setValue(self.step_size_um)
        self.sb_step_size.blockSignals(False)
    
    def sb_step_size_value_changed(self) :
        self.step_size_um = self.sb_step_size.value()
        self.slider_step_size.blockSignals(True)
        self.slider_step_size.setValue(self.step_size_um * 100)
        self.slider_step_size.blockSignals(False)
        
    def pb_move_fw1_clicked(self):
        "Move forward of 1 step"
        self.piezo.move_by(self.step_size_um/1000) # step size is in mm for pizo
        self.get_position()
    
    def pb_move_bw1_clicked(self):
        "Move backward of 1 step"
        self.piezo.move_by(-self.step_size_um/1000) # step size is in mm for pizo
        self.get_position()
        
    def pb_calibrate_clicked(self):
        if self.laser_on :
            self.start_calibration.emit()
            self.calibrated = True
        else :
            self.label_message.setText("Laser should be on")  
    
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
        position = self.piezo.get_position()
        self.lcdNumber_Position.display(position)
        
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
        
    def test_port(self):
        "Test if the current port is the right device"
        return self.piezo.test_port()
        
    def tools_desactivation(self):
        if self.piezo_connected :
            inactive = False
        else:
            inactive = True
        
        self.slider_step_size.setDisabled(inactive)
        self.pb_piezo_reference.setDisabled(inactive)
        self.pb_move_bw1.setDisabled(inactive)
        self.pb_move_fw1.setDisabled(inactive)
        self.pb_stabilize.setDisabled(inactive)
        self.pb_timelaps.setDisabled(inactive)
        self.pb_calibrate.setDisabled(inactive)
        
    def set_label_connection(self):
        "set self.label_connection depending in the device connection"
        if self.piezo_connected :
            self.label_connection.setText('Connected')
            text_color = 'green'
        else:
            self.label_connection.setText('Not Connected')
            text_color = 'red'
            
        self.label_connection.setStyleSheet(f'color: {text_color}')
    
    #
    # Stabilization and display
    #
    
    def store_frame(self, frame, data):
        """Receive a frame from the camera thread and store it (unless paused)."""
        self.preview_frame = frame
        self.preview_data = data
        self.lcdNumber_Position.display(self.preview_data["piezo_position"])
        self.update_preview()
    
    def update_preview(self):
        """Display the most recent frame in the GUI."""
        if self.preview_frame is not None :
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
                
    def update_graph(self, data):
            self.displacements.append(data["um_displacement"])
            self.piezo_displacements.append(data["piezo_displacement"])
                
            size = self.label_graph.size()
            w , h = size.width() , size.height()
            
            plot = create_stabilisation_plot(self.displacements,
                                             self.piezo_displacements,
                                             w,
                                             h,)
            
            self.label_graph.setPixmap(QPixmap.fromImage(plot))
            
    def change_folder(self, folder) :
        self.folder_path = folder
        self.stabilisation.change_folder(folder)
            
    def closeEvent(self, event):
        """Stop worker threads before closing the window."""
    
        try:
            
            if hasattr(self, "stabilisationThread"):
                self.stop_stabilisation.emit()
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
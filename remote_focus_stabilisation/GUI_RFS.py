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

from Functions_UI import functions_ui

class RFS_window(QWidget, Ui_Form):
    """
    """
    
    def __init__(self, stabilisation, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.stabilisation = stabilisation
        
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
        
        #
        # Channel recieved
        #
        
        self.stabilisation.new_data.connect(self.store_frame)


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
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
        self.pb_laser_on.clicked.connect(self.pb_laser_on_clicked)
        self.pb_stabilize.clicked.connect(self.pb_stabilize_clicked)
        # Cobo box devices
        self.sb_step_size.valueChanged.connect(self.sb_step_size_value_changed)
        self.pb_move_fw1.clicked.connect(self.pb_move_fw1_clicked)
        self.pb_move_bw1.clicked.connect(self.pb_move_bw1_clicked)
        # Combo ox grayscale
        self.cb_preview_zoom.currentIndexChanged.connect(self.cb_preview_zoom_index_changed)
        self.sb_min_grayscale.valueChanged.connect(self.sb_grayscale_value_changed)
        self.sb_max_grayscale.valueChanged.connect(self.sb_grayscale_value_changed)
        self.pb_minmax_grayscale.clicked.connect(self.pb_minmax_grayscale_clicked)
        self.pb_auto_grayscale.clicked.connect(self.pb_auto_grayscale_clicked)
        self.pb_reset_grayscale.clicked.connect(self.pb_resset_grayscale_clicked)
    
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
            
    def sb_step_size_value_changed(self):
        """"set the step size in negative and positive direction
        21% seems to be the minimum for forward
        """
        self.step_size = self.sb_step_size.value()
        
    def pb_move_fw1_clicked(self):
        pass
    
    def pb_move_bw1_clicked(self):
        pass
    
    def cb_preview_zoom_index_changed(self):
        zoom_list = [0.5,0.5,1,2,3,4]
        self.preview_zoom = zoom_list[self.cb_preview_zoom.currentIndex()]
    
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
    
    def _on_close(self):
        pass
    
class TLCameraThread(QThread):
    """
    Thread dedicated to continuously reading images from the Thorlabs TLCamera.
    Emits the most recent frame via the new_frame signal.
    """
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, tlcam):
        super().__init__()
        self.tlcam = tlcam
        self.running = True  # Permet de contrôler l'arrêt propre du thread

    def run(self):
        """Main acquisition loop: read and emit frames continuously."""
        while self.running:
            frames = self.tlcam.read_multiple_images()
            if frames:
                frame = frames[-1]  # On prend la dernière image disponible

                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage
            
            self.msleep(30)

    def stop(self):
        """Stop acquisition loop cleanly."""
        self.running = False
        self.quit()
        self.wait()
    
##############################################################################
if __name__ == '__main__':
    
    from remote_focus_stabilisation.main_stabilisation import remote_focus_stabilisation
    
    RFS = remote_focus_stabilisation()
    
    app = QApplication(sys.argv)

    editor = RFS_window(RFS)
    editor.show()
    sys.exit(app.exec())
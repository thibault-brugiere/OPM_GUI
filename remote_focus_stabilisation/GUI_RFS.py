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
    
    
    def __init__(self, camera_sn = '36805', piezzo_port = 'COM6', parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.camera_sn = camera_sn
        self.piezzo_port = piezzo_port
        self.on_init()
        
        atexit.register(self._on_close)
        
    def on_init(self):
        self.setWindowTitle('Active Remote Focus Stabilization')
        
        self.tlcameras_list = Thorlabs.list_cameras_tlcam()
        
        if len(self.tlcameras_list) >=1:
            if self.camera_sn in self.tlcameras_list :
                self.tlcam = Thorlabs.ThorlabsTLCamera(self.camera_sn)
                self.tlcam.open()
                self.tlcam.set_exposure(10/1000)
            else :
                self.tlcam = Thorlabs.ThorlabsTLCamera(serial=self.tlcameras_list[0])
        else :
            self.label_message.setText("No camera connected")
            self.desactivate_camera_options()
            self.tlcam = None
            
        #
        # Parameters
        #
        
        self.preview_frame = None # frame actually displayed
        
        self.is_preview = True
        self.is_preview_paused = False
        self.look_up_table = 'grayscale'
        self.min_grayscale = 0
        self.max_grayscale = 1024
        self.preview_zoom = 0.5
        
        #
        # Timers
        #
        
        self.timer_preview = QTimer() # Timer to show new frame
        self.timer_preview.timeout.connect(self.update_preview)
        self.timer_preview.start(30)
        
        # Start camera acquisition in separate thread
        self.camera_thread = TLCameraThread(self.tlcam)
        self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
        self.tlcam.start_acquisition(nframes=2)
        self.camera_thread.start()
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
        self.pb_stabilize.clicked.connect(self.pb_stabilize_clicked)
    
    def pb_stabilize_clicked(self):
        pass
    
    #
    # Stabilization and display
    #
    
    def store_frame(self, frame):
        """Receive a frame from the camera thread and store it (unless paused)."""
        if not self.is_preview_paused :
            self.preview_frame = frame
    
    def update_preview(self):
        """Display the most recent frame in the GUI."""
        if self.is_preview and self.preview_frame is not None :
            
            qt_image = functions_ui.create_preview(self.preview_frame,
                                                   self.look_up_table,
                                                   self.min_grayscale,
                                                   self.max_grayscale,
                                                   self.preview_zoom)
            
            self.label_image_preview.setPixmap(QPixmap.fromImage(qt_image))
            
        elif self.preview_frame is None :
            self.label_image_preview.setText("No image!")
    
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
    app = QApplication(sys.argv)

    editor = RFS_window()
    editor.show()
    sys.exit(app.exec())
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:40:05 2026

@author: tbrugiere
"""
import numpy as np
import os
from pylablib.devices import Thorlabs
import sys

from PySide6.QtCore import QThread, Signal, QObject

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from hardware.functions_super_agilis import functions_super_agilis as piezzo
    
class remote_focus_stabilisation(QObject): # Nécessaire pour le fonctionnement de new_data Signal
    new_data = Signal(np.ndarray, dict) # signal Qt émis avec image + datas
    
    def __init__(self, camera_sn = '36805', piezzo_port = 'COM6', NIDAQ_out = "Dev1/port0/Line13", parent = None):
        super().__init__()
        self.camera_sn = camera_sn
        self.piezzo_port = piezzo_port
        self.NIDAQ_out = NIDAQ_out
        self.parent = parent
        
        self.tlcam = None
        
        self.frame = None
        self.data = {"camera_connected" : False,
                     "camera_sn" : camera_sn}
        
        self.on_init()
    
    def on_init(self):
        self.connect_camera()
        
        # Start camera acquisition in separate thread
        self.camera_thread = TLCameraThread(self.tlcam)
        self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
        self.tlcam.start_acquisition(nframes=2)
        self.camera_thread.start()
    
    def connect_camera(self):
        self.tlcameras_list = Thorlabs.list_cameras_tlcam()
        
        if len(self.tlcameras_list) >=1:
            if self.camera_sn in self.tlcameras_list :
                self.tlcam = Thorlabs.ThorlabsTLCamera(self.camera_sn)
                self.tlcam.open()
                self.tlcam.set_exposure(10/1000)
            else :
                self.tlcam = Thorlabs.ThorlabsTLCamera(serial=self.tlcameras_list[0])
                self.tlcam.open()
                self.tlcam.set_exposure(10/1000)
                self.data["camera_sn"] = self.tlcameras_list[0]
        else :
            self.data["camera_connected"] = False
            self.tlcam = None
            self.new_data.emit(self.preview_frame, self.data)
            
    def store_frame(self, frame):
        """Receive a frame from the camera thread and store it (unless paused)."""
        self.preview_frame = frame
        self.new_data.emit(self.preview_frame, self.data)
        
    def stop(self):
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
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:40:05 2026

@author: tbrugiere
"""

import os
from pylablib.devices import Thorlabs
import sys

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from hardware.functions_super_agilis import functions_super_agilis as piezzo
    
class remote_focus_stabilisation:
    def __init__(self, camera_sn = '36805', piezzo_port = 'COM6', NIDAQ_out = "Dev1/port0/Line13", parent = None):
        self.camera_sn = camera_sn
        self.piezzo_port = piezzo_port
        self.NIDAQ_out = NIDAQ_out
        self.parent = parent
        
        self.on_init()
        
        self.tlcam = None
        
        self.frame = None
    
    def on_init(self):
        pass
    
    def connect_camera(self):
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
            
    def get_image(self):
        if self.tlcam is not None:
            return None
        else:
            return None
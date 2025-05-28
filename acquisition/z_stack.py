# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:30:40 2025

@author: tbrugiere

Ce programme permet de faire l'acquisition d'un Z-stack avec la platine ASI
Il est utilisé pour la caractérisation du microscope
Rien n'est optimisé dans ces fonctions
"""

import numpy as np
import os
from pylablib.devices import DCAM
import sys
import tifffile
import time as t

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from hardware.functions_camera import functions_camera
from hardware.functions_serial_ports import functions_serial_ports as serial

class z_stack():
    
    def __init__(self, hcam, path, port = 'COM10'):
        super().__init__()
        self.hcam = hcam
        self.path = path
        self.port = port
    
    def acquisition(self,scan_range = 2,
                    step_size = 0.05):
        
        scan_range = scan_range * 10 # values are in 1/10 of microns
        step_size = step_size * 10
        
        get_position = serial.send_command_response('WHERE Z', self.port)
        start_position = int(get_position.split()[1])
        
        # calculate total number of steps
        num_steps = int(scan_range / step_size)
        
        # Create vector of position around of the actual position
        positions = np.linspace(start_position - (num_steps / 2) * step_size,
                                start_position + (num_steps / 2) * step_size,
                                num_steps + 1)
        
        for position in positions :
            serial.send_command(f'MOVE Z={position}' , self.port)
            self.hcam.start_acquisition('snap')
            self.hcam.wait_for_frame()
            frame = self.hcam.read_newest_image()
            self.hcam.clear_acquisition()
            
            file_path = os.path.join(self.path , f"{position}.tiff")
            tifffile.imwrite(file_path, frame)
            
        self.hcam.clear_acquisition()
        serial.send_command(f'MOVE Z={start_position}' , self.port)
        
        
####################################################################
### Test
#########

if __name__ == '__main__':
    ncam = DCAM.get_cameras_number()
    hcam = DCAM.DCAMCamera(0)
    hcam.cav['EXPOSURE TIME'] = 0.1
    
    path = 'D:/Projets_Python/OPM_GUI/Images/test_z_stack'
    port = 'COM10'
    
    test_z_stack = z_stack(hcam, path, port)
    test_z_stack.acquisition(scan_range = 100,
                             step_size = 10)
    hcam.close()
    
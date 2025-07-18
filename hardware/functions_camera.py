# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:37:20 2025

@author: tbrugiere
"""
import numpy as np

from PySide6.QtCore import QThread, Signal

from configs.config import camera

# from pylablib.devices import DCAM
from mock.hamamatsu import DCAM

class functions_camera():
    
    def initialize_cameras(n_camera, magnification):
        """
        Initialize a list of camera objects based on the number of detected cameras.
        
        Returns:
        - hcams : List[DCAM.DCAMCamera]: A list of initialized camera objects. (hcam for hamamatsu camera)
        - cameras list[camera]: A list of camera objects from config
        """
        
        hcams = []
        cameras = []
        
        for camera_id in range(n_camera):
            hcam = DCAM.DCAMCamera(camera_id)
            hcams.append(hcam)
            
            cam = camera(camera_id)
            
            # Automatically get the parameters from the camera
            cam.hchipsize, cam.vchipsize = hcam.get_detector_size()
            cam.hsize, cam.vsize = cam.hchipsize, cam.vchipsize
            cam.pixel_size = hcam.get_attribute_value('image_detector_pixel_width')
            cam.line_readout_time = hcam.get_attribute_value('internal_line_interval')
            cam.sample_pixel_size = cam.pixel_size / magnification
            
            cameras.append(cam)
            
        return hcams, cameras
    
    def close_cameras(hamamatsu_cameras):
        """"Close all the cameras openned"""
        n_camera = len(hamamatsu_cameras)
        
        for camera_id in range(n_camera) :
            hamamatsu_cameras[camera_id].close()
    
    def configure_camera_for_preview(hcam, camera):
        """Configure les paramètres de la caméra.
        Parameters
        ----------
        
        hcam : DCAM camera from pylablib
        camera : camera object from config file
        
        """

        hcam.cav["SUBARRAY MODE"]=2
        hcam.cav["EXPOSURE TIME"] = camera.exposure_time
        hcam.cav["subarray_hpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        hcam.cav["subarray_vpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        hcam.cav["subarray_hsize"] =  camera.hsize
        hcam.cav["subarray_vsize"] = camera.vsize
        hcam.cav["subarray_hpos"] =  camera.hpos
        hcam.cav["subarray_vpos"] =  camera.vpos
        hcam.cav["binning"] = camera.binning

class CameraThread(QThread):
    """Thread that continously get last image from camera."""
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, hcam):
        super().__init__()
        self.hcam = hcam
        self.running = True  # Permet de contrôler l'arrêt propre du thread

    def run(self):
        """Boucle d'acquisition d'images en continu."""
        while self.running:
            frames = self.hcam.read_multiple_images()
            if frames:
                frame = frames[-1]  # On prend la dernière image disponible

                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage

    def stop(self):
        """Arrête proprement l'acquisition."""
        self.running = False
        self.quit()
        self.wait()
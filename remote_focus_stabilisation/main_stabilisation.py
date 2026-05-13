# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:40:05 2026

@author: tbrugiere
"""
import warnings
warnings.filterwarnings("ignore", message="Mean of empty slice")
warnings.filterwarnings("ignore", message="invalid value encountered")

import contextlib
import numpy as np
import os
import pandas as pd
from pylablib.devices import Thorlabs
from scipy.stats import linregress
import sys
import threading
import time

from palm_tracer.Processing import Palm

from PySide6.QtCore import QThread, Signal, QObject, QElapsedTimer

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
    
    def __init__(self, camera_sn = '36805', piezzo_port = None, NIDAQ_out = "Dev1/port0/Line13", parent = None):
        super().__init__()
        self.camera_sn = camera_sn
        self.piezzo_port = piezzo_port
        self.NIDAQ_out = NIDAQ_out
        self.parent = parent
        
        self.tlcam = None
        
        self.piezzo_position = 0.0
        self.frame = None
        self.camera_sn = camera_sn
    
    def on_init(self):
        self.data_image = {"camera_connected" : False,
                     "camera_sn" : self.camera_sn,
                     "calibration_data" : None}
        
        self.connect_camera()
        
        self.palm = Palm()
        self._last_palm = 0.0
        self._palm_wait = 0.5
        
        self.preview_frame = None
        self.mode = 'preview'
        
        # Start camera acquisition in separate thread
        self.camera_thread = TLCameraThread(self.tlcam)
        self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
        self.tlcam.start_acquisition(nframes=2)
        self.camera_thread.start()
        
        # Get values for stabilization :
        self.calibration_data = {
            "x_displacement" : None,
            "y_displacement" : None,
            "r2x" : None,
            "r2y" : None,
            "fw_step" : None,
            "bw_step" : None,
            "x_spot_pos" : None,
            "y_spot_pos" : None,
            }
        
        self.data_image["calibration_data"] = self.calibration_data
    
    def set_piezzo_port(self, piezzo_port):
        self.piezzo_port = piezzo_port
    
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
                self.data_image["camera_sn"] = self.tlcameras_list[0]
                
            self.data_image["camera_connected"] = True
            
        else :
            self.data_image["camera_connected"] = False
            self.tlcam = None
            self.new_data.emit(self.preview_frame, self.data_image)
            
    def store_frame(self, frame):
        """Receive a frame from the camera thread and store it (unless paused)."""
        self.preview_frame = frame
        self.new_data.emit(self.preview_frame, self.data_image)
        x,y = self._get_center()
        return x,y
        
    def ecrit(self):
        print('ça fonctionne')
        
        
    def calibration(self, sampling = 10):
        if self.piezzo_port is None :
            print("Pizzo port not set")
            return
        
        self.mode = "calibration"
        
        self.camera_thread.set_mode("on_demand")
        x_list = []
        y_list = []
        piezzo_positions = []
        for k in range(2 * sampling + 1) :
            if k < sampling :
                piezzo.send_command('XR1', self.piezzo_port)
            elif k == sampling :
                piezzo.send_command('XR-10', self.piezzo_port)
            elif k > sampling : 
                piezzo.send_command('XR-1', self.piezzo_port)
                
            time.sleep(0.5)
            self.get_piezzo_position()
            x_image = []
            y_image = []
            for i in range(10) :
                self.camera_thread.frame_event.clear()
                self.camera_thread.request_frame()
                self.camera_thread.frame_event.wait(timeout=1.0)
                x,y = self.store_frame(self.camera_thread.frame)
                x_image.append(x)
                y_image.append(y)
                
            x = np.mean(x_image)
            y = np.mean(y_image)
            
            x_list.append(x)
            y_list.append(y)
            piezzo_positions.append(self.piezzo_position)

            print(f"{x:.2f} - {y:.2f} - {self.piezzo_position:.3f}")
    
        regres_x = linregress(piezzo_positions, x_list)
        regres_y = linregress(piezzo_positions, y_list)
        
        fw_step = (piezzo_positions[sampling - 1] - piezzo_positions[0]) / sampling
        bw_step = (piezzo_positions[2*sampling] - piezzo_positions[sampling + 1]) / sampling
        
        self.calibration_data["x_displacement"] = regres_x.slope
        self.calibration_data["y_displacement"] = regres_y.slope
        self.calibration_data["r2x"] = regres_x.rvalue ** 2
        self.calibration_data["r2y"] = regres_y.rvalue ** 2
        self.calibration_data["fw_step"] = fw_step
        self.calibration_data["bw_step"] = bw_step
        
        if (regres_x.rvalue ** 2) > 0.98 and (regres_y.rvalue ** 2) > 0.98 :
            print('Calibration successful ')
        else :
            print(f'Calibration failed: poor linear regression : r²x =  {(regres_x.rvalue ** 2):.4f},  r²y =  {(regres_y.rvalue ** 2):.4f}')
            
        print(f'axe x : {regres_x.slope:.2f} ps/µm - r² : {(regres_x.rvalue ** 2):.4f}')
        print(f'axe x : {regres_y.slope:.2f} ps/µm - r² : {(regres_y.rvalue ** 2):.4f}')
        print(f"fw step : {fw_step:.3f} - bw step = {bw_step:.3f}")
            
        self.mode = "preview"
        self.camera_thread.set_mode("preview")
        
        
    def _get_center(self):
        if self.preview_frame is not None :
            h,w = self.preview_frame.shape
            cy, cx = h // 2, w // 2
            crop = self.preview_frame[cy - 256 : cy + 256,cx - 256 : cx + 256 ]
            # threshold = self.palm.auto_threshold(self.preview_frame, np.array([30], dtype=np.float64))  # paramètre juste la ROI
            threshold = 20
            with contextlib.redirect_stdout(open(os.devnull, 'w')): # To avoid print from palm
                localizations = self.palm.localization(crop, threshold, False, 4, np.array([15, 1, 2, 0], dtype=np.float64))
                
            n_points = len(localizations)
            if n_points == 1 :
                x = float(localizations.loc[0,"X"])
                y = float(localizations.loc[0,"Y"])
                if self.mode == "preview" :
                    print(f'{x:.2f} - {y:.2f}')
                return x, y
            elif n_points == 0 :
                print("no point detected")
                return None, None
            else :
                print('more than 1 point detected')
                return None, None
        else :
            print("no frame")
            return None, None
        
    def get_piezzo_position(self):
        "Get the current position of the device and display it"
        position = piezzo.send_command_response('TP', self.piezzo_port)
        position = float(position[2:])
        position = 1000 * position
        self.piezzo_position = position
        
    def stop(self):
        """Stop all internal workers cleanly."""
    
        if hasattr(self, "camera_thread") and self.camera_thread is not None:
            self.camera_thread.stop()
    
        if self.tlcam is not None:
            try:
                self.tlcam.stop_acquisition()
            except Exception:
                pass
    
            try:
                self.tlcam.close()
            except Exception:
                pass
        
class TLCameraThread(QThread):
    """
    Thread dedicated to continuously reading images from the Thorlabs TLCamera.
    Emits the most recent frame via the new_frame signal.
    """
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, tlcam, period_ms = 100):
        super().__init__()
        self.tlcam = tlcam
        self.period = period_ms
        
        self.frame_event = threading.Event()
        
        self.running = True  # Permet de contrôler l'arrêt propre du thread
        self.frame_requested = False
        self.mode = "preview"
        self.frame = None #last frame read on the camera
        
    def set_mode(self, mode) :
        self.mode = mode
    
    def request_frame(self):
        self.frame_requested = True
        
    def _read_emit(self):
        """Read the newest available image and emit it."""
        frame = self.tlcam.read_newest_image()
        
        if frame is not None :
            self.frame = frame
            
            if self.mode == "preview" :
                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage
                
            self.frame_event.set()

    def run(self):
        """Main acquisition loop: read and emit frames continuously."""
        timer = QElapsedTimer()
        
        while self.running:
            if self.mode == "preview" :
                timer.restart()
                
                self._read_emit()
                
                elapsed = timer.elapsed()
                remaining = self.period - elapsed
                
                if remaining > 0 :
                    self.msleep(remaining)
            
            elif self.mode == "on_demand" :
                if self.frame_requested :
                    self.frame_requested = False
                    self._read_emit()
                
                else:
                    self.msleep(1)
                    
    def stop(self):
        """Stop acquisition loop cleanly."""
        self.running = False
        self.wait()
        self.quit()
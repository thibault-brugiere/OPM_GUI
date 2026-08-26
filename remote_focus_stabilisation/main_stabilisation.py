# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:40:05 2026

@author: tbrugiere
"""
import warnings
warnings.filterwarnings("ignore", message="Mean of empty slice")
warnings.filterwarnings("ignore", message="invalid value encountered")

import contextlib
import json
import numpy as np
import os
from pathlib import Path
from pylablib.devices import Thorlabs
from scipy.stats import linregress
import sys
import threading
import time
import tifffile

from palm_tracer.Processing import Palm

from PySide6.QtCore import QThread, Signal, QObject, QElapsedTimer

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from hardware.functions_piezo import piezo_SAS, PiezoState, PiezoExecutionError
from hardware.functions_DAQ import functions_daq


class PiezoError(RuntimeError):
    "Error while using the Piezo"

class remote_focus_stabilisation(QObject): # Nécessaire pour le fonctionnement de new_data Signal
    new_data = Signal(np.ndarray, dict) # signal Qt émis avec image + datas
    new_stabilisation = Signal(dict)
    new_calibration = Signal(dict)
    new_piezo_position = Signal(dict)
    
    def __init__(self,
                 camera_sn = '36805',
                 piezo = None,
                 NIDAQ_out = "Dev1/port0/Line13",
                 folder_path = Path(r"D:\Images_OPM\Metrologie-Developpement\20260821_RFS"),
                 message = True,
                 parent = None):
        
        """
        

        Parameters
        ----------
        camera_sn : str, optional
            Serial number of the thorlabs camera used for stabilisation.
            The default is '36805'.
        piezo_port : str, optional
            port COM number of the piezo controller (ex. "COM6")
        NIDAQ_out : str, optional
            Digital out of the NiDAQ that controls the 488nm laser for stabilisation.
            The default is "Dev1/port0/Line13".
        folder_path : Path, optional
            Path of the folder to save datas of stabilisation
        """
        
        super().__init__()
        self.camera_sn = camera_sn
        self.piezo = piezo
        self.NIDAQ_out = NIDAQ_out
        self.folder = folder_path
        self.message = message
        self.calibration = Calibration()
        
        self.parent = parent
        
        # self.on_init()
    
    def on_init(self):
        self.data_image = {"camera_connected" : False,
                           "camera_sn" : self.camera_sn,
                           "calibration_data" : None,
                           "displacement" : 0.0,
                           "piezo_displacement" : 0.0,
                           "piezo_position" : 0.0
                           }
        
        self.data_stabilisation = {"displacement" : 0.0,
                                   "piezo_displacement" : 0.0,
                                   "piezo_position" : 0.0
                                   }
        
        self.connect_camera()
        
        self.palm = Palm() # To measure the center of mass of the spot on the camera
        
        self.preview_frame = None
        self.mode = 'preview'
        
        # Parameters for stabilisation and timelaps
        self.stabilisation_period_s = 60
        self.timelaps_period_s = 60
        
        # Start camera acquisition in separate thread
        self.camera_thread = TLCameraThread(self.tlcam)
        self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
        self.tlcam.start_acquisition(nframes=2)
        self.camera_thread.start()
        
        # Create Piezo
        if self.piezo is None :
            self.piezo = piezo_SAS()
        
        # Create values for stabilization :
        self.original_position = None
        self.displacement = None
        self.piezo_position = 0.0
        self.frame = None
        
        self.laser_on = False
        
        self.data_image["calibration_data"] = self.calibration.get_calibration_data()
        
    def set_piezo_port(self, piezo_port):
        """
        

        Parameters
        ----------
        piezo_port : str
            port COM number of the piezo controller (ex. "COM6")

        """
        self.piezo.change_port(piezo_port)
        if not self.piezo.test_port() :
            print("[RFS] Pizo not connected")
            
        self.check_piezo_state()
            
    def check_piezo_state(self):
        state = self.piezo.get_status()
        if state == PiezoState.READY_OL:
            self.piezo.close_loop()
        elif state == PiezoState.READY_CL:
            pass
        else :
            raise PiezoError("Piezo is not in READY_CL or READY_OL state : {state}")
    
    def get_piezo_position(self):
        """
        send the piezo position each time the program ask the position of the piezo

        Returns
        -------
        position : int
            piezo position in mm.

        """
        position = self.piezo.get_position()
        self.new_piezo_position.emit({"position" : position})
        return position
    
    def connect_camera(self):
        self.tlcameras_list = Thorlabs.list_cameras_tlcam()
        
        if len(self.tlcameras_list) >=1:
            if self.camera_sn in self.tlcameras_list :
                self.tlcam = Thorlabs.ThorlabsTLCamera(self.camera_sn)
                self.tlcam.open()
                self.tlcam.set_exposure(50/1000)
            else :
                self.tlcam = Thorlabs.ThorlabsTLCamera(serial=self.tlcameras_list[1])
                self.tlcam.open()
                self.tlcam.set_exposure(50/1000)
                self.data_image["camera_sn"] = self.tlcameras_list[1]
                
            self.data_image["camera_connected"] = True
            
        else :
            self.data_image["camera_connected"] = False
            self.tlcam = None
            self.new_data.emit(self.preview_frame, self.data_image)
            
    def turn_laser_on(self, state = True):
        functions_daq.digital_out(state, self.NIDAQ_out)
        self.laser_on = state
    
    def is_laser_on(self):
        return self.laser_on
            
    def store_frame(self, frame):
        """
        Receive a frame from the camera thread and store it (unless paused) and return the
        center of the laser point on the image
        """
        self.preview_frame = frame
        if self.piezo.connected :
            try :
                self.data_image["piezo_position"] = self.get_piezo_position()
                self.piezo_position = self.data_image["piezo_position"]
            except :
                pass
        self.new_data.emit(self.preview_frame, self.data_image)
        x,y = self._get_center()
        return x,y
        
    def load_calibration(self):
        self.calibration.load_data()
        self.new_calibration.emit(self.calibration.get_calibration_data())
        
    def save_calibration(self):
        self.calibration.save_data()
        
    def start_calibration(self, sampling:int = 10, step:float = 1):
        """
        

        Parameters
        ----------
        sampling : int, optional
            Number of point used in each direction for calibration. The default is 10.
        step : float, optional
            Distance for each step of the calibration in µm
        """
        if not self.piezo.test_port() :
            raise ValueError(f"Wrong piezo port : {self.piezo.get_port}")
            
        self.check_piezo_state()
        
        self.mode = "calibration"
        
        self.camera_thread.set_mode("on_demand")
        x_list = []
        y_list = []
        piezo_positions = []
        position = self.get_piezo_position()
        original_position = position
        first_position = original_position - step * sampling / 2 / 1000
        self.piezo.move_to(first_position)
        for k in range(sampling) :
            try :
                self.piezo.move_by(step/1000)
            except PiezoExecutionError :
                pass
            except Exception as exc :
                print(f"Error: {exc}")
                raise
 
            time.sleep(0.5)
            x_image = []
            y_image = []
            for i in range(10) :
                self.camera_thread.frame_event.clear()
                self.camera_thread.request_frame()
                self.camera_thread.frame_event.wait(timeout=1.0)
                x,y = self.store_frame(self.camera_thread.frame)
                if x is not None :
                    x_image.append(x)
                    y_image.append(y)
            
            if len(x_image) > 0 :
                x = np.mean(x_image)
                y = np.mean(y_image)
            
                x_list.append(x)
                y_list.append(y)
                position = self.get_piezo_position()
                piezo_positions.append(position)
                
                
                if self.message : print(f"{x:.2f} - {y:.2f} - {position:f}")
            
            else :
                if self.message : print("None - None - None")
            
            self.save_image(f"RFS_{position:6f}")
            
        self.piezo.move_to(original_position)
    
        if len(x_list) >= 2 :
            if len(x_list) < 5 :
                print("[RFS] Bad calibration, not enough points")
                    
            self.calibration.calculate_px_per_um(piezo_positions, x_list, y_list)
            
            if (self.calibration.r2x) > 0.98 and (self.calibration.r2y) > 0.98 :
                print('[RFS] calibration successful ')
            else :
                print(f'[RFS] Calibration failed: poor linear regression : r²x =  {self.calibration.r2x:.4f},  r²y =  {self.calibration.r2y:.4f}')
                
            print(f'axe x : {self.calibration.px_per_um_x:.2f} px/µm - r² : {self.calibration.r2x:.4f}')
            print(f'axe y : {self.calibration.px_per_um_y:.2f} px/µm - r² : {self.calibration.r2y:.4f}')
            
            self.new_calibration.emit(self.calibration.get_calibration_data())
            
        else :
            print("[RFS] Images too bad for caliration")
            
        self.data_image["calibration_data"] = self.calibration.get_calibration_data()
        self.mode = "preview"
        self.camera_thread.set_mode("preview")

        
    def stabilisation(self, kp = 0.5, max_step_um = 2.0,
                      max_correction_in_row = 5, drift_threshold = 0.3,
                      max_total_displacement_um = 200):
        """
        

        Parameters
        ----------
        kp : float, optional
            agressivity of the stabilisation, should be between 0 and 1. The default is 0.5.
        max_step_um : float, optional
            Maximum step of the piezo in one correction. The default is 2.0 µm.
        max_correction_in_row : int, optional
            maximum correction steps in a row. The default is 5.
        drift_threshold : float, optional.
            Maximum displacement in px on the camera from the original position before correction

        Raises
        ------
        ValueError
            If kp is not between 0 and 1.
        """

        if not self.piezo.test_port() :
            raise ValueError(f"Wrong piezo port : {self.piezo.get_port}")
        
        if self.calibration.calibrated == False :
            raise ValueError(f"[RFS] stabilisation should be calibrated befor stabilisation. Calivration: {self.calibration.calibrated}")
        
        if self.mode != "preview":
            print(f'[RFS] Can not start timelaps, {self.mode} running')
            return
        
        # if self.stabilisation_period_s < 10 :
        #     self.stabilisation_period_s = 10
        #     print("[RFS] period_s too small, set to 10s")
            
        if kp > 1 or kp < 0 :
            raise ValueError(f"kp shoulb be between 0 and 1, actual value {kp}")
        
        self.mode = "stabilisation"
        self.camera_thread.set_mode("on_demand")
        
        timer = QElapsedTimer()
        
        get_position = True
        
        file_path = os.path.join(self.folder, "stabilization_log.txt")
        
        with open(file_path, "a", encoding="utf-8") as file:
            file.write('current_time,x,y,position,displacement,piezo_displacement\n')
            file.flush()
            
        correction_count = 0
        total_correction_count = 0
        self.piezo_position = self.get_piezo_position()
        max_position = min(self.piezo.max_position, self.piezo_position + max_total_displacement_um / 1000)
        min_position = max(self.piezo.min_position, self.piezo_position - max_total_displacement_um / 1000)
        
        timer.start()
                
        while self.mode == "stabilisation" :

            timer.start()
        
            if correction_count < max_correction_in_row :
                
                x_image = []
                y_image = []
                
                for i in range(10) :
                    
                    self.camera_thread.frame_event.clear()
                    self.camera_thread.request_frame()
                    self.camera_thread.frame_event.wait(timeout=1.0)
                    x,y = self.store_frame(self.camera_thread.frame)
                    # self.piezo_position is updated in self.store_frame
                    
                    if x is not None :
                        x_image.append(x)
                        y_image.append(y)
                        
                
                if len(x_image) > 0 :
                    x = np.mean(x_image)
                    y = np.mean(y_image)
                    
                    if get_position :
                        self.calibration.x_spot_pos = x
                        self.calibration.y_spot_pos = y
                        get_position = False
                        
                    um_displacement = self.calibration.calculate_displacement(x, y)
                    
                    if abs(um_displacement) > drift_threshold :
                        
                        piezo_displacement = np.clip(
                            kp * um_displacement,
                            -max_step_um,
                            max_step_um)
                        
                        target_position = self.piezo_position + piezo_displacement / 1000
                        
                        if min_position <= target_position <= max_position:
                            try :
                                self.piezo.move_by(piezo_displacement / 1000)
                                time.sleep(1)
                                correction_count += 1
                                total_correction_count += 1
                                if total_correction_count >= 80 :
                                    self.mode == "preview"
                            except PiezoExecutionError :
                                pass
                            except Exception as exc :
                                print(f"Error: {exc}")
                                raise
                                
                    # self.save_image(f"{frame*5} min_{x:.3f}_{y:.3f}.tif")
                    
                    else :
                        piezo_displacement = 0
                    
                    current_time = time.strftime("%H:%M:%S")
                    
                    if self.message : print(f'{current_time} - {x:.2f} - {y:.2f} - {self.piezo_position:.6f} - {um_displacement:.3f} - {piezo_displacement}')
                    
                    self.data_stabilisation["um_displacement"] = um_displacement
                    self.data_stabilisation["piezo_displacement"] = piezo_displacement
                    self.new_stabilisation.emit(self.data_stabilisation)
                    
                    with open(file_path, "a", encoding="utf-8") as file:
                        file.write(f'{current_time},{x:.2f},{y:.2f},{self.piezo_position:.6f},{um_displacement:.3f},{piezo_displacement:.3f}\n')
                        file.flush()
                        
                    if piezo_displacement == 0 :
                        while self.mode == "stabilisation" and timer.elapsed() < (self.stabilisation_period_s * 1000) :
                            time.sleep(0.01) # Attendre 0 ms
                            correction_count = 0
                        
            else :
                correction_count = 0
                k = 0
                while self.mode == "stabilisation" and timer.elapsed() < (self.stabilisation_period_s * 1000) :
                    time.sleep(0.01) # Attendre 0 ms
                    k +=1
                    if k == 10 :
                        position = self.piezo.get_position()
                        self.new_piezo_position.emit({"position" : position})
                        k = 0
                
        self.camera_thread.set_mode("preview")
        
    def stop_stabilisation(self):
        if self.mode == "stabilisation" :
            if self.message : print('[RFS] stop stabilisation')
            self.mode = "preview"
        
    def timelaps(self):
        """

        """
        if not self.piezo.test_port() :
            raise ValueError(f"Wrong piezo port : {self.piezo.get_port}")
        
        if self.mode != "preview":
            print(f'[RFS] Can not start timelaps, {self.mode} running')
            return
        
        self.mode == "timelaps"
        self.camera_thread.set_mode("on_demand")
        
        timer = QElapsedTimer()
        
        get_position = True
        
        file_path = os.path.join(self.folder, "timelaps_log.txt")
        
        with open(file_path, "a", encoding="utf-8") as file:
            file.write('current_time,x,y,position,um_displacement,piezo_displacement\n')
            file.flush()
            
        self.mode = "timelaps"
        self.camera_thread.set_mode("on_demand")
        
        while self.mode == "timelaps" :

            timer.start()
            
            x_image = []
            y_image = []
            
            for i in range(10) :
                
                self.camera_thread.frame_event.clear()
                self.camera_thread.request_frame()
                self.camera_thread.frame_event.wait(timeout=1.0)
                x,y = self.store_frame(self.camera_thread.frame)
                # self.piezo_position is updated in self.store_frame
                
                if x is not None :
                    x_image.append(x)
                    y_image.append(y)
            
            if len(x_image) > 0 :
                x = np.mean(x_image)
                y = np.mean(y_image)
                
                if get_position :
                    self.calibration.x_spot_pos = x
                    self.calibration.y_spot_pos = y
                    get_position = False
                    
                if self.calibration.calibrated :
                    um_displacement = self.calibration.calculate_displacement(x, y)
                
                    current_time = time.strftime("%H:%M:%S")
                    
                    if self.message : print(f'[RFS] {current_time} - {x:.2f} - {y:.2f} - {um_displacement:.3f} - {um_displacement}')
                
                self.data_image["um_displacement"] = um_displacement
                self.data_image["piezo_displacement"] = um_displacement
                
                self.data_stabilisation["um_displacement"] = um_displacement
                self.data_stabilisation["piezo_displacement"] = 0
                self.new_stabilisation.emit(self.data_stabilisation)
                
                with open(file_path, "a", encoding="utf-8") as file:
                    file.write(f'{current_time},{x:.2f},{y:.2f},{self.piezo_position:.6f},{um_displacement:.3f},0\n')
                    file.flush()
            
            # self.save_image(f"{frame*5} min_{x:.3f}_{y:.3f}.tif")
            
            k = 0
            while self.mode == "timelaps" and timer.elapsed() < (self.timelaps_period_s * 1000) :
                time.sleep(0.01) # Attends 10ms
                k +=1
                if k == 10 :
                    position = self.piezo.get_position()
                    self.new_piezo_position.emit({"position" : position})
                    k = 0
                
    def stop_timelaps(self):
        if self.mode == "timelaps" :
            if self.message : print('[RFS] stop timelaps')
            self.mode = "preview"
            self.camera_thread.set_mode("preview")
        
    def _get_center(self):
        if self.preview_frame is not None :
            h,w = self.preview_frame.shape
            cy, cx = h // 2, w // 2
            crop = self.preview_frame[cy - 256 : cy + 256,cx - 256 : cx + 256 ]
            # threshold = self.palm.auto_threshold(self.preview_frame, np.array([30], dtype=np.float64))  # paramètre juste la ROI
            threshold = 45
            with contextlib.redirect_stdout(open(os.devnull, 'w')): # To avoid print from palm
                localizations = self.palm.localization(crop, threshold, False, 4, np.array([15, 1, 2, 0], dtype=np.float64))
                
            n_points = len(localizations)
            if n_points == 1 :
                x = float(localizations.loc[0,"X"])
                y = float(localizations.loc[0,"Y"])
                # if self.message : print(f"[RFS] point detected : {x:3f},{y:3f}")
                return x, y
            elif n_points == 0 :
                if self.laser_on :
                    if self.message : print("[RFS] no point detected")
                return None, None
            else :
                if self.message : print('[RFS] more than 1 point detected')
                return None, None
        else :
            if self.message : print("[RFS] no frame")
            return None, None
        
    def save_image(self, name: str) :
        return
    
        if self.preview_frame is None :
            return
        
        file_path = os.path.join(self.folder, name)
        
        try :
            tifffile.imwrite(file_path, self.preview_frame)
            
        except Exception as e:
            if self.message : print(f"[RFS] Failed to save frame:\n{str(e)}.tif")
        
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
            
    def change_folder(self, folder) :
        self.folder = folder
            
    def closeEvent(self, event):
    
        if self.tlcam is not None:
            try:
                self.tlcam.close()
            except Exception as e:
                print(f"[RFS] Error while closing camera: {e}")
    
        event.accept()
            
class Calibration():
    def __init__(self) :
        self.calibrated = False
        self.px_per_um_x = None
        self.px_per_um_y = None
        self.r2x = None
        self.r2y = None
        self.x_spot_pos = None,
        self.y_spot_pos = None
    
    def calculate_px_per_um(self, piezo_positions, x_list, y_list):
        regres_x = linregress(piezo_positions, x_list)
        regres_y = linregress(piezo_positions, y_list)
        
        self.px_per_um_x = regres_x.slope / 1000
        self.px_per_um_y = regres_y.slope / 1000
        self.r2x = regres_x.rvalue ** 2
        self.r2y = regres_y.rvalue ** 2
        self.calibrated = True
            
    def get_calibration_data(self):
        calibration_data = {
            "calibrated" : self.calibrated,
            "px_per_um_x" : self.px_per_um_x,
            "px_per_um_y" : self.px_per_um_y,
            "r2x" : self.r2x,
            "r2y" : self.r2y,
            "x_spot_pos" : self.x_spot_pos,
            "y_spot_pos" : self.y_spot_pos,
            }
        
        return calibration_data
    
    def calculate_displacement(self, x , y):
        if self.px_per_um_x is None :
            raise ValueError("px_per_um_x is None")
            
        if self.px_per_um_y is None :
            raise ValueError("px_per_um_x is None")
        
        if self.x_spot_pos is None :
            raise ValueError("x_spot_pos is None")
        
        if self.y_spot_pos is None :
            raise ValueError("y_spot_pos is None")
            
        dx = self.x_spot_pos - x
        dy = self.y_spot_pos - y
        
        um_displacement = (dx/self.px_per_um_x + dy/self.px_per_um_y) / 2
                    
        return um_displacement
    
    def save_data(self):
        data = self.get_calibration_data()
        # file_path = os.path.join('remote_focus_stabilisation', 'data_calibration.json')
        file_path = 'data_calibration.json'
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent = 4)
    
    def load_data(self):
        # file_path = os.path.join('remote_focus_stabilisation', 'data_calibration.json')
        file_path = 'data_calibration.json'
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                self.calibrated = data["calibrated"]
                self.px_per_um_x = data["px_per_um_x"]
                self.px_per_um_y = data ["px_per_um_y"]
                self.r2x = data["r2x"]
                self.r2y = data["r2y"]
                self.x_spot_pos = data["x_spot_pos"]
                self.y_spot_pos = data["y_spot_pos"]
                

class TLCameraThread(QThread):
    """
    Thread dedicated to continuously reading images from the Thorlabs TLCamera.
    Emits the most recent frame via the new_frame signal.
    """
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, tlcam, period_ms = 500):
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
        
    def change_folder(self, folder) :
        self.folder = folder
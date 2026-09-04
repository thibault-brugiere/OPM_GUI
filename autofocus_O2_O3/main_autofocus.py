# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:36:21 2025

Pour l'instant la partie qui a été faite est dans : Tools.signal_generators

@author: tbrugiere
"""
import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)

import os
import time

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    # Lancement en script : on relance en module pour activer les imports relatifs
    import sys
    from pathlib import Path

    pkg_root = Path(__file__).resolve().parent.parent  # dossier qui contient multiposition_acquisition/
    sys.path.insert(0, str(pkg_root))

from image_analysis.Deskew_Numpy import compute_px_shift
from hardware.functions_piezo import piezo_SAS
from autofocus_O2_O3.Config.autofocus_config import config
from autofocus_O2_O3.Hardware.daq_controller import NIDAQ_Acquisition
from autofocus_O2_O3.Hardware.camera_controller import camera_acquisition
from autofocus_O2_O3.Hardware.filter_wheel_controller import FilterWheel
from autofocus_O2_O3.Hardware.functions_serial_ports import functions_serial_ports
from autofocus_O2_O3.Tools.acquisition_pipeline.acquisition_worker import AutofocusAcquisitionWorker as AcquisitionWorker
from autofocus_O2_O3.Tools.regression import gaussian_fit, plot_gaussian_fit, create_black_graph, plot_show_gaussian_fit
from autofocus_O2_O3.Tools.signal_generators.multi_channel import generate_channel_signals


class AutofocusAcquisition(QObject):
    autofocus_result_ready = Signal(object, dict) 
    
    def __init__(self, hcams=None, filterwheel = None, piezo = None,
                 n_piezo_positions = 5, piezo_step_mm = 0.002, n_pixels = 10,
                 frequency=1e5, interface = False):
        super().__init__()
        print('[Main Autofocus] Start acquisition')
        
        self.hcams = hcams
        self.filterwheel = filterwheel
        self.fw_None = True if self.filterwheel is None else False # To properly close the filterwheel
        self.piezo = piezo if piezo is not None else piezo_SAS()
        
        self._own_piezo_connection = not self.piezo.connect()
        if self._own_piezo_connection :
            self.piezo.connect()
        
        if not self.piezo.is_referenced() :
            self.piezo.close()
            raise ValueError(f'Piezo must be hommed, current value : {self.piezo.is_referenced()}')
            
        self.frequency = frequency
        self.interface = interface
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)
        
        if self.config.experiment.mode != "autofocus" :
            raise NameError(f"Autofocus Error: not the right experiment mode: {self.config.experiment.mode}")
        
        if len(self.config.channels) != 1 :
            print(f"Autofocus Warning: the number of channel should be 1, current value {len(self.config.channels)}")
            
        if self.config.experiment.timepoints != 1:
            print(f"Autofocus Warning: the number of timepoints should be 1, current value {self.config.experiment.timepoint}")
            
        # Set the piezo for autofocus
        self.original_piezo_position = self.piezo.get_position()
        self.n_piezo_positions = n_piezo_positions
        self.piezo_step_mm = piezo_step_mm
        self.n_pixels = n_pixels
        self.piezo_positions = self.create_piezo_positions(self.n_piezo_positions, self.piezo_step_mm)
        self.px_shift = compute_px_shift(self.config.experiment.aspect_ratio,
                                         self.config.microscope.tilt_angle,
                                         self.config.cameras[0].binning,
                                         unit="deg")
        
        self.channel_name = self.config.channels[0].channel_id
        # Generate tension library
        self.volume_tensions_library = generate_channel_signals(self.config.cameras,
                                                                [self.config.channels[0]],
                                                                self.config.experiment,
                                                                self.config.microscope,
                                                                frequency = self.frequency)
        print("[Main Autofocus] channel signals generated")

        self.cameras_acquisition = []
        self.acquisition_workers = []
        self.daq = None
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }
        
        self.cw = False # Vérifie sur le countworker existe
        
    def create_piezo_positions(self, n_pos:int, step_mm:float) -> list:
        """
        Create a vector of piezo positions for autofocus

        Parameters
        ----------
        n_pos : int
            number of positions for the autofocus. Should be between 3 and 10
        step_mm : float
            step between two positions for autofocus in mm
            should be between 0.0001mm and 0.01 mm

        Returns
        -------
        positions : list
            list of positions in mm of the piezo during experiment
        """
        n_pos = min(max(3,n_pos),10)
        step_mm = min(max(0.0001,step_mm),0.01)
        pos = self.original_piezo_position
        min_pos = pos - step_mm * (n_pos -1) / 2
        positions = []
        for k in range(n_pos):
            positions.append(min_pos + k * step_mm)
        return positions

    def initialize_cameras(self):
        for i, cam_cfg in enumerate(self.config.cameras):
            hcam = self.hcams[i] if self.hcams else None
            cam = camera_acquisition(cam_cfg, hcam,
                                     channels = self.config.channels,
                                      experiment = self.config.experiment,
                                      microscope = self.config.microscope)
            if hcam is None:
                cam.initialize_camera()
            cam.configure_camera_for_acquisition()
            self.cameras_acquisition.append(cam)
            
        self.state['camera'] = 'ready'
        
        print("[Main Autofocus] camera initialized")
        
    def initialize_laser(self):
        """
        Note : si plusieurs cannaux utilisent le même laser contrôlé par une commande (chez nous le 561)
        seul la puissance du dernier cannal l'utilisant sera prise en compte
        """
        for laser in self.config.microscope.lasers:
            if self.config.microscope.OxxiusCombiner_port is not None:
                port = self.config.microscope.OxxiusCombiner_port
                command = self.config.microscope.OxxiusCombiner_command[laser]
                if command is not None:
                    for channel in self.config.channels:
                        if channel.laser_power[laser] > 0:
                            power = min(100.0, float(channel.laser_power[laser]))
                            command_to_send = command + " " + str(power)
                            response = functions_serial_ports.send_command_response(command_to_send,port)
                            print(f"[Main Autofocus] laser {laser} power set to {power}")
                            if response == str(power):
                                print("[Main Autofocus] command laser power set")
                            else:
                                print("[Main Autofocus] [ERROR] for command laser power setting")

    def initialize_acquisition_workers(self):
        for cam in self.cameras_acquisition:
            worker = AcquisitionWorker(
                camera_worker=cam,
                channel_name = self.channel_name,
                n_steps = self.config.experiment.n_steps,
                n_positions = self.n_piezo_positions,
                n_pixels = self.n_pixels,
                px_shift = self.px_shift,
                interface = self.interface)
            
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main Autofocus] acquisition workers initialized")
        
    def initialize_count_worker(self):
        pass
        
    def initialize_filterwheel(self):
        if self.filterwheel is None :
            self.filterwheel = FilterWheel()
            self.filterwheel.connect()
            self.filterwheel.home()
        else:
            if not self.filterwheel.connected :
                self.filterwheel.connect()
                # self.filterwheel.home() # TODO remettre ici
                
        print("[Main Autofocus] filter wheel initialized")
                
        self.filterwheel.moveToFilter(self.config.experiment.channels[0].filter)
        self.filterwheel.setTrigMove(0)

    def configure_daq(self):
        self.daq = NIDAQ_Acquisition()
        self.daq.send_signals_to_daq_single_channel(
            self.volume_tensions_library,
            self.config.experiment.timepoints,
            self.config.experiment.time_intervals,
            self.config.microscope.daq_channels,
            self.config.microscope.daq_channels_laser_analog_out,
            self.config.microscope.daq_channels_laser_digital_out,
            self.frequency)
        
        self.state['daq'] = 'ready'
        
        print("[Main Autofocus] DAQ ready")

    def run(self):    
        if not self._all_ready():
            print(f"Not ready to start : {self.state}")
            return
        
        print("[Main Autofocus] run acquisition")
        
        for worker in self.acquisition_workers:
            worker.start()
            
        for cam in self.cameras_acquisition:
            cam.start_acquisition()
            
        self.state = {'camera': 'acquiring',
                      'acquisition_workers' : 'processing',
                      'daq': 'controll'
                      }
        
        pos = 0 # Total positions acquired
        
        self.daq.arm_task()

        self.position = 0
        
        for piezo_position in self.piezo_positions :
            pos += 1
            self.position += 1
            
            self.piezo.move_to(piezo_position)

            while self.piezo.is_moving():
                time.sleep(0.01)

            self.daq.trigger_acquisition()
    
            expected_frames = pos * self.config.experiment.n_steps
            
            try:
                while True: # Wait until it reach the right number of frames 
                    images = [w.total_images for w in self.acquisition_workers]
                    
                    if all(v >= expected_frames for v in images):
                        break
            
            except:
                print("[INFO Autofocus] Acquisition interrupted by user.")
            
            time.sleep(0.011)
            
        self.stop_all()
        
        self.piezo_regression()
        
    def piezo_regression(self):
        x = self.piezo_positions
        y = self.acquisition_workers[0].get_max_px_intensity()
        
        y_fit, r2, x_max, y_max, parameters = gaussian_fit(x, y)
        
        if abs(x_max - self.original_piezo_position) < (self.piezo_step_mm * 1.5) :
            autofocus_quality = True
        else :
            autofocus_quality = False  
        
        if not self.interface :
            print(f"Original position = {self.original_piezo_position:6f}")
            print(f"    Best position = {x_max:.6f}")
            print(f"Max intensity = {y_max:.1f}")
            print(f"R² = {r2:.4f}")
            print(f'Autofocus good : {autofocus_quality}')
            if parameters is not None :
                plot_show_gaussian_fit(x, y, r2, x_max, y_max, parameters)
                
            if input("Do you want to use this calibration? [y/N]: ").strip().lower() == "y":
                self.piezo.move_to(x_max)
            else :
                self.piezo.move_to(self.original_piezo_position)    
        else :
            if parameters is not None :
                graph = plot_gaussian_fit(x, y, r2, x_max, y_max, parameters)
            else :
                graph = create_black_graph()  
                
            parameters = {
                "channel" : "autofocus",
                "original_piezo_position" : self.original_piezo_position,
                "best_piezo_position" : x_max,
                "max_intensity" : y_max,
                "R2" : r2,
                "quality" : autofocus_quality}
            
            self.autofocus_result_ready.emit(graph, parameters)
                
 
    def _all_ready(self):
        return all(v == 'ready' for v in self.state.values())

    def stop_all(self):
        """
        Stop all acquisition workers and DAQ tasks. Can be called at the end of acquisition
        or via external user action (e.g. GUI button).
        """

        for worker in self.acquisition_workers:
            worker.stop()
            
        for cam in self.cameras_acquisition :
            cam.stop_acquisition()
            cam.release_camera()
        
        if self.fw_None :
            self.filterwheel.close()

        if self.daq:
            if self.daq.state == "running" :
                self.daq.stop()
            if self.daq.state == "ready" :
                self.daq.close()
        
        if self._own_piezo_connection :
            self.piezo.close()

        print("[Main Autofocus] Acquisition stopped and hardware released.")
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }

##############################################################################

if __name__ == "__main__":
    Autofocus = AutofocusAcquisition()
    Autofocus.initialize_cameras()
    Autofocus.initialize_laser()
    Autofocus.initialize_acquisition_workers()
    Autofocus.initialize_filterwheel()
    Autofocus.configure_daq()
    Autofocus.run()

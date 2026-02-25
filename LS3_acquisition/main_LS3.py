# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:36:21 2025

Pour l'instant la partie qui a été faite est dans : Tools.signal_generators

@author: tbrugiere
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))

import math
import os
from PySide6.QtCore import QThread
import time

from Config.LS3_config import config
from Hardware.daq_controller import NIDAQ_Acquisition_ls3
from Hardware.camera_controller import camera_acquisition
from Hardware.filter_wheel_controller import FilterWheel
from Hardware.functions_serial_ports import functions_serial_ports
from Hardware.functions_Stage_ASI import Stage_ASI
# from Hardware.mock import Mock_functions_serial_ports as functions_serial_ports
# from Hardware.mock import MockDAQAcquisition as NIDAQ_Acquisition
# from Hardware.mock import MockCameraAcquisition as camera_acquisition
from Tools.acquisition_pipeline.acquisition_worker import AcquisitionWorker
from Tools.saving import prepare_saving_directory, save_metadata
from Tools.signal_generators.single_channel_ls3 import generate_channel_signals as generate_channel_signals_LS3


class Light_sheet_stabilized_scanning:
    def __init__(self, hcams=None, filterwheel = None, frequency=1e5, scanning_axis = "Y"):
        
        print('[Main LS3] Start Light sheet stabilized stage scanning')
        
        self.hcams = hcams
        self.filterwheel = filterwheel
        self.fw_None = True
        self.frequency = frequency
        self.scanning_axis = scanning_axis
        
        # Load configuration and get values
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)
        
        if self.config.experiment.mode != "LS3":
            raise NameError("LS3 Error: nnot the right experiment mode")
        
        self.n_channels = len(self.config.channels)
        self.n_lines = self._get_lines()
        
        self.filterseq = [] # Liste des filtres dans l'ordre utilisé
        for n in range(self.n_channels):
            self.filterseq.append(self.config.channels[n].filter)
        
        # Generate list of one tension library per channel
        self.list_volume_tensions_library = []
        volume_duration = 0
        for idx in range(len(self.config.experiment.channels)) :
            self.list_volume_tensions_library.append(
                generate_channel_signals_LS3(self.config.cameras,
                                             self.config.channels,
                                             self.config.experiment,
                                             self.config.microscope,
                                             idx,
                                             frequency = self.frequency))
            volume_duration += ( len(self.list_volume_tensions_library[idx]['tensions_galvo']) / self.frequency )

        print("[Main LS3] channel signals generated")

        # Prepare saving directory and metadata
        self.save_dir = prepare_saving_directory(self.config.experiment.data_path,
                                                 self.config.experiment.exp_name)
        save_metadata(self.config, self.save_dir)
        self.config.copy_parameters(self.save_dir)

        # Placeholders for hardware
        self.cameras_acquisition = []
        self.acquisition_workers = []
        self.daq = None
        
        self.state = {'camera': 'idle',
                      'acquisition_workers': 'idle',
                      'daq': 'idle',
                      'stage': 'idle',
                      }
        
    def _get_lines(self):
        field_size = self.config.cameras[0].pixel_size * self.config.cameras[0].hsize
        scanV_size = self.config.experiment.scanV_range
        scanV_overlap = self.config.experiment.scanV_overlap
        fied_overlap = scanV_overlap * field_size
        
        return math.ceil(scanV_size / (field_size - fied_overlap))
        
    def initialize_cameras(self):
        for i, cam_cfg in enumerate(self.config.cameras):
            hcam = self.hcams[i] if self.hcams else None
            cam = camera_acquisition(cam_cfg, hcam,
                                     channels = self.config.channels,
                                      experiment = self.config.experiment,
                                      microscope = self.config.experiment)
            if hcam is None:
                cam.initialize_camera()
            cam.configure_camera_for_acquisition()
            self.cameras_acquisition.append(cam)
            
        self.state['camera'] = 'ready'
        
        print("[Main LS3] camera initialized")
        
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
                            print(f"[Main LS3] laser {laser} power set to {power}")
                            if response == str(power):
                                print("[Main LS3] command laser power set")
                            else:
                                print("[Main LS3] [ERROR] for command laser power setting")

    def initialize_acquisition_workers(self):
        for cam in self.cameras_acquisition:
            worker = AcquisitionWorker(
                camera_worker = cam,
                save_dir = self.save_dir,
                n_steps = self.config.experiment.n_steps,
                n_lines = self.n_lines,
                n_channels = self.n_channels,
                channel_names = [ch.channel_id for ch in self.config.channels],
                mode = self.config.experiment.mode
            )
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main LS3] acquisition workers initialized")
        
    def initialize_filterwheel(self):
        if self.filterwheel is None :
            self.filterwheel = FilterWheel()
            self.filterwheel.connect()
            self.filterwheel.home()
            print("[Main LS3] filter wheel initialized")
        else:
            self.fw_None = False
            if not self.filterwheel.connected :
                self.filterwheel.connect()
                self.filterwheel.home()
                
            print("[Main LS3] filter wheel initialized")
                
        self.filterwheel.moveToFilter(self.filterseq[0])

    def configure_daq(self):
        self.daq = NIDAQ_Acquisition_ls3()
        
        self.state['daq'] = 'ready'
        
        print("[Main LS3] DAQ ready")
        
    def configure_stage(self):
        self.stage = Stage_ASI(port = self.config.microscope.stage_port)
        self.state['stage'] = 'ready'
    
    def _prepare_scan_parameters(self):
        """
        Prepare variables for scanning
        If there is only one axis, the scanning wil be made in one time
        """
        return {"n_lines" : 1 if self.n_channels == 1 else self.n_lines,
                "SCANR_start" : 0,
                "SCANR_stop" : self.config.experiment.stage_scan_range,
                "SCANV_start" : 0 if self.n_channels == 1 else 0,
                "SCANV_stop" : 0 if self.n_channels == 1 else 0,
                "SCANV_lines" : self.n_lines if self.n_channels == 1 else 1,
                "axis": self.scanning_axis
                }
        
    def run_acquisition(self):    
        if not self._all_ready():
            print(f"[Main LS3] Not ready to start : {self.state}")
            return
        
        print("[Main LS3] run acquisition")
        
        for worker in self.acquisition_workers:
            worker.start()
            
        for cam in self.cameras_acquisition:
            cam.start_acquisition()
            
        self.state = {'camera': 'acquiring',
                      'acquisition_workers' : 'processing',
                      'daq': 'controll',
                      'stage': 'moving'
                      }
        
        expected_volume_images = self.config.experiment.n_steps
        
        scan_parameters = self._prepare_scan_parameters()
        
        for line in range(scan_parameters["n_lines"]) :
            
            for chan in range(self.n_channels) :
                
                # go to the right filter
                self.filterwheel.moveToFilter(self.config.experiment.channels[chan].filter)
                
                # Prepare ni-daq
                tensions_library = self.list_volume_tensions_library[chan]
                
                self.scan_duration = len(tensions_library["tensions_galvo"]) / self.frequency
                
                self.daq.send_signals_to_daq_single_channel(
                    self.tensions_library,
                    1, # experiment.timepoints
                    self.config.experiment.time_intervals,
                    self.config.microscope.daq_channels,
                    self.config.microscope.daq_channels_laser_analog_out,
                    self.config.microscope.daq_channels_laser_digital_out,
                    self.frequency)
                
                self.daq.arm_task()
                
                self.daq.trigger_acquisition()
                
                # set scanning parameters and start scan
                SPEED = tensions_library["stage_speed_mm_s"]
                
                self.stage.set_scan(SPEED, scan_parameters["SCANR_start"], scan_parameters["SCANR_stop"],
                                    scan_parameters["SCANV_start"], scan_parameters["SCANV_stop"],
                                    scan_parameters["SCANV_lines"], scan_parameters["axis"])
                
                self.stage.start_scan()
                
                try:
                    while True:
                        images = [w.total_images for w in self.acquisition_workers]
                        if all(v >= expected_volume_images for v in images):
                            break
                        time.sleep(0.5)

                except:
                    print("[INFO] Acquisition interrupted by user.")
                    
                self.stage.set_speed()
                
                self.daq.stop()
                self.daq.close()
                
                expected_volume_images += self.config.experiment.n_steps
        
        self.stop_all()
        
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
            self.daq.stop()
            self.daq.close()

        print("[Main MDA] Acquisition stopped and hardware released.")
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }
        
    def worker(self,i):
        """
        Return the acquisition worker i to use in other processes
        """
        return self.acquisition_workers[i]

##############################################################################

if __name__ == "__main__":
    LS3 = Light_sheet_stabilized_scanning()
    LS3.initialize_cameras()
    LS3.initialize_laser()
    LS3.initialize_acquisition_workers()
    LS3.initialize_filterwheel()
    LS3.configure_daq()
    LS3.configure_stage()
    # LS3.initialize_count_worker()
    LS3.run_acquisition()

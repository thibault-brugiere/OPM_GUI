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

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    # Lancement en script : on relance en module pour activer les imports relatifs
    import sys
    from pathlib import Path

    pkg_root = Path(__file__).resolve().parent.parent  # dossier qui contient multidimensional_acquisition/
    sys.path.insert(0, str(pkg_root))
  
import math
import os
import time

from LS3_acquisition.Config.LS3_config import config
from LS3_acquisition.Hardware.daq_controller import NIDAQ_Acquisition_ls3
from LS3_acquisition.Hardware.camera_controller import camera_acquisition
from LS3_acquisition.Hardware.filter_wheel_controller import FilterWheel
from LS3_acquisition.Hardware.functions_serial_ports import functions_serial_ports
from LS3_acquisition.Hardware.functions_Stage_ASI import Stage_ASI
# from LS3_acquisition.Hardware.mock import Mock_functions_serial_ports as functions_serial_ports
# from LS3_acquisition.Hardware.mock import MockDAQAcquisition as NIDAQ_Acquisition
# from LS3_acquisition.Hardware.mock import MockCameraAcquisition as camera_acquisition
from LS3_acquisition.Tools.acquisition_pipeline.acquisition_worker import AcquisitionWorker
from LS3_acquisition.Tools.saving import prepare_saving_directory, save_metadata
from LS3_acquisition.Tools.signal_generators.single_channel_ls3 import generate_channel_signals as generate_channel_signals_LS3


class Light_sheet_stabilized_scanning:
    def __init__(self, hcams=None, filterwheel = None, frequency=1e5, scan_axis = 'Y'):
        
        print('[Main LS3] Start Light sheet stabilized stage scanning')
        
        self.hcams = hcams
        self.filterwheel = filterwheel
        self.fw_None = True if self.filterwheel is None else False # To properly close the filterwheel
        self.frequency = frequency
        self.scan_axis = scan_axis
        self.v_axis = "Y" if self.scan_axis == "X" else "X"
        
        # Load configuration and get values
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)
        
        if self.config.experiment.mode != "LS3":
            raise NameError("LS3 Error: not the right experiment mode")
        
        self.n_channels = len(self.config.channels)
        self._get_lines()
        self._get_n_steps()
        self.n_frames = self.config.experiment.n_steps * self.n_lines * self.n_channels
        self.stage_position = [0.0,0.0,0.0]
        
        # Generate list of one tension library per channel
        self._generate_tension_library()

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
        
    def _get_n_steps(self):
        """
        Calculate number of steps as the original value was for 
        """        
        self.config.experiment.n_steps = 1 + int(round(self.config.experiment.stage_scan_range / self.config.experiment.step_size))
        
    def _get_lines(self):
        sample_pixel_size = self.config.cameras[0].sample_pixel_size
        hsize = self.config.cameras[0].hsize
        field_size = sample_pixel_size * hsize
        scanV_size = self.config.experiment.scanV_range
        scanV_overlap = self.config.experiment.scanV_overlap
        fied_overlap = scanV_overlap * field_size
        
        if field_size < scanV_size :
            self.n_lines = math.ceil(scanV_size / (field_size - fied_overlap))
            final_field_overlap = (field_size * self.n_lines - scanV_size) / (self.n_lines - 1)
            self.config.experiment.scanV_overlap = final_field_overlap / hsize
        else :
            self.n_lines = 1

    def _generate_tension_library(self):
        """
        Generate liste of tension libraries per channel for ni-dac controll
        Also set the duration of one volume (not counting the return bach of the stage)
        """
        self.list_volume_tensions_library = []
        self.volume_duration = 0
        speeds = []
        for idx in range(len(self.config.experiment.channels)) :
            self.list_volume_tensions_library.append(
                generate_channel_signals_LS3(self.config.cameras,
                                             self.config.channels,
                                             self.config.experiment,
                                             self.config.microscope,
                                             idx,
                                             frequency = self.frequency))
            self.volume_duration += len(self.list_volume_tensions_library[idx]['tensions_galvo']) / self.frequency
            speeds.append(f'{self.list_volume_tensions_library[idx]["stage_speed_mm_s"]:5f}')
        
        print(f'[MAIN LS3] SPEED for channels are : {speeds} mm/s')
        # print(f'[MAIN LS3] SPEED for the first channel : {self.list_volume_tensions_library[0]["stage_speed_mm_s"]:4f} mm/s')
        print("[Main LS3] channel signals generated")
        
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
                mode = self.config.experiment.mode,
                max_volume_queue = 10
            )
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main LS3] acquisition workers initialized")
        
    def initialize_filterwheel(self):
        if self.filterwheel is None :
            self.filterwheel = FilterWheel()
            self.filterwheel.connect()
            # self.filterwheel.home()
            print("[Main LS3] filter wheel initialized")
        else:
            if not self.filterwheel.connected :
                self.filterwheel.connect()
                self.filterwheel.home()
                
            print("[Main LS3] filter wheel initialized")

    def configure_daq(self):
        self.daq = NIDAQ_Acquisition_ls3()
        
        self.state['daq'] = 'ready'
        
        print("[Main LS3] DAQ ready")
        
    def configure_stage(self):
        self.stage = Stage_ASI(port = self.config.microscope.stage_port)
        self.stage_position = self.stage.get_position() # Actual position in XYZ
        self.state['stage'] = 'ready'
    
    def _prepare_scan_parameters(self, v_pos = 0.0):
        """
        Prepare variables for scanning
        If there is only one axis, the scanning wil be made in one time
        The scanning is made around the center of the stage position when the experiment starts
        
        Parameters
        ----------
        v_pos : float, optionnal
            position of the stage if there is only one line at a time (for multicolors)
            
        """
        # Get the original position for each axis
        v_origin = self.stage_position[["X","Y","Z"].index(self.v_axis)]
        scan_origin = self.stage_position[["X","Y","Z"].index(self.scan_axis)]
        
        # for each axis, the scan is made in the original position +/- the scan_range / 2 
        
        return {
                "SCANR_start" : (self.config.experiment.stage_scan_range / 2 + scan_origin) / 1000,
                "SCANR_stop" : (-self.config.experiment.stage_scan_range / 2 + scan_origin) / 1000, #en mm
                "SCANV_start" : (- self.config.experiment.scanV_range / 2 + v_origin) / 1000 if self.n_channels == 1 else v_pos / 1000,
                "SCANV_stop" : (self.config.experiment.scanV_range / 2 + v_origin) / 1000 if self.n_channels == 1 else v_pos / 1000,
                "SCANV_lines" : self.n_lines if self.n_channels == 1 else 1,
                "axis": self.scan_axis
                }
    
    def _get_v_pos(self):
        """
        For multi color acquisition, calculate oll the position in the slow axis
        The scanning is made around the center of the stage position when the experiment starts

        Returns
        -------
        v_positions : list
            Positions of the stage in the slow axis

        """
        v_origin = self.stage_position[["X","Y","Z"].index(self.v_axis)]
        if self.n_lines > 1 :
            SCANV_start = - self.config.experiment.scanV_range / 2 + v_origin
            SCANV_stop = self.config.experiment.scanV_range / 2 + v_origin
            SCANV_range = SCANV_stop - SCANV_start # Je fais ici comme ça pour si un momejt la fonction fonctionne avec un début et une fin
            step = SCANV_range / (self.n_lines - 1)
            v_positions = []
            for k in range(self.n_lines):
                v_positions.append(SCANV_start + step * k)
        else :
            v_positions = [v_origin]
        return v_positions
    
    def run_acquisition(self):
        """
        There are two possibility for the running of the acquisition :
            -If there is only on channel, the stage scans the entire field of view
            and trig the ni-dac at each lines
            -If there are more than 1 channels, the function sets the scan line by line
        """
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
        
        lines_to_set = self.n_lines if self.n_channels != 1 else 1 #If the is only one channel, the scanning is made in one step
        v_positions = self._get_v_pos()
        total_volumes = 0

        for line in range(lines_to_set) :
            
            for chan in range(self.n_channels) :
                
                scan_parameters = self._prepare_scan_parameters(v_positions[line])
                
                # go to the right filter
                self.filterwheel.moveToFilter(self.config.experiment.channels[chan].filter)
                
                # Prepare ni-daq
                tensions_library = self.list_volume_tensions_library[chan]
                
                self.daq.send_signals_to_daq_single_channel(
                    tensions_library,
                    1, # experiment.timepoints
                    self.config.experiment.time_intervals,
                    self.config.microscope.daq_channels,
                    self.config.microscope.daq_channels_laser_analog_out,
                    self.config.microscope.daq_channels_laser_digital_out,
                    self.frequency)
                
                self.daq.arm_task()
                                
                # set scanning parameters and start scan
                SPEED = tensions_library["stage_speed_mm_s"]
                
                self.stage.set_scan(SPEED, scan_parameters["SCANR_start"], scan_parameters["SCANR_stop"],
                                    scan_parameters["SCANV_start"], scan_parameters["SCANV_stop"],
                                    scan_parameters["SCANV_lines"], scan_parameters["axis"])
                
                self.stage.start_scan()
                
                # Calculate the number of the volume and the expected frames
                
                total_volumes += 1
                
                expected_frames = self.config.experiment.n_steps * total_volumes
                
                try:
                    while True: # Wait until it reach the right number of frames 
                        images = [w.total_images for w in self.acquisition_workers]
                        if all(v >= expected_frames for v in images):
                            break
                        time.sleep(0.05)
                    while self.stage.is_moving(): # Wait until stage stops moving 
                        time.sleep(0.05)
                        
                except:
                    print("[INFO] Acquisition interrupted by user.")
                
                self.daq.close()
                self.daq.stop()
                    
        self.stage.set_speed() # Put back the stage to riginal speed
        self.stage.go_to_position(self.stage_position)
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

        print("[Main LS3] Acquisition stopped and hardware released.")
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }

##############################################################################

if __name__ == "__main__":
    LS3 = Light_sheet_stabilized_scanning()
    LS3.initialize_cameras()
    LS3.initialize_laser()
    LS3.initialize_filterwheel()
    LS3.configure_daq()
    LS3.configure_stage()
    LS3.initialize_acquisition_workers()
    LS3.run_acquisition()
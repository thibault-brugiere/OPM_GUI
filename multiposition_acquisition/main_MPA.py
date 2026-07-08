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
from PySide6.QtCore import QThread
import time
from tqdm import tqdm

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    # Lancement en script : on relance en module pour activer les imports relatifs
    import sys
    from pathlib import Path

    pkg_root = Path(__file__).resolve().parent.parent  # dossier qui contient multiposition_acquisition/
    sys.path.insert(0, str(pkg_root))


from multiposition_acquisition.Config.MPA_config import config
from multiposition_acquisition.Config.positions import Positions
from multiposition_acquisition.Hardware.daq_controller import NIDAQ_Acquisition
from multiposition_acquisition.Hardware.camera_controller import camera_acquisition
from multiposition_acquisition.Hardware.filter_wheel_controller import FilterWheel
from multiposition_acquisition.Hardware.functions_Stage_ASI import Stage_ASI
from multiposition_acquisition.Hardware.functions_serial_ports import functions_serial_ports
# from multiposition_acquisition.Hardware.mock import Mock_functions_serial_ports as functions_serial_ports
# from multiposition_acquisition.Hardware.mock import MockDAQAcquisition as NIDAQ_Acquisition
# from multiposition_acquisition.Hardware.mock import MockCameraAcquisition as camera_acquisition
from multiposition_acquisition.Tools.acquisition_pipeline.acquisition_worker import AcquisitionWorker
from multiposition_acquisition.Tools.acquisition_pipeline.count_worker import CountWorker, mouvement_sequence
from multiposition_acquisition.Tools.saving import prepare_saving_directory, save_metadata
from multiposition_acquisition.Tools.signal_generators.multi_channel import generate_channel_signals

class MultiPositionAcquisition:
    def __init__(self, hcams=None, filterwheel = None, frequency=1e5):
        
        print('[Main MPA] Start multiposition acquisition')
        
        self.hcams = hcams
        self.filterwheel = filterwheel
        self.stage = Stage_ASI()
        self.fw_None = True if self.filterwheel is None else False # To properly close the filterwheel
        self.frequency = frequency
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)
        self.n_channels = len(self.config.channels)
        self.n_positions = self.config.experiment.positions
        self.remaining_time = 0.0
        self.timepoint = 0
        self.position = 0
        
        self.positions = Positions()
        self.positions.load(os.path.join(config_path, "positions.json"))
        
        self.timepoint_values = [] # Time of the starting of each timepoint
        
        
        if self.config.experiment.mode != "multiposition" :
            raise NameError(f"MPA Error: not the right experiment mode: {self.config.experiment.mode}")
        
        self.filterseq = [] # Liste des filtres dans l'ordre utilisé
        for n in range(self.n_channels):
            self.filterseq.append(self.config.channels[n].filter)
            
        self.filters_mouve = mouvement_sequence(self.config.microscope.filters , self.filterseq)
        
        print(f"[Main MPA] experiment mode : {self.config.experiment.mode}")
                
        self.volume_tensions_library = generate_channel_signals(self.config.cameras,
                                                                self.config.channels,
                                                                self.config.experiment,
                                                                self.config.microscope,
                                                                frequency = self.frequency)
        print("[Main MPA] channel signals generated")

        volume_duration = len(self.volume_tensions_library['tensions_galvo']) / self.frequency
        print(f'[Main MPA] volume duration : {volume_duration} s')
        if self.n_positions * volume_duration > self.config.experiment.time_intervals + 1.0 * self.n_positions :
            self.config.experiment.time_intervals = volume_duration + 1.0 * self.n_positions
            print(f"[INFO] Time interval too short. Adjusted to : {self.config.experiment.time_intervals} s to match volume duration.")
        
        # Prepare saving directory and metadata
        self.save_dir = prepare_saving_directory(self.config.experiment.data_path,
                                                 self.config.experiment.exp_name)
        save_metadata(self.config, self.save_dir)
        self.config.copy_parameters(self.save_dir)
        self.positions.save(os.path.join(self.save_dir, "positions.json"))
        
        # Placeholders for hardware
        self.cameras_acquisition = []
        self.acquisition_workers = []
        self.daq = None
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }
        
        self.cw = False # Vérifie sur le countworker existe

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
        
        print("[Main MPA] camera initialized")
        
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
                            print(f"[Main MPA] laser {laser} power set to {power}")
                            if response == str(power):
                                print("[Main MPA] command laser power set")
                            else:
                                print("[Main MPA] [ERROR] for command laser power setting")

    def initialize_acquisition_workers(self):
        for cam in self.cameras_acquisition:
            worker = AcquisitionWorker(
                camera_worker=cam,
                save_dir=self.save_dir,
                n_steps=self.config.experiment.n_steps,
                timepoints=self.config.experiment.timepoints,
                n_channels = self.n_channels,
                n_positions = self.n_positions,
                channel_names=[ch.channel_id for ch in self.config.channels],
                mode = self.config.experiment.mode
            )
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main MPA] acquisition workers initialized")
        
    def initialize_filterwheel(self):
        if self.filterwheel is None :
            self.filterwheel = FilterWheel()
            self.filterwheel.connect()
            self.filterwheel.home()
            print("[Main MPA] filter wheel initialized")
        else:
            if not self.filterwheel.connected :
                self.filterwheel.connect()
                self.filterwheel.home()
                
            print("[Main MPA] filter wheel initialized")
                
        self.filterwheel.moveToFilter(self.filterseq[0])
        if self.n_channels == 1 :
            self.filterwheel.setTrigMove(0)
        else:
            self.filterwheel.setTrigMove(self.filters_mouve[0])

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
        
        print("[Main MPA] DAQ ready")
        
    def initialize_count_worker(self):
        """
        worker used to properly set the position of the filter wheel at the right moment during the acquisition

        Returns
        -------
        None.

        """
        self.count_worker = CountWorker(self.daq, self.filterwheel, self.filters_mouve)
        self.count_thread = QThread()
        self.count_worker.moveToThread(self.count_thread)
        self.count_thread.started.connect(self.count_worker.start)
        self.count_worker.trigger_received.connect(self.on_trigger_detected)
        self.count_thread.start()
        
        self.cw = True
        
        print("[Main MPA] count workers initialized")
        
    def on_trigger_detected(self, count):
        # print(f"Trigger reçu : {count}")
        pass

    def run(self):    
        if not self._all_ready():
            print(f"Not ready to start : {self.state}")
            return
        
        print("[Main MPA] run acquisition")
        
        timepoints = self.config.experiment.timepoints
        
        # Initialize tqdm bars
        self.position_bar = tqdm(total=self.n_positions, desc="Positions       ", position=2)
        self.timepoint_bar = tqdm(total=timepoints, desc="Timepoints      ", position=3)
        self.remaining_time_message = tqdm(total=0, bar_format="{desc}", position=4)
        
        for worker in self.acquisition_workers:
            worker.start()
            
        for cam in self.cameras_acquisition:
            cam.start_acquisition()
            
        self.state = {'camera': 'acquiring',
                      'acquisition_workers' : 'processing',
                      'daq': 'controll'
                      }
        
        time_pos = 0 # Total timepoints and positions acquired
        
        self.daq.arm_task()
        
        time_start = time.time()
        
        for timepoint in range(timepoints) :
            self.timepoint_values.append(time.time())
            self.timepoint_bar.update(1)
            self.timepoint += 1
            self.position_bar.n = 0
            self.position_bar.refresh()
            self.position = 0
            for position in self.positions :
                if position.enabled :
                    time_pos += 1
                    self.position = (self.position % self.n_positions) + 1
                    
                    self.stage.go_to_position([position.x * 1000, position.y * 1000, position.z * 1000 ])
                    
                    # print(f"timepoint {timepoint}, position {position.name}")
                    
                    while self.stage.is_moving() :
                        time.sleep(0.01)
        
                    self.daq.trigger_acquisition()
            
                    expected_frames = time_pos * self.n_channels * self.config.experiment.n_steps
                    # print(f"Expected Frames : {expected_frames}")
                    
                    try:
                        while True: # Wait until it reach the right number of frames 
                            images = [w.total_images for w in self.acquisition_workers]
                            # print(f"images {images}")
                            
                            if all(v >= expected_frames for v in images):
                                # print(f"Acquired Frames {images}")
                                break
                    
                            
                    except:
                        print("[INFO] Acquisition interrupted by user.")
                        
                    self.position_bar.n = self.position
                    self.position_bar.refresh()
                    
                    time.sleep(0.011)
                    
            self.remaining_time = time_start + (timepoint + 1) * self.config.experiment.time_intervals - time.time()
            if self.remaining_time >= 0 :
                self.remaining_time_message.set_description_str(f"{self.remaining_time:.2f}s remaining between frames...")
                self.remaining_time_message.refresh()
                time.sleep(self.remaining_time)
            else :
                self.remaining_time_message.set_description_str(f"{-self.remaining_time:.2f}s missing between frames...")
                self.remaining_time_message.refresh()

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
        
        self.count_worker.stop()
        
        self.count_thread.quit()
        self.count_thread.wait()
        
        if self.fw_None :
            self.filterwheel.close()

        if self.daq:
            if self.daq.state == "running" :
                self.daq.stop()
            if self.daq.state == "ready" :
                self.daq.close()

        print("[Main MPA] Acquisition stopped and hardware released.")
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }

##############################################################################

if __name__ == "__main__":
    MPA = MultiPositionAcquisition()
    MPA.initialize_cameras()
    MPA.initialize_laser()
    MPA.initialize_acquisition_workers()
    MPA.initialize_filterwheel()
    MPA.configure_daq()
    MPA.initialize_count_worker()
    MPA.run()

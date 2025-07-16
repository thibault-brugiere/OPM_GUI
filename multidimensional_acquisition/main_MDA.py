# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:36:21 2025

Pour l'instant la partie qui a été faite est dans : Tools.signal_generators

@author: tbrugiere
"""
import os
import time

from Config.MDA_config import config
from Hardware.daq_controller import NIDAQ_Acquisition
from Hardware.camera_controller import camera_acquisition
# from Hardware.mock import MockDAQAcquisition as NIDAQ_Acquisition
# from Hardware.mock import MockCameraAcquisition as camera_acquisition
from Tools.acquisition_pipeline.acquisition_worker import AcquisitionWorker
from Tools.saving import prepare_saving_directory, save_metadata
from Tools.signal_generators.single_channel import generate_single_channel_signals

class MultidimensionalAcquisition:
    def __init__(self, hcams=None, frequency=1e4):
        
        print('[Main MDA] Start multidimensionnal acquisition')
        
        self.hcams = hcams
        self.frequency = frequency
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)

        self.n_channels = len(self.config.channels)
        if self.n_channels == 1:
            self.volume_tensions_library = generate_single_channel_signals(
                self.config.cameras,
                self.config.channels,
                self.config.experiment,
                self.config.microscope,
                self.frequency)

            volume_duration = len(self.volume_tensions_library['tensions_galvo']) / self.frequency
            print(f'[Main MDA] volume duration : {volume_duration} s')
            if volume_duration > self.config.experiment.time_intervals + 0.001:
                self.config.experiment.time_intervals = volume_duration + 0.001
                print(f"[INFO] Time interval too short. Adjusted to : {volume_duration + 0.001} s to match volume duration.")
        else:
            raise NotImplementedError("Only single-channel acquisition is currently supported.")
        
        # Prepare saving directory and metadata
        self.save_dir = prepare_saving_directory(self.config.experiment.data_path,
                                                 self.config.experiment.exp_name)
        save_metadata(self.config, self.save_dir)

        # Placeholders for hardware
        self.cameras_acquisition = []
        self.acquisition_workers = []
        self.daq = None
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }

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
        
        print("[Main MDA] camera initialized")

    def initialize_acquisition_workers(self):
        for cam in self.cameras_acquisition:
            worker = AcquisitionWorker(
                camera_worker=cam,
                save_dir=self.save_dir,
                n_steps=self.config.experiment.n_steps,
                timepoints=self.config.experiment.timepoints,
                channel_names=[ch.channel_id for ch in self.config.channels],
            )
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main MDA] acquisition workers initialized") 

    def configure_daq(self):
        self.daq = NIDAQ_Acquisition()
        self.daq.send_signals_to_daq_single_channel(
            self.volume_tensions_library,
            self.config.experiment.timepoints,
            self.config.experiment.time_intervals,
            self.config.microscope.daq_channels,
            self.frequency)
        
        self.state['daq'] = 'ready'
        
        print("[Main MDA] DAQ ready")

    def run(self):    
        if not self._all_ready():
            print(f"Not ready to start : {self.state}")
            return
        
        print("[Main MDA] run acquisition")
        
        for worker in self.acquisition_workers:
            worker.start()
            
        for cam in self.cameras_acquisition:
            cam.start_acquisition()

        self.daq.arm_task()
        self.daq.trigger_acquisition()
        
        # Wait until all volumes are acquired
        expected_images = self.config.experiment.timepoints * self.config.experiment.n_steps
        try:
            while True:
                images = [w.total_images for w in self.acquisition_workers]
                if all(v >= expected_images for v in images):
                    # print("[INFO] All volumes acquired.")
                    break
                time.sleep(0.5)
        except:
            print("[INFO] Acquisition interrupted by user.")
        
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
            cam.stop_acquisition
            cam.release_camera

        if self.daq:
            self.daq.stop()
            self.daq.close()

        print("[INFO] Acquisition stopped and hardware released.")
        
        self.state = {'camera': 'idle',
                      'acquisition_workers' : 'idle',
                      'daq': 'idle'
                      }

##############################################################################

if __name__ == "__main__":
    MDA = MultidimensionalAcquisition()
    MDA.initialize_cameras()
    MDA.initialize_acquisition_workers()
    MDA.configure_daq()
    MDA.run()

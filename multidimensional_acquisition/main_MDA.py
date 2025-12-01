# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:36:21 2025

Pour l'instant la partie qui a été faite est dans : Tools.signal_generators

@author: tbrugiere
"""
import math
import os
from PySide6.QtCore import QThread
import time

from Config.MDA_config import config
from Hardware.daq_controller import NIDAQ_Acquisition
from Hardware.camera_controller import camera_acquisition
from Hardware.filter_wheel_controller import FilterWheel
from Hardware.functions_serial_ports import functions_serial_ports
# from Hardware.mock import Mock_functions_serial_ports as functions_serial_ports
# from Hardware.mock import MockDAQAcquisition as NIDAQ_Acquisition
# from Hardware.mock import MockCameraAcquisition as camera_acquisition
from Tools.acquisition_pipeline.acquisition_worker import AcquisitionWorker
from Tools.acquisition_pipeline.count_worker import CountWorker, mouvement_sequence
from Tools.saving import prepare_saving_directory, save_metadata
from Tools.signal_generators.multi_channel import generate_channel_signals
from Tools.signal_generators.multi_channel_ultra_fast import generate_channel_signals as generate_signals_fast

class MultidimensionalAcquisition:
    def __init__(self, hcams=None, filterwheel = None, frequency=1e5):
        
        print('[Main MDA] Start multidimensionnal acquisition')
        
        self.hcams = hcams
        self.filterwheel = filterwheel
        self.fw_None = True
        self.frequency = frequency
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        self.config = config(dirname=config_path)
        self.n_channels = len(self.config.channels)
        
        self.filterseq = [] # Liste des filtres dans l'ordre utilisé
        for n in range(self.n_channels):
            self.filterseq.append(self.config.channels[n].filter)
            
        self.filters_mouve = mouvement_sequence(self.config.microscope.filters , self.filterseq)
            
        if self.config.experiment.mode == "standard" :
            self.volume_tensions_library = generate_channel_signals(self.config.cameras,
                                                                    self.config.channels,
                                                                    self.config.experiment,
                                                                    self.config.microscope,
                                                                    frequency = 1e5)
            print("[Main MDA] channel signals generated")
            
        if self.config.experiment.mode == "fast" :
            min_exposure_time = math.ceil(100*self.config.cameras[0].image_readout_time*1000)/100
            for channel in self.config.channels :
                if channel.exposure_time < min_exposure_time:
                    channel.exposure_time = min_exposure_time
                    print(f"[INFO] Exposure time to low for {channel.channel_id}, exposure time set to {min_exposure_time}ms")
            self.volume_tensions_library = generate_signals_fast(self.config.cameras,
                                                                 self.config.channels,
                                                                 self.config.experiment,
                                                                 self.config.microscope,
                                                                 frequency = 1e5)
            print("[Main MDA] channel signals generated")
            
        volume_duration = len(self.volume_tensions_library['tensions_galvo']) / self.frequency
        print(f'[Main MDA] volume duration : {volume_duration} s')
        if volume_duration > self.config.experiment.time_intervals + 0.001:
            self.config.experiment.time_intervals = volume_duration + 0.001
            print(f"[INFO] Time interval too short. Adjusted to : {volume_duration + 0.001} s to match volume duration.")
        
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
                                      microscope = self.config.experiment)
            if hcam is None:
                cam.initialize_camera()
            cam.configure_camera_for_acquisition()
            self.cameras_acquisition.append(cam)
            
        self.state['camera'] = 'ready'
        
        print("[Main MDA] camera initialized")
        
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
                            print(f"[Main MDA] laser {laser} power set to {power}")
                            if response == str(power):
                                print("[Main MDA] command laser power set")
                            else:
                                print("[Main MDA] [ERROR] for command laser power setting")

    def initialize_acquisition_workers(self):
        for cam in self.cameras_acquisition:
            worker = AcquisitionWorker(
                camera_worker=cam,
                save_dir=self.save_dir,
                n_steps=self.config.experiment.n_steps,
                timepoints=self.config.experiment.timepoints,
                n_channels = self.n_channels,
                channel_names=[ch.channel_id for ch in self.config.channels],
                mode = self.config.experiment.mode
            )
            self.acquisition_workers.append(worker)
            
        self.state['acquisition_workers'] = 'ready'
        
        print("[Main MDA] acquisition workers initialized")
        
    def initialize_filterwheel(self):
        if self.filterwheel is None :
            self.filterwheel = FilterWheel()
            self.filterwheel.connect()
            self.filterwheel.home()
            print("[Main MDA] filter wheel initialized")
        else:
            self.fw_None = False
            if not self.filterwheel.connected :
                self.filterwheel.connect()
                self.filterwheel.home()
                
            print("[Main MDA] filter wheel initialized")
                
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
        
        print("[Main MDA] DAQ ready")
        
    def initialize_count_worker(self):
        self.count_worker = CountWorker(self.daq, self.filterwheel, self.filters_mouve)
        self.count_thread = QThread()
        self.count_worker.moveToThread(self.count_thread)
        self.count_thread.started.connect(self.count_worker.start)
        self.count_worker.trigger_received.connect(self.on_trigger_detected)
        self.count_thread.start()
        
        self.cw = True
        
        print("[Main MDA] count workers initialized")
        
        
    def on_trigger_detected(self, count):
        # print(f"Trigger reçu : {count}")
        pass
        

    def run(self):    
        if not self._all_ready():
            print(f"Not ready to start : {self.state}")
            return
        
        print("[Main MDA] run acquisition")
        
        for worker in self.acquisition_workers:
            worker.start()
            
        for cam in self.cameras_acquisition:
            cam.start_acquisition()
            
        self.state = {'camera': 'acquiring',
                      'acquisition_workers' : 'processing',
                      'daq': 'controll'
                      }

        self.daq.arm_task()
        self.daq.trigger_acquisition()
        
        # Wait until all volumes are acquired
        expected_images = self.config.experiment.timepoints * self.n_channels * self.config.experiment.n_steps
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
            cam.stop_acquisition()
            cam.release_camera()
        
        self.count_worker.stop()
        
        self.count_thread.quit()
        self.count_thread.wait()
        
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
    MDA = MultidimensionalAcquisition()
    MDA.initialize_cameras()
    MDA.initialize_laser()
    MDA.initialize_acquisition_workers()
    MDA.initialize_filterwheel()
    MDA.configure_daq()
    MDA.initialize_count_worker()
    MDA.run()

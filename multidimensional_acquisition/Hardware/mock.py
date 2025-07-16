# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:20:53 2025

@author: tbrugiere
"""
import time
import numpy as np

class MockCameraAcquisition:

# ==============================
# MOCK CAMERA ACQUISITION CLASS
# ==============================

    """
    Simulates a camera acquisition triggered by a DAQ signal every volume.
    Returns synthetic image stacks, tracking time intervals between triggers.
    """
    def __init__(self, camera, hcam=None, channels=None, experiment=None, microscope=None):
        """
        Initialize mock camera acquisition.
        Simulates a camera triggered by a DAQ volume-wise.
    
        Parameters:
        - camera: camera config object
        - hcam: not used, for compatibility
        - channels, experiment, microscope: full config used to access acquisition timing
        """
        self.camera = camera
        self.hcam = hcam
        self.channels = channels
        self.experiment = experiment
        self.microscope = microscope
    
        self.image_shape = (camera.vsize, camera.hsize)
        self.acquiring = False
        self.state = "idle"
        
        if self.hcam is not None :
            self.state = "initialized"
            
        self.start_time = None
        self.last_read_time = None
        self.frames_per_volume = experiment.n_steps if experiment else 10
        self.volume_interval = experiment.time_intervals if experiment else 1.0
        self.timepoints = self.experiment.timepoints
        self.total_frames =  self.timepoints * self.frames_per_volume
        self.generated_frames = 0

    def initialize_camera(self):
        if self.hcam is not None:
            raise RuntimeError("Camera already initialized")
            
        self.state = "initialized"
        self.hcam = True
        
    def configure_camera_for_acquisition(self):
        if self.hcam is None:
            raise RuntimeError("Camera is not initialized. Call initialize_camera() first.")
            
        self.state = "configured"
        

    def start_acquisition(self):
        if self.state != "configured" :
            raise RuntimeError("Camera not configured. Call initialize_camera() first.")
            
        self.acquiring = True
        self.start_time = time.time()
        self.last_read_time = self.start_time
        self.state = "acquiring"

    def stop_acquisition(self):
        if self.state != "acquiring" :
            raise RuntimeError("Camera not initialized. Call initialize_camera() first.")
            
        self.acquiring = False
        self.state = "configured"

    def release_camera(self):
        if self.hcam is not None:
            self.acquiring = False
            self.hcam = None
            self.state = "idle"

    def read_camera(self):
        """
        Simulates reading the camera buffer.

        - Computes how much time passed since last read
        - Determines how many volume triggers would have occurred
        - Returns n_steps × volumes synthetic frames
        """
        # if self.state != "acquiring":
        #     raise RuntimeError("Camera not acquiring. start acquisition first.")
            
        if not self.acquiring:
            return []

        now = time.time()
        elapsed_since_last = now - self.last_read_time

        # Determine how many volumes should have been acquired since last read
        expected_volumes = int(elapsed_since_last / self.volume_interval)
        frames_to_return = expected_volumes * self.frames_per_volume
        if frames_to_return > 0 and self.generated_frames < self.total_frames :
            self.last_read_time = now
            self.generated_frames = self.generated_frames + frames_to_return
            return [
                np.random.randint(0, 256, self.image_shape, dtype=np.uint16)
                for _ in range(frames_to_return)
            ]
        else:
            return []

    def legalize_roi(self):
        return []
    
    def get_image_shape(self):
        return self.camera.vsize, self.camera.hsize


class MockDAQAcquisition:
# =========================
# MOCK DAQ CONTROL CLASS
# =========================

    """
    Mock DAQ class that simulates volume triggering at regular intervals.
    """
    def __init__(self):
        """
        Initialize mock DAQ class. It simulates task state transitions.
        """
        self.state = "idle"

    def send_signals_to_daq_single_channel(self, tensions_library, timepoints, time_intervals,
                                           daq_channels, frequency=1e4):
        """
        Configure the mock DAQ with acquisition parameters.
        """
        self.timepoints = timepoints
        self.time_intervals = time_intervals
        self.state = "ready"

    def arm_task(self):
        """
        Set the mock DAQ to "armed" state before triggering.
        """
        if self.state != "ready":
            raise RuntimeError("[MOCK DAQ] Cannot arm unless state is 'ready'.")
        self.state = "armed"

    def trigger_acquisition(self):
        """
        Simulate the DAQ triggering acquisition at regular intervals.
        Displays simulated volume triggers.
        """
        if self.state != "armed":
            raise RuntimeError("[MOCK DAQ] Cannot trigger unless state is 'armed'.")
        self.state = "running"

        # Simulate periodic triggering
        for i in range(self.timepoints):
            time.sleep(self.time_intervals)

        self.state = "complete"

    def stop(self):
        """
        Simulate stopping DAQ tasks.
        """
        if self.state != "running" and self.state != "armed":
            return

        self.state = "ready"

    def close(self):
        """
        Simulate closing/releasing DAQ resources.
        """
        
        self.state = "idle"


# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 14:00:18 2025

@author: tbrugiere
"""

import json
import os

from configs.config import camera, channel_config, experiment, microscope

class config():
    """
    Configuration manager for the acquisition program.
    
    This class loads and converts the GUI-defined microscope configuration
    (stored in a JSON file) into Python objects: cameras, channels,
    experiment and microscope settings.
    """
    
    def __init__(self, dirname = ""):
        """
        Initialize the config object.
        
        Parameters
        ----------
        dirname : str, optional
            Path to the directory containing the configuration JSON file.
            If empty, the current directory is used.
        
        Actions
        -------
        - Loads parameters from GUI_parameters.json
        - Converts the dictionary into camera, channel, experiment, and microscope objects.
        """
        
        self.dirname = dirname
        self.GUI_parameters = self.load_parameters_from_GUI()
        
        self.cameras, self.channels, self.experiment, self.microscope = self.GUI_parameters_to_config()
    
    def load_parameters_from_GUI(self, filename = 'GUI_parameters.json'):
        """
        Load microscope parameters from a GUI-generated JSON file.
    
        Parameters
        ----------
        filename : str
            Name of the JSON file containing the configuration.
    
        Returns
        -------
        dict
            Dictionary of parameters loaded from the file.
        """
        dirname = self.dirname
        file_path = os.path.join(dirname, filename)   # Construct full path to the file
        
        with open(file_path, 'r') as json_file:
            parameters = json.load(json_file)
        return parameters
    
    def GUI_parameters_to_config(self):
        """
        Convert the loaded dictionary of parameters into proper configuration objects.
        
        Returns
        -------
        tuple
            A tuple containing:
            - cameras (list): list of camera objects
            - channels (list): list of channel_config objects
            - experiment (experiment): experiment object
            - microscope (microscope): microscope object
        """
        
        config_dict  = self.GUI_parameters
        
        # 1. Create camera objects from dictionary entries
        cameras = []
        for cam_key, cam_data in config_dict["cameras"].items():
            cam = camera(camera_id=cam_data["camera_id"])
            cam.hchipsize = cam_data["hchipsize"]
            cam.vchipsize = cam_data["vchipsize"]
            cam.pixel_size = cam_data["pixel_size"]
            cam.sample_pixel_size = cam_data["sample_pixel_size"]
            cam.hsize = cam_data["hsize"]
            cam.hpos = cam_data["hpos"]
            cam.vsize = cam_data["vsize"]
            cam.vpos = cam_data["vpos"]
            cam.exposure_time = cam_data["exposure_time"]
            cam.binning = cam_data["binning"]
            cam.line_readout_time = cam_data["line_readout_time"]
            # image_readout_time is not used in the camera object, but could be stored if needed
            cameras.append(cam)
    
        # 2. Create channel objects with laser configuration
        channels = []
        for chan_key, chan_data in config_dict["channels"].items():
            chan = channel_config(channel_id=chan_data["channel_id"])
            chan.is_active = chan_data["is_active"]
            chan.channel_order = chan_data["channel_order"]
            chan.camera = chan_data["camera"]
            chan.exposure_time = chan_data["exposure_time"]
            chan.filter = chan_data["filter"]
            chan.laser_is_active.update(chan_data["laser_is_active"])
            chan.laser_power.update(chan_data["laser_power"])
            channels.append(chan)
    
        # 3. Create the experiment object
        exp_data = config_dict["experiment"]
        exp = experiment()
        exp.exp_name = exp_data["exp_name"]
        exp.data_path = exp_data["data_path"]
        exp.timepoints = exp_data["timepoints"]
        exp.time_intervals = exp_data["time_intervals"]
        exp.total_duration = exp_data["total_duration"]
        exp.scanner_position = exp_data["scanner_position"]
        exp.scan_range = exp_data["scan_range"]
        exp.aspect_ratio = exp_data["aspect_ratio"]
        exp.n_steps = exp_data["n_steps"]
        exp.step_size = exp_data["step_size"]
        exp.slit_aperture = exp_data["slit_aperture"]
        exp.cameras = cameras
        exp.channels = channels
    
        # 4. Create and populate the microscope object with mechanical and optical settings
        micro_data = config_dict["microscope"]
        micro = microscope()
        micro.tilt_angle = micro_data["tilt_angle"]
        micro.mag_total = micro_data["mag_total"]
        micro.volts_per_um = micro_data["volts_per_um"]
        micro.galvo_response_time = micro_data["galvo_response_time"]
        micro.galvo_flyback_time = micro_data["galvo_flyback_time"]
        micro.stage_port = micro_data["stage_port"]
        micro.filters = micro_data["filters"]
        micro.lasers = micro_data["lasers"]
        micro.volts_per_laser_percent = micro_data["volts_per_laser_percent"]
        micro.laser_response_time = micro_data["laser_response_time"]
        micro.daq_channels.update(micro_data["daq_channels"])
    
        return cameras, channels, exp, micro
    

##############################################################################
if __name__ == '__main__':
    config = config()
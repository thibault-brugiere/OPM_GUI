# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 09:26:31 2025

@author: tbrugiere
"""

class camera(object)   :
    "Object discribing camera settings"
    def __init__(self, camera_id):
        self.camera_id = 0
        self.hchipsize = 4432
        self.vchipsize = 2368
        self.pixel_size = 4.6 #in µm
        self.hsize = 4432
        self.hpos = 0
        self.vsize = 2308
        self.vpos = 0
        self.binning = 1
        self.exposure_time = 0.0087 # in seconds
        
class channel_config(object):
    "Object discribing channels settings"
    def __init__(self, channel_id, lasers = ["405","488","561","640"]):
        self.channel_id = channel_id
        self.is_active = False
        self.channel_order = None

        # Channel set from the interface
        self.laser_is_active = {}
        self.laser_power = {}
        self.filter = 'BFP' #Name of the filter in the weel
        self.camera = 0 #Camera ID
        self.exposure_time = 8.5 #Exposure time in ms
        
        for laser in lasers:
            self.laser_is_active[laser] = False
            self.laser_power[laser] = 0
            

class experiment(object):
    "Object discribing experiment settings"
    def __init__(self):
        self.timepoints = 0
        self.time_intervals = 0
        self.total_duration = 0
        self.scan_position = 0
        self.scan_range = 0
        self.channels = []
        
class microscope(object):
    def __init__(self):
        self.tilt_angle = 45 #in degrees
        self.slit_aperture = 800 #in µm
        
        self.lasers = ["405","488","561","640"]
        self.filters = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6']
        
        self.daq_channels = {"galvo": "Dev1/ao0",
                             "camera_0": "Dev1/port0/line0",
                             "405" : "Dev1/ao1",
                             "488" : None,
                             "561" : "Dev1/ao2",
                             "640" : "Dev1/ao3",
                             "laser_blanking" : "Dev1/port0/line3"
                             }
        
class microscope_values(object):
    def __init__(self):
        self.sample_pixel_size = 160 #in µm
        self.volts_per_um = 0.05
        self.volts_per_laser_percent = 5 / 100 # 5v max
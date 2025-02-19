# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 09:26:31 2025

@author: tbrugiere
"""
from datetime import date, datetime

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
        self.exp_name = 'Image'
        self.date_today = str(date.today())
        self.time_now = datetime.now().strftime("%H-%M-%S")
        
        self.timepoints = 10.0
        self.time_intervals = 1.0
        self.total_duration = 10.0
        
        self.aspect_ratio = 3
        self.scan_range = 0
        self.slit_aperture = 800 #in µm
        
        self.cameras = []
        self.channels = []
        
class microscope(object):
    def __init__(self):
        self.tilt_angle = 45 #in degrees
        
        # scanning galvo
        self.volts_per_um = 0.05
        
        # Filters
        self.filters = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6']
        
        # Lasers
        self.lasers = ["405","488","561","640"]
        self.volts_per_laser_percent_405 = 5 / 100 # 5v max
        self.volts_per_laser_percent_488 = 5 / 100 # 5v max
        self.volts_per_laser_percent_561 = 5 / 100 # 5v max
        self.volts_per_laser_percent_640 = 5 / 100 # 5v max
        
        # Microscope magnification
        self.sample_pixel_size = 0.160 #in µm
        
        # DAQ
        self.daq_channels = {"galvo": "Dev1/ao0",
                             "camera_1": "Dev1/port0/line0",
                             "camera_2": None,
                             "405" : "Dev1/ao1",
                             "488" : None,
                             "561" : "Dev1/ao2",
                             "640" : "Dev1/ao3",
                             "laser_blanking" : "Dev1/port0/line3"
                             }
        
        ##############################
        ## Microscope configuration ##
        ##############################
        
        # Objectives
        
            ## primary objective
        self.OBJ_1_MANUFACTURER = "Nikon"
        self.OBJ_1_MODEL = "CFI75 Apo 25XC W"
        self.OBJ_1_SN = "0000000"
        self.OBJ_1_MAGNIFICATION = 25
        self.OBJ_1_NA = 1.1
        self.OBJ_1_EFL = 8  # in mm
        self.OBJ_1_IM = "Water dipping"
        self.OBJ_1_IM_RI = 1.333
        
            ## secondary objective
        self.OBJ_1_MANUFACTURER = "Nikon"
        self.OBJ_1_MODEL = "CFI Plan Apochromat Lambda D 20X"
        self.OBJ_1_SN = "0000000"
        self.OBJ_1_MAGNIFICATION = 20
        self.OBJ_1_NA = 0.8
        self.OBJ_1_EFL = 10  # in mm
        self.OBJ_1_IM = "Air"
        self.OBJ_1_IM_RI = 1
        
            ## tertiary objective
        self.OBJ_3_MANUFACTURER = "Special Optics"
        self.OBJ_3_MODEL = "AMS-AGY v2.0"
        self.OBJ_3_SN = "0000"
        self.OBJ_3_MAGNIFICATION = 200/9
        self.OBJ_3_NA = 1.0
        self.OBJ_3_EFL = 9  # in mm
        self.OBJ_3_IM = "Glass"
        self.OBJ_3_IM_RI = 1.525
        #self.OBJ3_PIEZO_POS_UM = 0 #Dans le fichier original
        
        # Lenses
        
            ## tube lens 1
        self.TUBE_LENS_1_MANUFACTURER = "Thorlabs"
        self.TUBE_LENS_1_MODEL = "TTL200MP"
        self.TUBE_LENS_1_EFL = 200  # in mm

            ## tube lens 2
        self.TUBE_LENS_2_MANUFACTURER = "Thorlabs"
        self.TUBE_LENS_2_MODEL = "EFL188"
        self.TUBE_LENS_2_EFL = 188  # in mm

            ## tube lens 3
        self.TUBE_LENS_3_MANUFACTURER = "Nikon"
        self.TUBE_LENS_3_MODEL = "Nikon 200mm Tube Lens "
        self.TUBE_LENS_3_EFL = 200  # in mm

            ## scan lens 1
        self.SCAN_LENS_1_MANUFACTURER = "Thorlabs"
        self.SCAN_LENS_1_MODEL = "CLS-SL"
        self.SCAN_LENS_1_EFL = 70

            ## scan lens 2
        self.SCAN_LENS_2_MANUFACTURER = "Thorlabs"
        self.SCAN_LENS_2_MODEL = "CLS-SL"
        self.SCAN_LENS_2_EFL = 70
        
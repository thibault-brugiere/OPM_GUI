# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 09:26:31 2025

@author: tbrugiere
"""

LASERS = ["405","488","561","640"]

class camera(object):
    "Object discribing camera settings"
    # TODO: get camera brand, model, serial number 
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.hchipsize = 4432
        self.vchipsize = 2368
        self.pixel_size = 4.6 #in µm
        self.sample_pixel_size = 0.153 # in µm, calculated later
        self.hsize = 4432
        self.hpos = 0
        self.vsize = 2308
        self.vpos = 0
        self.binning = 1
        self.exposure_time = 0.0087 # in seconds
        self.line_readout_time = 8e-6 # (s) temps de lecture/ligne (7.309E-06/2 lignes d'aprés la doc)
        # Pour calculer le temps de lecture selon la vsize (Ne pas prendre en compte le binning !)
        
class channel_config(object):
    "Object discribing channels settings"
    def __init__(self, channel_id, lasers = LASERS): #lasers = ["405","488","561","640"]
        self.channel_id = channel_id # channel_id : nom du canal de type chr
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
            self.laser_power[laser] = 0 # laser_power en %
            

class experiment(object):
    "Object discribing experiment settings"
    def __init__(self):
        self.exp_name = 'Image'
        self.data_path = "D:/Projets_Python/OPM_GUI"
        self.timepoints = 10
        self.time_intervals = 1.0 # in s
        self.total_duration = 10.0 # in s
        
        self.scanner_position = 0
        self.scan_range = 20
        self.aspect_ratio = 3
        self.n_steps = 0 # Calculé plus tard
        self.step_size = 0 # Calculé plus tard
        
        self.slit_aperture = 800 #in µm
        
        self.cameras = []
        self.channels = []
        
class microscope(object):
    def __init__(self):
        
        self.tilt_angle = 45.0 #in degrees
        self.mag_total = 29.61
        
        # scanning galvo
        self.volts_per_um = 0.05
        self.galvo_response_time = 2.0  # A mesure in ms
        self.galvo_flyback_time = 3.0 # A mesurer in ms
        
        # stage
        self.stage_port = 'COM10'
        
        # Filters
        self.filters = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6'] #should be 6 options
        
        # Lasers
        self.lasers = LASERS # ["405","488","561","640"]
        self.volts_per_laser_percent = {'405' : 5.0 / 100.0, # 5v max
                                        '488' : 5.0 / 100.0, # 5v max
                                        '561' : 5.0 / 100.0, # 5v max
                                        '640' : 5.0 / 100.0  # 5v max
                                        }
        self.laser_response_time = 2.0 # in ms

        # DAQ
        self.daq_channels = {"co_channel": "Dev1/ctr0", # ADD: trigger start of each volume
                             "co_terminal": "/Dev1/PFI0", # ADD: trigger start of each volume
                             "galvo": "Dev1/ao0", # Fait bouger le galvo pour le scanning
                             "camera_0": "Dev1/port0/line0", # Trigger l'exposition de la camera
                             "camera_1": "Dev1/port0/line1", # Trigger l'exposition de la deuxieme camera (si presente)
                             "405" : "Dev1/ao1", # Régle la puissance du laser 405
                             "488" : "Dev1/ao2",      # Régle la puissance du laser 488
                             "561" : "Dev1/ao3", # Régle la puissance du laser 561
                             "640" : None, # Régle la puissance du laser 640
                             "laser_blanking" : "Dev1/port0/line3" # Trigger le blanking de l'AOTF du banc laser
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
        
        # Filters, dichroics
            ## Filter weel
            
            ## Filters
            
            ## Dichroic